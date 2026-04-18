install:
	pip install -r requirements.txt

run:
	pythonw.exe src/toggl_nudge.pyw

test:
	pythonw.exe tests/toggl_nudge_test.py