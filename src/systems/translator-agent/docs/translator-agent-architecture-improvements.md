# Translator Agent (systems/translator-agent) — Architecture Analysis and Improvement Plan

## 1) Current Architecture Snapshot

- Entry point (`systems/translator-agent/main.py`)
  - Builds agent via `build_agent()`
  - Prints graph ASCII
  - Invokes agent with `{"user_query": "..."}` and prints `state["output_query"]`
- Agent graph (`systems/translator-agent/agent.py`)
  - `StateGraph` with a single node: `translator`
  - Edges: `START -> translator -> END`
  - `compile()` returns runnable graph
- State schema (`systems/translator-agent/agent_state.py`)
  - `AgentState` `TypedDict`:
    - `messages`: `Annotated[list, add_messages]`
    - `user_query`: `str`
    - `output_query`: `str`
  - `add_messages` aggregator allows nodes to append messages and accumulate across steps
- Translator node (`systems/translator-agent/nodes/translator_node.py`)
  - Creates `Config()`; constructs `ChatOpenAI` per invocation
  - Uses system + human messages; includes prior messages from state
  - Invokes model and returns assistant response in `messages` plus `output_query`
- Config (`systems/translator-agent/config.py`)
  - Loads `.env`; requires `OPENAI_API_KEY` and `OPENAI_MODEL_NAME`
  - Exposes `openai_api_key` and `openai_model_name`

## 2) Dataflow

- Input: `main.py` supplies `{"user_query": "..."}` (currently no explicit `messages`)
- Node:
  - Reads config, creates `ChatOpenAI`
  - Builds `SystemMessage` (translator role) and `HumanMessage` from `user_query`
  - Appends `state["messages"]` (if present) for conversation context
  - Invokes model, returns `{"messages": [assistant_response], "output_query": response.content}`
- State evolution:
  - `add_messages` merges returned assistant message with previous state messages

## 3) Strengths

- Clear modular separation (config, graph assembly, node logic, state schema)
- Correct use of LangGraph `StateGraph` and `add_messages` to support memory accumulation
- Dual output: conversational `messages` + simplified `output_query` for easy consumption
- Environment-driven API key and model name with fail-fast validation

## 4) Issues / Risks

- Messages initialization
  - `main.py` does not pass `messages`; `translator_node` indexes `state["messages"]` when building the prompt
  - Potential `KeyError` or type mismatch if `state["messages"]` is absent or not a list of LangChain `BaseMessage`
- Model client lifecycle
  - `ChatOpenAI` re-created on every node invocation; adds latency and overhead
- Generation controls
  - `temperature=0.9` is high for translation; promotes non-determinism
  - `max_tokens=100` risks truncation on longer translations
- Operational hardening
  - Missing request timeout and retries; requests may hang or fail transiently without retry strategy
  - No structured error handling; exceptions bubble up and abort execution
- Observability
  - No logging/telemetry for latency, token usage, or errors; hard to debug
- Prompt constraints
  - System prompt does not strictly constrain output; risk of meta-text (e.g., “Here is the translation …”)
- Tools integration
  - `tools/example_tool.py` is unused; no `ToolNode` or chained tool integration
- Extensibility limits
  - Single-node graph; no language detection/routing/post-processing/quality safeguards
- Testing
  - No unit tests for node behavior, state handling, config loading, or error flows
- API parameter compatibility
  - Depending on `langchain_openai` version, timeout parameter may be `timeout` or `request_timeout`; can cause runtime error if wrong

## 5) Recommendations (prioritized)

### High priority (correctness/robustness)
- Safe messages handling
  - In `translator_node`, use `prior_messages = state.get("messages", [])` rather than `state["messages"]`
  - Optionally validate that `prior_messages` are LangChain `BaseMessage` instances before including
- Deterministic translation defaults
  - `temperature`: 0.0–0.3 (suggest 0.1)
  - `max_tokens`: `None` or generous cap (512–1024) to avoid truncation; keep configurable
  - Add “Reply with only the translation.” to the system prompt
