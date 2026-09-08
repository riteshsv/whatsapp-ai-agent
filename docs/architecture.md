# System Architecture: WhatsApp AI Agent Middleware

This document provides a detailed overview of the system architecture, data flow, component layout, and security considerations for the **`WhatsApp-ai-agent`** project.

---

## 1. High-Level Architecture Diagram

```
                                    EXTERNAL SERVICES
 ┌─────────────────┐       ┌────────────────────────────────┐       ┌─────────────────┐
 │ Customer Phone  │ ────> │  Meta WhatsApp Business API    │ ────> │ FastAPI Server  │
 │  (WhatsApp App) │ <──── │   (Webhooks & Graph API)       │ <──── │   (via ngrok)   │
 └─────────────────┘       └────────────────────────────────┘       └────────┬────────┘
                                                                             │
                                                                             ▼
                                                                  INTERNAL APP LAYERS
                                                                    ┌─────────────────┐
                                                                    │   config.py     │
                                                                    │ (Pydantic Env)  │
                                                                    └────────┬────────┘
                                                                             │
                                                                             ▼
                                                                    ┌─────────────────┐
                                                                    │    main.py      │
                                                                    │ (POST /webhook) │
                                                                    └────────┬────────┘
                                                                             │
                                              ┌──────────────────────────────┴──────────────────────────────┐
                                              ▼                                                             ▼
                                   ┌──────────────────────┐                                              ┌──────────────────────┐
                                   │ services/agent.py    │                                      │ services/whatsapp.py │
                                   │  (OpenAI GPT-4o)     │                                      │ (Send /messages API) │
                                   └──────────────────────┘                                      └──────────────────────┘
```

---

## 2. Directory & Component Structure

The application follows a modular layout managed with `uv`:

```text
WhatsApp-ai-agent/
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI pipeline
├── demo/
│   └── sample_webhook_payload.json    # Mock Meta webhook payload for local testing
├── src/
│   └── whatsapp_ai_agent/             # Core Python package
│       ├── __init__.py
│       ├── main.py                    # FastAPI application & HTTP endpoint routing
│       ├── config.py                  # Environment settings & credentials validation
│       ├── services/                  # Core domain logic
│       │   ├── whatsapp.py            # Meta Graph API HTTP client
│       │   └── agent.py               # OpenAI LLM integration & prompt processing
│       └── models/                    # Data schemas
│           └── webhook.py             # Pydantic models for incoming WhatsApp events
├── .env.example                       # Environment template
├── .gitignore                         # Git exclusion rules
├── .python-version                    # Pinned Python version (3.12+)
├── pyproject.toml                     # Project dependencies and tool configurations
├── uv.lock                            # Deterministic dependency lockfile
├── architecture.md                    # System architecture documentation
└── README.md                          # Repository guide
```

---

## 3. Step-by-Step Data Flow

1. **Webhook Handshake & Verification (`GET /webhook`)**
   - Meta sends a verification request with a challenge parameter (`hub.challenge`) and verify token (`hub.verify_token`).
   - `main.py` validates the token against `META_VERIFY_TOKEN` defined in `config.py`.

2. **Inbound Event Processing (`POST /webhook`)**
   - When a user sends a message, Meta issues an HTTP `POST` payload.
   - Pydantic models in `models/webhook.py` validate the event payload.
   - Non-message events (e.g., status updates like "read" or "delivered") are acknowledged and discarded.

3. **AI Generation (`services/agent.py`)**
   - The user's text message is extracted and sent to the OpenAI API client (`gpt-4o-mini` or specified model).
   - The system prompt enforces tone, length, and support guidelines.

4. **Outbound Dispatch (`services/whatsapp.py`)**
   - The response text is packaged into Meta's `/messages` standard JSON schema.
   - An asynchronous HTTP client (`httpx`) posts the response back to Meta's Graph API.

---

## 4. Environment & Security Management

- **Environment Variables:** All secrets (`META_ACCESS_TOKEN`, `OPENAI_API_KEY`, `META_VERIFY_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`) are managed via Pydantic Settings (`config.py`).
- **Dependencies & Environment Isolation:** Managed cleanly with **`uv`**, locking exact package hashes in `uv.lock`.
