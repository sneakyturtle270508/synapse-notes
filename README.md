# Synapse Notes

AI-powered note-taking app that automatically connects your notes using semantic embeddings and a visual knowledge graph.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green) ![D3.js](https://img.shields.io/badge/D3.js-v7-orange)

## Features

- **Smart Linking** - Notes connect automatically based on semantic similarity
- **Knowledge Graph** - Interactive D3.js visualization of your notes
- **AI Categorization** - Automatic topic clustering with color coding
- **Real-time Updates** - Links recalculate on every save
- **Path Finding** - Discover connections between any two notes
- **Self-hosted** - Runs entirely on your machine with Ollama

## Quick Start

### Prerequisites

- Python 3.9+
- Ollama installed

### Setup

```bash
# 1. Pull the embedding model
ollama pull nomic-embed-text

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Start Ollama (if not running)
ollama serve

# 4. Run the server
uvicorn main:app --reload
```

Open http://localhost:8000

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Write Note │ ──► │ AI Embedding│ ──► │   SQLite    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  D3.js      │ ◄── │  Similarity │ ◄── │  Cosine Sim │
│  Graph View │     │  Threshold  │     │  Calculation│
└─────────────┘     └─────────────┘     └─────────────┘
```

1. You write a note
2. Ollama generates semantic embedding
3. Similarity calculated against all other notes
4. Notes above threshold get linked
5. Graph view updates in real-time

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes` | List all notes |
| POST | `/api/notes` | Create note |
| PUT | `/api/notes/:id` | Update note |
| DELETE | `/api/notes/:id` | Delete note |
| GET | `/api/graph` | Get graph nodes + links |
| GET | `/api/graph/version` | Graph version (for polling) |
| GET | `/api/notes/:id/connections` | Get related notes |
| GET | `/api/path?source=X&target=Y` | Find shortest path |
| POST | `/api/recluster` | Re-run clustering |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API URL |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `CHAT_MODEL` | `qwen2.5:7b` | Chat model for categorization |
| `LINK_THRESHOLD` | `0.65` | Similarity threshold (0-1) |

## Docker Deployment

```bash
docker compose up --build
```

## Project Structure

```
synapse-notes/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── requirements.txt
│   └── synapse.db       # SQLite database
├── frontend/
│   ├── index.html
│   └── static/
│       ├── style.css
│       └── app.js
├── docker-compose.yml
├── Dockerfile
├── README.md
└── PROJECT.md            # Presentation outline
```

## Configuration Tips

- **Too many links?** Raise `LINK_THRESHOLD` to 0.75-0.85
- **Not enough links?** Lower `LINK_THRESHOLD` to 0.55-0.65
- **Want faster embeddings?** Use a smaller model like `all-minilm`

## Tech Details

- **Similarity**: Cosine similarity between 768-dim vectors
- **Clustering**: Greedy algorithm with configurable threshold
- **Auto-save**: 1.2 second idle debounce
- **Database**: SQLite with cascading deletes

## Contributing

Pull requests welcome! Please read the code style and ensure tests pass.

## License

MIT

## Author

Made with Python, FastAPI, D3.js, and Ollama