- Client reuse/caching
  - Use a cached factory (e.g., `@lru_cache`) to avoid recreating `ChatOpenAI` for each invocation; key cache by `api_key`, `model`, `temperature`, `max_tokens`, `timeout`, `max_retries`
- Operational hardening
  - Add timeout and retry configuration; pass to `ChatOpenAI` via `timeout` (or `request_timeout`) and `max_retries`
  - Wrap `model.invoke` in `try/except`; on error, return `{"messages": [], "output_query": ""}` or structured error, and log exception

### Medium priority (quality/observability)
- Logging/telemetry
  - Log model name, parameters, latency, token usage, and errors
  - Consider LangChain callbacks for tracing, or integrate your logger
- Prompt refinement
  - Support optional config for formality/tone/dialect
  - Explicitly instruct “Do not include quotes or backticks; output French only.”
- State typing/rules
  - Refine typing to ensure `messages` is `Sequence[BaseMessage]`
  - Consider runtime checks to coerce plain dicts into Messages if upstream feeds non-Message content
- `main.py` clarity
  - Initialize `messages: []` when invoking the graph (unless using safe get in the node)
  - Optionally add argparse for user input; print both the graph and parameters

### Optional / strategic (extensibility)
- Multi-node LangGraph pipeline
  - Node A: Language detection / no-op router (if already French, skip translation)
  - Node B: Translation
  - Node C: Post-processing (quality checks, profanity filtering, PII redaction, glossary/terminology enforcement)
  - Conditional edges based on detection/confidence and validations
- Tools integration
  - If glossary or domain-specific lookups are needed, integrate `tools/example_tool.py` via a `ToolNode` or as a retriever/tool callable in the chain
- Streaming
  - Enable `streaming=True` output with callbacks for progressive UI updates
- Model strategy
  - Keep `OPENAI_MODEL_NAME` configurable; choose defaults that balance cost/quality/latency (e.g., `gpt-4o-mini` where available, fallback to `gpt-3.5-turbo`)

## 6) Concrete Code Suggestions

### 6.1 Config extensions (keep existing properties; add optional tuning and ops)
- Add environment variables (with sane defaults):
  - `OPENAI_TEMPERATURE` (default `"0.1"`)
  - `OPENAI_MAX_TOKENS` (optional; unset means `None`)
  - `OPENAI_TIMEOUT` (default `"30"`)
  - `OPENAI_MAX_RETRIES` (default `"2"`)
- Expose properties:
  - `openai_temperature: float`
  - `openai_max_tokens: Optional[int]`
  - `openai_timeout: float`
  - `openai_max_retries: int`

Example:
```python
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self._openai_api_key:
            raise EnvironmentError("OPENAI_API_KEY not set.")

        self._openai_model_name = os.getenv("OPENAI_MODEL_NAME")
        if not self._openai_model_name:
            raise EnvironmentError("OPENAI_MODEL_NAME not set.")

        # New optional configs with defaults
        self._openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
        max_tokens_env = os.getenv("OPENAI_MAX_TOKENS")
        self._openai_max_tokens = int(max_tokens_env) if max_tokens_env else None
        self._openai_timeout = float(os.getenv("OPENAI_TIMEOUT", "30"))
        self._openai_max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "2"))

    @property
    def openai_api_key(self):
        return self._openai_api_key

    @property
    def openai_model_name(self):
        return self._openai_model_name

    @property
    def openai_temperature(self):
        return self._openai_temperature

    @property
    def openai_max_tokens(self):
        return self._openai_max_tokens

    @property
    def openai_timeout(self):
        return self._openai_timeout

    @property
    def openai_max_retries(self):
        return self._openai_max_retries
```

### 6.2 Cached ChatOpenAI factory and `translator_node` refactor

- Caches model instance
- Safer state access
- Deterministic defaults
- Timeouts and retries
- Error handling
- Stricter output prompt

