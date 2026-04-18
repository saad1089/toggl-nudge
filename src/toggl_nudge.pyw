import os
import sys
import logging
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# --- OPTIMIZATION: Set Low Process Priority for Windows ---
if sys.platform == 'win32':
    import psutil
    p = psutil.Process(os.getpid())
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

# Setup logging (minimal)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
log_file = os.path.join(project_root, "data", "toggl_nudge.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO, # Changed from DEBUG to INFO to save disk I/O
    format="%(asctime)s - %(message)s"
)

# Redirect only errors to log to keep it quiet
sys.stderr = open(log_file, 'a', buffering=1)

load_dotenv(os.path.join(project_root, ".env"))
TOGGL_API_KEY = os.getenv("TOGGL_API_KEY")

SHORTCUTS = {
    'w': ("work", 183382585),
    'a': ("admin", 169586280),
    'v': ("waste of time", 172747402),
    's': ("stretches", 175817767)
}

class TogglNudgeApp:
    def __init__(self):
        self.auth = None
        self.ws_client = None
        self.workspace_id = None
        self.project_map = {}
        self.focus_until = datetime.now()
        
        # Setup UI first (Tkinter is very light when hidden)
        self.root = tk.Tk()
        self.root.withdraw()
        self.setup_ui()
        
        # Lazy Loading: Only connect to Toggl when we actually need it
        self.root.after(100, self.show_nudge)
        self.root.mainloop()

    def connect_toggl(self):
        """Only connects when the window is about to show."""
        if self.ws_client: return True
        try:
            from toggl_python import TokenAuth, Workspace
            self.auth = TokenAuth(token=TOGGL_API_KEY)
            self.ws_client = Workspace(auth=self.auth)
            workspaces = self.ws_client.list()
            if workspaces:
                self.workspace_id = workspaces[0].id
                projects = self.ws_client.get_projects(workspace_id=self.workspace_id)
                self.project_map = {p.name.lower(): p.id for p in projects}
                return True
        except Exception:
            return False
        return False

    def setup_ui(self):
        self.nudge_window = tk.Toplevel(self.root)
        self.nudge_window.withdraw()
        self.nudge_window.attributes("-topmost", True)
        self.nudge_window.overrideredirect(True)
        
        # UI colors and layout (Static, so no CPU cost after creation)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width, height = 300, 160
        self.nudge_window.geometry(f"{width}x{height}+{screen_width - width - 20}+{screen_height - height - 60}")
        self.nudge_window.configure(bg="#2c3e50")
        
        tk.Label(self.nudge_window, text="What are you working on?", fg="white", bg="#2c3e50", font=("Arial", 12, "bold")).pack(pady=5)
        self.entry = tk.Entry(self.nudge_window, width=30)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda e: self.submit_custom())
        
        tk.Label(self.nudge_window, text="(W)ork | (A)dmin | (V)aste | (S)tretch", fg="#ecf0f1", bg="#2c3e50", font=("Arial", 9)).pack()
        
        btn_frame = tk.Frame(self.nudge_window, bg="#2c3e50")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Focus", command=self.prompt_focus).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Skip", command=self.hide_nudge).pack(side=tk.LEFT, padx=5)
        self.nudge_window.bind("<Key>", self.handle_key)

    def handle_key(self, event):
        if self.entry.get(): return
        key = event.char.lower()
        if key in SHORTCUTS:
            name, pid = SHORTCUTS[key]
            self.start_timer(pid, name)
            self.hide_nudge()

    def submit_custom(self):
        name = self.entry.get().strip().lower()
        if not name: self.hide_nudge(); return
        
        pid = self.project_map.get(name)
        if not pid:
            matches = [pname for pname in self.project_map.keys() if name in pname]
            if matches: pid = self.project_map[matches[0]]; name = matches[0]
            
        if pid:
            self.start_timer(pid, name)
            self.hide_nudge()
        else:
            messagebox.showwarning("Unknown", f"Project '{name}' not found.")

    def start_timer(self, project_id, description):
        try:
            self.ws_client.create_time_entry(
                workspace_id=self.workspace_id,
                project_id=project_id,
                description=description,
                start_datetime=datetime.now(timezone.utc),
                duration=-1,
                created_with="TogglNudge"
            )
        except Exception: pass

    def prompt_focus(self):
        duration = simpledialog.askstring("Focus", "Hours?")
        if duration:
            try:
                self.focus_until = datetime.now() + timedelta(hours=float(duration))
                self.hide_nudge()
            except ValueError: pass

    def show_nudge(self):
        if datetime.now() > self.focus_until:
            if self.connect_toggl():
                self.nudge_window.deiconify()
                self.nudge_window.lift()
                self.entry.delete(0, tk.END)
                self.entry.focus_set()
        
        # Re-check every 30 mins
        self.root.after(1800000, self.show_nudge)

    def hide_nudge(self):
        self.nudge_window.withdraw()

if __name__ == "__main__":
    try:
        TogglNudgeApp()
    except Exception:
        sys.exit(1)
