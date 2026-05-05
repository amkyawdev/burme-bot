# Burme AI

Burme AI is a Myanmar-first intelligent assistant built for fast chat, code help, translation, explanation, and streaming AI responses.

## Overview

Burme AI is designed as a clean, modern web app with a dark gold UI and an AI backend powered by HuggingFace. The project is structured for frontend deployment on Vercel and API deployment on a server/worker layer.

## Key Features

- Myanmar-first assistant experience
- Streaming AI responses with SSE
- Multi-mode assistant workflow
  - Chat
  - Code
  - Translate
  - Explain
- Prompt-driven AI behavior via skill prompts
- PWA-ready frontend with custom favicon and manifest
- Vercel deployment support

## Tech Stack

- Frontend: Vite, React, TypeScript, Tailwind CSS
- Routing: Wouter
- Data: TanStack React Query
- API: Express-based server
- AI Model: HuggingFace `amkyawdev/kyaw-mm-v1`

## Project Structure

```text
artifacts/burme-ai/      # Frontend app
artifacts/api-server/    # API server
lib/api-spec/            # OpenAPI contract and generated clients
lib/api-zod/             # Generated Zod schemas
```

## Local Development

### Frontend

```bash
pnpm --filter @workspace/burme-ai run dev
```

### API Server

```bash
pnpm --filter @workspace/api-server run dev
```

## Deployment

### Vercel

This app includes `vercel.json` for SPA routing.

### PWA Assets

- `artifacts/burme-ai/public/favicon.svg`
- `artifacts/burme-ai/public/manifest.webmanifest`

## Environment Variables

Required for AI features:

- `HUGGINGFACE_API_TOKEN`

## Notes

- The frontend uses the artifact base path so it works correctly in Replit and in production.
- The AI backend is contract-first and uses generated schemas from the OpenAPI spec.
