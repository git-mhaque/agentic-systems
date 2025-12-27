# Agentic Systems

This repository is a collection of multiple production-grade agentic systems, demonstrating advanced use of AI, automation, and orchestration using state-of-the-art frameworks.

## Repository Structure

- `/systems/` — Each agentic system lives in its own subdirectory here. Designed for modular, production-ready deployment or customization.
- `requirements.txt` — Shared dependencies for convenience. Each system may also have its own dependencies.
- `.gitignore` — Exclude secrets, caches, and Python artifacts.
- `.env.example` — Template for common environment variables (e.g. API keys).


### Current Systems

| System Name         | Path                               | Description                          |
|---------------------|------------------------------------|--------------------------------------|
| Translator Agent   | `systems/translator-agent/`       | Baseline example: bootstrapped Python app using LangChain and OpenAI |

_More systems coming soon!_

## Getting Started

### (Recommended) Set up a Python Virtual Environment

Before installing dependencies, create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

```bat
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

Install the shared dependencies at the repo root:

```sh
python3 -m pip install -r requirements.txt
```
