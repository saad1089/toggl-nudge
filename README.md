# Windows Background Toggl Processor (Toggl Nudge)

A lightweight background utility for Windows that nudges you to track your time in Toggl if you're active but not currently recording an entry.

## **Overview**
This project follows the [Graze Skeleton Project](https://github.com/graze-ai/project-template) structure. It uses the Toggl API to monitor current time entries and displays a Windows notification (nudge) if time tracking is forgotten or needs attention.

## **Directory Structure**
```text
├── configs/              # configuration files for the nudge logic
├── data/                 # local data and logs (toggl_nudge.log)
├── docs/                 # documentation for the project
├── notebooks/            # experimentation and R&D notebooks
├── scripts/              # utility scripts like get_toggl_projects.py
├── src/                  # main source code (toggl_nudge.pyw)
├── tests/                # test scripts (toggl_nudge_test.py)
├── Makefile              # automation for setup and running
├── run_nudge.bat         # entry point for Windows background execution
└── requirements.txt      # Python dependencies
```

## **Installation**
1.  Ensure you have Python installed.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Install dependencies:
    ```bash
    make install
    ```
4.  Configure your credentials in a `.env` file based on `.env.example`.

## **Usage**
-   **Run in background:** Execute `run_nudge.bat`. This will start the processor without a terminal window.
-   **Run for testing:** Run `make test` or execute `tests/toggl_nudge_test.py` directly.
-   **Fetch Projects:** Run `python scripts/get_toggl_projects.py` to list your Toggl projects.

## **Key Components**
-   `src/toggl_nudge.pyw`: The core engine that runs in the background.
-   `run_nudge.bat`: A simple batch script to launch the background process.
-   `toggl_nudge.log`: Log file used for monitoring script behavior and errors.

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.
