# Social posts & comments API (`code-smells-1`)

FastAPI + Beanie + MongoDB service.

## Context

This is an API for a social media app. Here we have **Posts** and **Comments** on those posts (many comments per post, stored in a separate collection). Consider there is not authentication layer.

## Run

1. `docker compose up -d`
2. Set `MONGODB_URL` and `DATABASE_NAME` in your environment (see `.env.example`).
3. From this directory: `uvicorn app.main:app --reload`

OpenAPI: http://127.0.0.1:8000/docs
