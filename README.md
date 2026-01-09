# Agentic Systems

This repository is a collection of multiple production-grade agentic systems, demonstrating advanced use of AI, automation, and orchestration using state-of-the-art frameworks.

Currently this repository has the following agentic systems:
- Translator Agent
- Restaurant Finder Agent

## Repository Structure

- `/systems/` — Each agentic system lives in its own subdirectory here. Designed for modular, production-ready deployment or customization.
- `/tools/` - Reusable tools used in multiple agentic systems.
- `requirements.txt` — Shared dependencies for all systems.
- `.gitignore` — Exclude secrets, caches, and Python artifacts.
- `.env.example` — Template for common environment variables (e.g. API keys).


## Getting Started

### Set up a Python virtual environment

Before installing dependencies, create and activate a virtual environment.

Create a virtual environment: 
```sh
python3 -m venv venv
```

Activate the virtual enviroment:
```sh
source venv/bin/activate
```


### Install dependencies

Install the shared dependencies:

```sh
python3 -m pip install -r requirements.txt
```

### Set up environment variables 

Create a `.env` file by copying `.env.example` and add necessary configuration values and API keys.

```sh
cp .env.example .env 
```

Update `.env` file with your API keys:
```
OPENAI_API_KEY=your-openai-key-here

OPENAI_MODEL_NAME=your-openai-model-name-here

TAVILY_API_KEY=your-taviliy-api-key-here
```

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