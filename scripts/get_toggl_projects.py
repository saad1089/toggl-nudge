import os
from dotenv import load_dotenv
from toggl_python import TokenAuth, Workspace

# Load environment variables from .env file
load_dotenv()

# Retrieve Toggl API Key from environment variables
TOGGL_API_KEY = os.getenv("TOGGL_API_KEY")

if not TOGGL_API_KEY:
    print("Error: TOGGL_API_KEY not found in environment variables or .env file.")
    print("Please ensure your .env file is correctly set up with TOGGL_API_KEY=YOUR_API_KEY")
    exit()

try:
    # Initialize the Toggl auth with your API key
    auth = TokenAuth(token=TOGGL_API_KEY)

    # Initialize the Workspace client
    ws_client = Workspace(auth=auth)

    print("Fetching Toggl Workspaces and Projects...")

    # Get all workspaces
    workspaces = ws_client.list()

    if not workspaces:
        print("No workspaces found for this API key.")
    else:
        for ws in workspaces:
            print(f"\n--- Workspace: {ws.name} (ID: {ws.id}) ---")

            # Get projects for the current workspace
            projects = ws_client.get_projects(workspace_id=ws.id)

            if not projects:
                print("  No projects found in this workspace.")
            else:
                for project in projects:
                    print(f"  Project: {project.name} (ID: {project.id}, Active: {project.active})")

except Exception as e:
    print(f"An error occurred: {e}")

