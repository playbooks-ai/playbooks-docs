---
title: Web Server
---

# Web Server

A WebSocket-first server exposes an HTTP API to create runs and a WebSocket to stream all execution events, enabling custom UIs.

## Run the server

```bash
python -m playbooks.applications.web_server --host localhost --http-port 8000 --ws-port 8001
```

On start, it prints endpoints like:

- HTTP API: `http://localhost:8000`
- WebSocket: `ws://localhost:8001`
- Create run: `POST /runs/new`

## HTTP API

- `POST /runs/new` with JSON body:

```json
{ "path": "tests/data/02-personalized-greeting.pb" }
```

or

```json
{ "program": "# ... full Playbooks program ..." }
```

Response:

```json
{ "run_id": "<uuid>" }
```

## WebSocket

Connect to `ws://localhost:8001/ws/<run_id>` to receive a stream of events:

- Connection, start, termination
- Agent messages and streaming updates
- Human input prompts
- Meeting broadcasts
- Session log entries

## Typical flow

1. Start server
2. `POST /runs/new` with `{ path: "my.pb" }`
3. Open WebSocket and render events in your UI

See also: [Playground](playground.md) for a ready-made HTML client.


