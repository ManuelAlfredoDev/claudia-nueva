# Claudia Nueva - Operational Assistant Prototype

## Overview

This sanitized local demo illustrates the HTTP boundary of a modular operational-assistant prototype under active development.

## Features

- `GET /health` reports demo-local status.
- `POST /chat` accepts a JSON object with `text`.
- `POST /voice` uses the same safe, simulated conversation path.
- No external system, credential, or operational dataset is used.
- A responsive local web page demonstrates chat, health, and the simulated voice route.

## Technologies

Python, JSON, standard-library HTTP server, automated tests.

## Run

```bash
python app.py
```

Then send `{"text":"hello"}` to `http://127.0.0.1:8765/chat`.

## Test

```bash
python -m unittest discover -s tests
```

## Current status

In development. The voice route is a simulated interface, not a speech-recognition or speech-synthesis product.

## Security and privacy

This repository is a standalone demo with fictional responses only. See [SECURITY.md](SECURITY.md).