```python
from functools import lru_cache
from typing import Optional, Sequence
from config import Config
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from agent_state import AgentState

@lru_cache(maxsize=8)
def get_chat_model(
    api_key: str,
    model: str,
    temperature: float,
    max_tokens: Optional[int],
    timeout: float,
    max_retries: int,
) -> ChatOpenAI:
    return ChatOpenAI(
        openai_api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,   # Prefer None unless you must cap
        timeout=timeout,         # If this raises, try request_timeout instead
        max_retries=max_retries,
    )

def translator_node(state: AgentState) -> AgentState:
    config = Config()

    prior_messages: Sequence[BaseMessage] = state.get("messages", [])
    user_query = (state.get("user_query") or "").strip()
    if not user_query:
        return {"messages": [], "output_query": ""}

    model = get_chat_model(
        api_key=config.openai_api_key,
        model=config.openai_model_name,
        temperature=getattr(config, "openai_temperature", 0.1),
        max_tokens=getattr(config, "openai_max_tokens", None),
        timeout=getattr(config, "openai_timeout", 30.0),
        max_retries=getattr(config, "openai_max_retries", 2),
    )

    system_message = SystemMessage(
        content=(
            "You are a highly skilled translator. Translate the user's message into French, "
            "maintaining the original meaning and tone. Reply with only the translation."
        )
    )
    human_message = HumanMessage(content=user_query)

    try:
        response = model.invoke([system_message, *prior_messages, human_message])
    except Exception:
        # Optionally log exception
        return {"messages": [], "output_query": ""}

    return {"messages": [response], "output_query": response.content}
```

### 6.3 `main.py` initialization (optional if using safe get in node)

Initialize messages to avoid any surprises:

```python
state = agent.invoke({"messages": [], "user_query": user_query})
```

### 6.4 `.env` additions (optional)

```bash
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=
OPENAI_TIMEOUT=30
OPENAI_MAX_RETRIES=2
```

### 6.5 Testing plan

- Unit tests (pytest):
  - `test_empty_input_returns_empty_output`
  - `test_low_temperature_determinism`
  - `test_long_input_no_truncation_when_max_tokens_none`
  - `test_messages_aggregation_with_add_messages`
  - `test_model_invocation_error_handling_returns_safe_state`
  - `test_config_loading_defaults_and_overrides`
- Integration smoke test:
  - Setup `.env`, call `main`, verify output in French for a given English input

## 7) Observability and operations

- Add simple logging around the node:
  - Parameters (model, temperature, tokens)
  - Latency per invoke
  - Token usage (if available via callbacks/response metadata)
  - Exceptions
- Consider LangChain callbacks or custom tracer for dev/prod
- Add `max_retries` for transient errors; consider exponential backoff

## 8) Extensibility roadmap (LangGraph)

- Detection node:
  - Detect input language; if already French (or same as target), route to `END`
- Translation node:
  - Current node (hardened)
- Post-processing node:
  - Quality checks, term/glossary enforcement, profanity/PII redaction
- Router edges based on detection confidence and validation results

## 9) Model choice and version notes

- Keep `OPENAI_MODEL_NAME` configurable; recommended modern default when accessible (e.g., `gpt-4o-mini`)
- For cost/latency-sensitive environments, allow fallback to `gpt-3.5-turbo`
- LangChain/ChatOpenAI parameter names:
  - `timeout` vs `request_timeout` may vary by version; switch to `request_timeout` if `timeout` raises a `TypeError`
- Streaming:
  - If desired, enable `streaming=True` and wire callbacks to stream tokens for better UX

## 10) Summary of key parameter recommendations

- `temperature`: 0.1 (default), configurable 0.0–0.3
- `max_tokens`: `None` (default) or 512–1024 if you must cap
- `timeout`/`request_timeout`: 30s default
- `max_retries`: 2 default
- Prompt addition: “Reply with only the translation.” and optionally “Output French only; do not include quotes/backticks.”
