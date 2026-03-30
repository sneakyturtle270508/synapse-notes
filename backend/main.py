from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3, json, httpx, math, os, time, asyncio
from pathlib import Path

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = str(BASE_DIR / "synapse.db")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen2.5:7b")
LINK_THRESHOLD = float(os.getenv("LINK_THRESHOLD", "0.78"))

# Colors are assigned dynamically per unique category label
PALETTE = [
    "#4a90d9", "#a8c44e", "#9b7fd4", "#d4a017",
    "#4ecdc4", "#f7a35c", "#e05c5c", "#e07cb5",
    "#5cc8e0", "#d4724a", "#7dd48a", "#c4a44e",
]
CATEGORY_COLOR_MAP: dict[str, str] = {}

def get_category_color(category: str) -> str:
    if category not in CATEGORY_COLOR_MAP:
        CATEGORY_COLOR_MAP[category] = PALETTE[len(CATEGORY_COLOR_MAP) % len(PALETTE)]
    return CATEGORY_COLOR_MAP[category]


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            color TEXT NOT NULL DEFAULT '#888888',
            category TEXT NOT NULL DEFAULT 'other',
            embedding TEXT,
            created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            score REAL NOT NULL,
            UNIQUE(source_id, target_id),
            FOREIGN KEY(source_id) REFERENCES notes(id) ON DELETE CASCADE,
            FOREIGN KEY(target_id) REFERENCES notes(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


init_db()


def migrate_db():
    conn = get_db()
    cols = [r[1] for r in conn.execute("PRAGMA table_info(notes)").fetchall()]
    if "category" not in cols:
        conn.execute("ALTER TABLE notes ADD COLUMN category TEXT NOT NULL DEFAULT 'other'")
        conn.commit()
    conn.close()


migrate_db()


async def classify_note(text: str) -> str:
    prompt = f"""Read this note and invent a short 1-2 word category label that best describes its topic.

Note:
{text[:600]}

Rules:
- Reply with ONLY the category label, nothing else
- Use lowercase, no punctuation
- Be specific: prefer "css styling" over "tech", "weight training" over "health"
- Examples of good labels: "web development", "machine learning", "personal finance", "meal planning", "creative writing", "python scripting"
- Invent the best label for this specific note"""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={{
                    "model": CHAT_MODEL,
                    "stream": False,
                    "messages": [
                        {{"role": "system", "content": "You are a precise note classifier. Reply with only a short category label, nothing else."}},
                        {{"role": "user", "content": prompt}}
                    ]
                }}
            )
            resp.raise_for_status()
            raw = resp.json()["message"]["content"].strip().lower()
            # keep only first line, strip punctuation
            label = raw.split("\n")[0].strip().rstrip(".,!?")
            # max 3 words
            label = " ".join(label.split()[:3])
            return label if label else "other"
    except Exception as e:
        print(f"Classify error: {e}")
    return "other"


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x ** 2 for x in a))
    mag_b = math.sqrt(sum(x ** 2 for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


async def get_embedding(text: str) -> Optional[list[float]]:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": EMBED_MODEL, "prompt": text}
            )
            resp.raise_for_status()
            return resp.json()["embedding"]
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


async def recompute_links(note_id: int, embedding: list[float]):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, embedding FROM notes WHERE id != ? AND embedding IS NOT NULL",
        (note_id,)
    ).fetchall()

    conn.execute("DELETE FROM links WHERE source_id=? OR target_id=?", (note_id, note_id))

    for row in rows:
        other_emb = json.loads(row["embedding"])
        score = cosine_similarity(embedding, other_emb)
        if score >= LINK_THRESHOLD:
            try:
                conn.execute(
                    "INSERT OR REPLACE INTO links (source_id, target_id, score) VALUES (?,?,?)",
                    (min(note_id, row["id"]), max(note_id, row["id"]), round(score, 4))
                )
            except Exception:
                pass

    conn.commit()
    conn.close()


COLORS = ["#e05c5c", "#4a90d9", "#a8c44e", "#d4a017", "#9b7fd4", "#4ecdc4", "#f7a35c"]


class NoteCreate(BaseModel):
    title: str
    content: str = ""


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@app.get("/api/notes")
def list_notes():
    conn = get_db()
    notes = conn.execute("SELECT id, title, content, color, category, created_at, updated_at FROM notes ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(n) for n in notes]


@app.post("/api/notes")
async def create_note(data: NoteCreate):
    now = int(time.time())

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO notes (title, content, color, category, created_at, updated_at) VALUES (?,?,?,?,?,?)",
        (data.title, data.content, "#888888", "other", now, now)
    )
    note_id = cur.lastrowid
    conn.commit()
    conn.close()

    text = f"{data.title}\n{data.content}".strip()

    category, embedding = await asyncio.gather(
        classify_note(text),
        get_embedding(text)
    )
    color = get_category_color(category)

    conn = get_db()
    conn.execute(
        "UPDATE notes SET category=?, color=?, embedding=? WHERE id=?",
        (category, color, json.dumps(embedding) if embedding else None, note_id)
    )
    conn.commit()
    conn.close()

    if embedding:
        await recompute_links(note_id, embedding)

    return {"id": note_id, "color": color, "category": category}


@app.put("/api/notes/{note_id}")
async def update_note(note_id: int, data: NoteUpdate):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    if not note:
        conn.close()
        raise HTTPException(404, "Note not found")

    title = data.title if data.title is not None else note["title"]
    content = data.content if data.content is not None else note["content"]
    now = int(time.time())

    conn.execute("UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?", (title, content, now, note_id))
    conn.commit()
    conn.close()

    text = f"{title}\n{content}".strip()

    category, embedding = await asyncio.gather(
        classify_note(text),
        get_embedding(text)
    )
    color = get_category_color(category)

    conn = get_db()
    conn.execute(
        "UPDATE notes SET category=?, color=?, embedding=? WHERE id=?",
        (category, color, json.dumps(embedding) if embedding else None, note_id)
    )
    conn.commit()
    conn.close()

    if embedding:
        await recompute_links(note_id, embedding)

    return {"ok": True, "color": color, "category": category}


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/api/graph")
def get_graph():
    conn = get_db()
    notes = conn.execute("SELECT id, title, color FROM notes").fetchall()
    links = conn.execute("SELECT source_id, target_id, score FROM links").fetchall()
    conn.close()
    return {
        "nodes": [dict(n) for n in notes],
        "links": [{"source": l["source_id"], "target": l["target_id"], "score": l["score"]} for l in links]
    }


@app.get("/api/notes/{note_id}/connections")
def get_connections(note_id: int):
    conn = get_db()
    rows = conn.execute("""
        SELECT n.id, n.title, n.color, l.score
        FROM links l
        JOIN notes n ON (n.id = CASE WHEN l.source_id=? THEN l.target_id ELSE l.source_id END)
        WHERE l.source_id=? OR l.target_id=?
        ORDER BY l.score DESC
    """, (note_id, note_id, note_id)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
