import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from toggl_python import TokenAuth, Workspace

# Load environment variables with absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
load_dotenv(env_path)
TOGGL_API_KEY = os.getenv("TOGGL_API_KEY")

if not TOGGL_API_KEY:
    print("Error: TOGGL_API_KEY not found in .env")
    exit(1)

# Shortcuts mapping
SHORTCUTS = {
    'w': ("work", 183382585),
    'a': ("admin", 169586280),
    'v': ("waste of time", 172747402),
    's': ("stretches", 175817767)
}

class TogglNudgeTest:
    def __init__(self):
        self.auth = TokenAuth(token=TOGGL_API_KEY)
        self.ws_client = Workspace(auth=self.auth)
        
        print("--- TEST MODE ---")
        print("Fetching Toggl data...")
        try:
            self.workspaces = self.ws_client.list()
            if not self.workspaces:
                print("No workspaces found.")
                exit(1)
            
            # Use the first workspace (Saad Ali's workspace)
            self.workspace_id = self.workspaces[0].id
            print(f"Using Workspace: {self.workspaces[0].name} (ID: {self.workspace_id})")
            
            self.projects = self.ws_client.get_projects(workspace_id=self.workspace_id)
            self.project_map = {p.name.lower(): p.id for p in self.projects}
            print(f"Loaded {len(self.projects)} projects.")
            
        except Exception as e:
            print(f"Initialization Error: {e}")
            exit(1)
            
        self.focus_until = datetime.now()
        
        self.root = tk.Tk()
        self.root.withdraw()
        self.setup_ui()
        
        # TEST: Trigger every 10 seconds
        self.schedule_nudge()
        
        print("\n[READY] Test script running.")
        print("Nudge will appear every 10 seconds.")
        print("Check this terminal for logs when you click a button.\n")
        self.root.mainloop()

    def setup_ui(self):
        self.nudge_window = tk.Toplevel(self.root)
        self.nudge_window.title("Toggl Nudge TEST")
        self.nudge_window.attributes("-topmost", True)
        self.nudge_window.overrideredirect(True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width, height = 300, 150
        x = screen_width - width - 20
        y = screen_height - height - 60
        self.nudge_window.geometry(f"{width}x{height}+{x}+{y}")
        self.nudge_window.configure(bg="#e74c3c")
        
        tk.Label(self.nudge_window, text="TEST: What are you doing?", fg="white", bg="#e74c3c", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.entry = tk.Entry(self.nudge_window, width=30)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda e: self.submit_custom())
        
        tk.Label(self.nudge_window, text="(W)ork | (A)dmin | (V)aste | (S)tretch", fg="white", bg="#e74c3c").pack()
        
        btn_frame = tk.Frame(self.nudge_window, bg="#e74c3c")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Focus", command=self.prompt_focus).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Skip", command=self.hide_nudge).pack(side=tk.LEFT, padx=5)

        self.nudge_window.bind("<Key>", self.handle_key)
        self.nudge_window.withdraw()

    def handle_key(self, event):
        key = event.char.lower()
        if key in SHORTCUTS:
            name, pid = SHORTCUTS[key]
            self.start_timer(pid, name)
            self.hide_nudge()

    def submit_custom(self):
        name = self.entry.get().strip().lower()
        if name in self.project_map:
            self.start_timer(self.project_map[name], name)
            self.hide_nudge()
        else:
            matches = [pname for pname in self.project_map.keys() if name in pname]
            if matches:
                match = matches[0]
                self.start_timer(self.project_map[match], match)
                self.hide_nudge()
            else:
                messagebox.showwarning("Unknown Project", f"No project found: {name}")

    def start_timer(self, project_id, description):
        try:
            print(f"\n[ACTION] Attempting to start timer: '{description}'")
            
            # Use timezone-aware UTC datetime
            now_utc = datetime.now(timezone.utc)
            
            print(f"Sending to Toggl: PID={project_id}, Start={now_utc.isoformat()}")
            
            response = self.ws_client.create_time_entry(
                workspace_id=self.workspace_id,
                project_id=project_id,
                description=description,
                start_datetime=now_utc, # Pass the datetime object directly
                duration=-1, # Try -1 first, as it's standard for 'running'
                created_with="TogglNudgeTest"
            )
            
            print(f"Success! New entry created with ID: {response.id}")
            
        except Exception as e:
            print(f"API ERROR: {e}")
            messagebox.showerror("API Error", f"Failed to start timer: {e}")

    def prompt_focus(self):
        duration = simpledialog.askstring("Focus", "Hours?")
        if duration:
            try:
                self.focus_until = datetime.now() + timedelta(hours=float(duration))
                print(f"Focus active until {self.focus_until.strftime('%H:%M:%S')}")
                self.hide_nudge()
            except ValueError:
                pass

    def schedule_nudge(self):
        self.root.after(10000, self.show_nudge)

    def show_nudge(self):
        if datetime.now() > self.focus_until:
            print("\n[EVENT] Nudge popup appearing...")
            self.nudge_window.deiconify()
            self.nudge_window.lift()
            self.nudge_window.attributes("-topmost", True)
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
        self.schedule_nudge()

    def hide_nudge(self):
        self.nudge_window.withdraw()

if __name__ == "__main__":
    TogglNudgeTest()
