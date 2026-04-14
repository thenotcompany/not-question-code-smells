# Catalog API (`code-smells-1`)

FastAPI + Beanie + MongoDB service.

## Context

This is a fragment of a small **catalog + orders** API: **products** are stored in MongoDB (name, SKU, base price, product type such as one-time, subscription, or add-on), clients can request an **order quote** from a cart-style payload (line items, customer email, region-aware tax and shipping-style totals), then **place** an order and **fetch** it by id.

## Run

1. `docker compose up -d`
2. Set `MONGODB_URL` and `DATABASE_NAME` in your environment (see `.env.example`).
3. From this directory: `uvicorn app.main:app --reload`

OpenAPI: http://127.0.0.1:8000/docs
