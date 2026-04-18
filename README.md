# Windows Toggl Nudge Processor

A lightweight Python-based background processor designed for Windows to provide configurable nudges and reminders based on your Toggl track activity. This utility helps users stay focused and track their time effectively by prompting them at set intervals if no Toggl entry is active or if an entry exceeds a certain duration.

## Project Files:

*   `run_nudge.bat`: This batch file is the entry point for running the `toggl_nudge.pyw` script in the background on Windows. It's designed to be executed without opening a console window.
*   `toggl_nudge.pyw`: The main Python script that implements the Toggl nudge logic. It checks your current Toggl status and displays reminders based on predefined rules. The `.pyw` extension ensures that it runs without a visible Python console.
*   `toggl_nudge_test.pyw`: A test version of the nudge script, possibly configured for more frequent or specific test cases (e.g., showing every 10 seconds as mentioned by the user).
*   `get_toggl_projects.py`: A utility script to fetch and display Toggl projects. This might be used for configuration or debugging purposes.
*   `toggl_nudge.log`: A log file where `toggl_nudge.pyw` writes output, errors, or debugging information. Useful for troubleshooting and monitoring the script's execution.
*   `.env`: This file (ignored by Git) is used to store environment variables, such as your Toggl API key and workspace ID, ensuring that sensitive information is not hardcoded in the scripts.

## Setup:

1.  **Clone this repository** (after it's pushed to GitHub).
2.  **Install Python:** Ensure you have Python 3.x installed.
3.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt # (A requirements.txt will be generated later)
    ```
5.  **Configure `.env`:** Create a `.env` file in the root directory (if it doesn't exist) and add your Toggl API token and workspace ID:
    ```
    TOGGL_API_TOKEN=your_toggl_api_token_here
    TOGGL_WORKSPACE_ID=your_toggl_workspace_id_here
    ```
    *   You can find your Toggl API token in your Toggl Profile Settings.
    *   You can get your Toggl Workspace ID by checking the URL when you're logged into Toggl Track (e.g., `https://track.toggl.com/workspace/<WORKSPACE_ID>/dashboard`).

## Usage:

To run the main nudge processor, you would typically execute `run_nudge.bat`. Refer to the `run_nudge.bat` file for specific execution details.

## Development:

*   **Testing:** Use `toggl_nudge_test.pyw` for quick testing of nudge logic.
*   **Logging:** Monitor `toggl_nudge.log` for any issues or to understand script behavior.

---

**Note:** This project utilizes the `python-dotenv` library for loading environment variables and `toggl-python` for interacting with the Toggl API.
