---
title: HTML Playground
---

# HTML Playground

An in-browser, no-build conversational UI that connects to the Web Server.

## Usage

1. Start the web server:
```bash
python -m playbooks.applications.web_server
```

2. Open the Playground (application/playbooks_playground.html in playbooks repository) in your browser

3. Enter a Playbooks program path (e.g., `tests/data/02-personalized-greeting.pb`) and click Run Program

The UI will:

- Create a run via `POST http://localhost:8000/runs/new`
- Connect to `ws://localhost:8001/ws/<run_id>`
- Stream messages and execution logs with filtering controls




