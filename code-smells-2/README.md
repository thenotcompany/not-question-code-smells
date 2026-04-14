# Ops console (`code-smells-2`)

Nuxt 3 + TypeScript web app.

## Context

Small **internal admin-style UI**: **Home** introduces the app, **Users** lists people from a Nitro **`/api/users`** route, **Dashboard** loads **`/api/projects`** with project rows and a **metric tile**, and **Team → member** shows another view backed by the same user API. Data is static JSON for local development.

## Run

```bash
npm install
npm run dev
```

Build:

```bash
npm run build
```
