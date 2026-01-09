# Agentic Systems

This repository is a collection of multiple production-grade agentic systems, demonstrating advanced use of AI, automation, and orchestration using state-of-the-art frameworks.

## Repository Structure

- `/systems/` — Each agentic system lives in its own subdirectory here. Designed for modular, production-ready deployment or customization.
- `requirements.txt` — Shared dependencies for all systems.
- `.gitignore` — Exclude secrets, caches, and Python artifacts.
- `.env.example` — Template for common environment variables (e.g. API keys).


### Current Systems

| System Name         | Path                               | Description                          |
|---------------------|------------------------------------|--------------------------------------|
| Translator Agent   | `systems/translator-agent/`       | Baseline example: bootstrapped Python app using LangGraph and OpenAI |


## Getting Started

### Set up a Python Virtual Environment (Recommended)

Before installing dependencies, create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```
### Install Dependencies

Install the shared dependencies at the repo root:

```sh
python3 -m pip install -r requirements.txt
```

### Set up environment variables 

Create a `.env` file by copying `.env.example` and add necessary configuration values and API keys.

```sh
cp .env.example .env 
```

### Running an agentic system

### Running an agentic system
From `src` directory
```sh
python -m systems.restaurant-finder-agent.main
```

```sh
python -m systems.translator-agent.main
```

### Running tests
From `src` directory
```sh
python -m tools.test_tavily_web_search
```