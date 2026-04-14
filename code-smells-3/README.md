# Chat API (`code-smells-3`)

FastAPI + Beanie service for collaborative chat threads.

## Context

**Collaborative threaded chat API** backed by MongoDB. A thread stores **`participant_user_ids`** and an embedded **`messages`** list on the same document. Each message is either a **user** line (with **`author_user_id`**) or an **assistant** line (no author id). The LLM runs when the client sets **`request_llm_reply: true`** on `POST .../messages`; the JSON response includes **`assistant_reply_appended`** so callers can see whether an assistant turn was stored. Attachments require **`request_llm_reply`**. **`GET /health`** supports ops checks. The stack uses application, domain, and repository layers.

Request and response models live under [`app/schemas/`](app/schemas/) (`chat_requests.py`, `chat_responses.py`, `health.py`).

## Run

1. `docker compose up -d`
2. Copy `.env.example` to `.env` if needed.
3. `uvicorn app.main:app --reload`

OpenAPI: http://127.0.0.1:8000/docs

