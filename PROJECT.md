# Synapse Notes

## AI-Powered Knowledge Graph for Note-Taking

---

## The Problem

- Notes pile up without connections
- Hard to find related ideas
- Knowledge becomes siloed
- Hard to see the "big picture"

---

## Our Solution

**Synapse Notes** automatically maps your knowledge

1. Write naturally
2. AI understands meaning
3. Connections appear automatically
4. Explore your knowledge visually

---

## How It Works

1. **Create** → Write any note
2. **Embed** → AI generates semantic vector
3. **Connect** → Similar notes auto-link
4. **Explore** → Interactive knowledge graph

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vanilla JS + D3.js |
| Backend | Python FastAPI |
| Database | SQLite |
| AI Engine | Ollama |
| Embeddings | nomic-embed-text |
| Chat Model | qwen2.5:7b |

---

## Key Features

- Auto-save with 1.2s idle delay
- Real-time semantic similarity
- Visual graph with D3.js
- AI-powered categorization
- Path finding between notes
- Cosine similarity scoring

---

## API Endpoints

```
POST /api/notes          Create note
GET  /api/graph          Get graph data
GET  /api/path?source=1&target=5  Find path
GET  /api/notes/:id/connections   Related notes
```

---

## Live Demo

- 52 connected notes
- 60+ semantic links
- Real-time clustering
- Interactive exploration

---

## Future Ideas

- Export to Obsidian/Miro
- Collaboration features
- Mobile app
- Custom embedding models
- Topic-based filtering

---

## Thank You

**GitHub:** github.com/sneakyturtle270508/synapse-notes

**Questions?**
