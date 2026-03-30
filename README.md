# Synapse Notes

AI-powered note-taking app that automatically connects your notes using local Ollama embeddings and a visual knowledge graph.

## Stack

- **Frontend**: Vanilla HTML / CSS / JS + D3.js
- **Backend**: Python + FastAPI + SQLite
- **AI**: Ollama (`nomic-embed-text` for embeddings)
- **Hosting**: Docker on Oracle Cloud VPS

## Prerequisites

- Docker + Docker Compose
- Ollama running with `nomic-embed-text` pulled

```bash
ollama pull nomic-embed-text
```

## Run locally

```bash
git clone https://github.com/sneakyturtle270508/synapse-notes
cd synapse-notes
docker compose up --build
```

Open http://localhost:8000

## Run on Oracle Cloud VPS

1. SSH into your VPS and clone the repo
2. Make sure Ollama is running on the VPS (or set `OLLAMA_URL` to point to your home server via ngrok)
3. Run:

```bash
docker compose up -d --build
```

4. Set up a reverse proxy (nginx) to expose port 8000

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://host.docker.internal:11434` | Ollama API base URL |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model name |
| `LINK_THRESHOLD` | `0.78` | Cosine similarity threshold for auto-linking (0–1) |

## How it works

1. You write a note and save (auto-saves after 1.2s idle)
2. FastAPI sends the note text to Ollama `/api/embeddings`
3. The embedding vector is stored in SQLite
4. Cosine similarity is computed against all other notes
5. Notes above the threshold get a link created in the `links` table
6. The graph view renders all notes as nodes with edges for each link
7. The editor shows connected notes as chips at the bottom

## API endpoints

```
GET    /api/notes                   List all notes
POST   /api/notes                   Create note
PUT    /api/notes/:id               Update note
DELETE /api/notes/:id               Delete note
GET    /api/graph                   Get all nodes + links for graph
GET    /api/notes/:id/connections   Get connected notes for a note
```

## Adjust sensitivity

If links are too aggressive, raise `LINK_THRESHOLD` (e.g. `0.85`).
If notes aren't connecting enough, lower it (e.g. `0.72`).
