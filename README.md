# AgentForge

AgentForge is an open‑source, agentic AI template application designed to help teams quickly onboard their existing knowledge, tools, or data sources into an agentic workflow. It provides a ready‑to‑extend foundation for building conversational business copilots with structured tool‑calling and reasoning patterns.

The system uses an MCP‑style server implemented as a REST‑based FastAPI service, exposing tool metadata and tool invocations through clean HTTP endpoints. While the sample implementation focuses on media‑rights workflows (contracts, amortization, costs, payments, and closing data), the architecture is intentionally domain‑agnostic — allowing developers to adapt or extend it for any business vertical with minimal effort.

## Why AgentForge

- Provides a practical baseline for agentic application development with separation of concerns.
- Implements a tool-first retrieval pattern before response synthesis.
- Combines deterministic planning fallback with LLM-based planning for reliability.
- Supports AI LLM fundamental models from multiple providers through configuration.

## Core Agentic Flow

1. User asks a natural language question in chat.
2. Orchestration layer plans tool calls (LLM planner with heuristic fallback).
3. MCP-Like REST server executes tools against PostgreSQL data.
4. Tool outputs are aggregated and passed to the response synthesis prompt.
5. Chat UI returns a grounded, context-aware final answer.

## Technology Stack

### Agentic Development Core

- LangChain: agent orchestration, planning, prompt chaining, and model integration.
- Pydantic: tool contract and response schema validation for reliable structured outputs.
- LangSmith: tracing and observability for agent runs, planning paths, and tool-call visibility.
- Streamlit: conversational chat UI for rapid prototyping and agent workflow demos.

### Platform and Runtime

- FastAPI: REST API implementation for the MCP-Style server.
- PostgreSQL: structured transactional data store.
- Python 3.11+: primary language for all runtime modules.
- python-dotenv: environment-driven configuration.

## LLM Abstraction and Model Support

AgentForge uses an abstraction layer for model selection and runtime configuration:

- `orchestration/config.py` centralizes provider and model settings from environment variables.
- `orchestration/llm_factory.py` builds the selected chat model implementation.
- `LLM_PROVIDER` controls provider selection without changing business logic.

Supported providers:

- `openai`
- `gemini`
- `groq`
- `ollama`

This lets you swap between hosted and local AI LLM fundamental models through configuration only.

## Repository Structure

- `ui/`: Streamlit chat interface.
- `orchestration/`: planning, prompting, MCP client, observability, and model factory.
- `mcp_server/`: REST-based MCP-Like server, tool registry, schemas, and DB service layer.
- `database/postgres/sql/`: schema, seed, bulk seed, and select/query scripts.
- `docs/`: internal notes and planning documents.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL running locally or remotely
- Optional for local model inference: Ollama
- Optional for tracing and observability: langsmith

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```powershell
Copy-Item .env.example .env
```

Update `.env` with your PostgreSQL, LLM provider and other settings.

### 3. Prepare database

Create database `media_rights`, then apply SQL scripts in this order:

1. `database/postgres/sql/01_schema.sql`
2. `database/postgres/sql/02_seed_data.sql`
3. `database/postgres/sql/03_seed_bulk_data.sql`

### 4. Start MCP-Style REST server

```bash
uvicorn mcp_server.app:app --host 0.0.0.0 --port 8000 --reload
```

Health check endpoint: `GET /health`

### 5. Start Streamlit UI

```bash
streamlit run ui/app.py
```

## Example Questions

- Give amort schedule for contract CN-2026-100
- Show title list and payment schedule for contract CN-2026-101
- Compare license cost vs subdub cost for contract CN-2026-101
- Provide contract closing data for contract CN-2026-101
- Compare Payment for contracts CN-2026-100 and CN-2026-101
- Compare amortization across contracts CN-2026-100, CN-2026-101, CN-2026-103, and CN-2026-104 in a tabular format, with contracts as columns and rows for total amortization, amortization window duration (period start-end), and comma-separated titles.

## Future Plans

1. Multi-server orchestration with stable MCP server design:
	- Extend the orchestration layer to register multiple MCP servers, identify the correct server per tool/request, and route calls through simple configuration.
2. Configurable observability and logging abstraction:
	- Add LangFuse and database logging support behind an abstraction layer so each provider can be enabled, disabled, or swapped using configuration.

## License

This project is licensed under the MIT License. See `LICENSE`.

For dependency license context, see `THIRD_PARTY_NOTICES.md`.

## Maintainers

- Prajakt Thale
- Krunal Tadwala
- Organization: CodeYogee-Labs (https://github.com/CodeYogee-Labs)
