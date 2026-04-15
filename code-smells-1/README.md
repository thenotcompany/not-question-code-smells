# Social posts & chat API (`code-smells-1`)

FastAPI + Beanie + MongoDB service.

## Context

This is an API for a social media app. Here we have **Posts** and **Direct chats** between two participants.

Create a post with **`GET /posts`** using `headline`, `handle`, and **`postType`** as a single letter: **`i`**, **`t`**, or **`v`** (default **`t`**). Each is stored as **`image`**, **`text`**, or **`video`** respectively.

## Run

1. `docker compose up -d`
2. Set `MONGODB_URL` and `DATABASE_NAME` in your environment (see `.env.example`).
3. From this directory: `uvicorn app.main:app --reload`

OpenAPI: http://127.0.0.1:8000/docs
