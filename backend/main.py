from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3, json, httpx, math, os, time, asyncio, heapq, re
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
LINK_THRESHOLD = float(os.getenv("LINK_THRESHOLD", "0.65"))

PALETTE = [
    "#4a90d9", "#a8c44e", "#9b7fd4", "#d4a017",
    "#4ecdc4", "#f7a35c", "#e05c5c", "#e07cb5",
    "#5cc8e0", "#d4724a", "#7dd48a", "#c4a44e",
]
CATEGORY_COLOR_MAP: dict[str, str] = {}
STOP_WORDS = {
    "the", "and", "for", "that", "with", "this", "from", "your", "you", "are", "was",
    "were", "have", "has", "had", "not", "but", "about", "into", "over", "under", "then",
    "than", "like", "just", "they", "them", "their", "will", "would", "could", "should",
    "can", "its", "it's", "our", "out", "very", "more", "most", "some", "many", "much",
    "what", "when", "where", "which", "while", "also", "only", "because", "been", "being",
    "a", "an", "to", "of", "in", "on", "at", "is", "it", "as", "by", "or", "if"
}

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
    if "labels" not in cols:
        conn.execute("ALTER TABLE notes ADD COLUMN labels TEXT")
        conn.commit()
    conn.close()


migrate_db()


async def classify_note(text: str) -> str:
    clean = text.strip()
    if len(clean) < 15:
        return "other"

    prompt = f"""You are tagging a personal note with a short topic label.

Note:
{clean[:600]}

What is this note ACTUALLY about? Give a specific 1-3 word label in lowercase.
- "css styling" not "technology"
- "strength training" not "health"
- "trip planning" not "travel"
- "python scripting" not "coding"

Reply with ONLY the label. Nothing else."""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": CHAT_MODEL,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": "Reply with only a short lowercase topic label. No punctuation, no explanation."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            resp.raise_for_status()
            raw = resp.json()["message"]["content"].strip().lower()
            label = raw.split("\n")[0].strip().rstrip(".,!?\"'")
            label = " ".join(label.split()[:3])
            return label if label else "other"
    except Exception as e:
        print(f"Classify error: {e}")
    return "other"


async def reclassify_cluster(note_ids: list[int], titles_contents: list[str]) -> str:
    """Given a cluster of related notes, ask AI for one consistent category label."""
    notes_text = "\n".join(f"- {t[:200]}" for t in titles_contents[:10])
    prompt = f"""These notes are semantically related to each other. Give them ONE shared category label.

Notes in this cluster:
{notes_text}

Rules:
- 1-3 words, lowercase only
- Pick the label that best describes what ALL these notes have in common
- Be specific: "frontend development" not "tech", "strength training" not "health"
- Reply with ONLY the label, nothing else"""

    try:
        async with httpx.AsyncClient(timeout=40) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": CHAT_MODEL,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": "Reply with only a short lowercase category label. No explanation."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            resp.raise_for_status()
            raw = resp.json()["message"]["content"].strip().lower()
            label = raw.split("\n")[0].strip().rstrip(".,!?\"'")
            label = " ".join(label.split()[:3])
            return label if label else "other"
    except Exception as e:
        print(f"Reclassify cluster error: {e}")
    return "other"


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x ** 2 for x in a))
    mag_b = math.sqrt(sum(x ** 2 for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def stem_word(word: str) -> str:
    w = word.lower().strip()
    if len(w) <= 3:
        return w
    if w.endswith("ing") and len(w) > 5:
        w = w[:-3]
        if len(w) >= 2 and w[-1] == w[-2]:
            w = w[:-1]
    elif w.endswith("ed") and len(w) > 4:
        w = w[:-2]
    elif w.endswith("es") and len(w) > 4:
        w = w[:-2]
    elif w.endswith("s") and len(w) > 3:
        w = w[:-1]
    if w.endswith("i") and len(w) > 3:
        w = w[:-1] + "y"
    return w


def extract_labels(text: str, limit: int = 8) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]+", text.lower())
    counts: dict[str, int] = {}
    for raw in words:
        if raw in STOP_WORDS:
            continue
        token = stem_word(raw)
        if len(token) < 3 or token in STOP_WORDS:
            continue
        counts[token] = counts.get(token, 0) + 1

    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [w for w, _ in ranked[:limit]]


def build_label_links(notes_rows: list[sqlite3.Row], min_overlap: int = 1) -> list[dict]:
    note_labels: dict[int, set[str]] = {}
    for row in notes_rows:
        try:
            parsed = json.loads(row["labels"] or "[]")
            labels = {stem_word(x) for x in parsed if isinstance(x, str)}
        except Exception:
            labels = set()
        note_labels[row["id"]] = labels

    links: list[dict] = []
    ids = [row["id"] for row in notes_rows]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            overlap = note_labels[a].intersection(note_labels[b])
            if len(overlap) < min_overlap:
                continue
            score = min(0.9, 0.5 + 0.1 * len(overlap))
            links.append({
                "source": min(a, b),
                "target": max(a, b),
                "score": round(score, 4),
                "same_label": True,
                "shared_labels": sorted(overlap)[:3]
            })
    return links


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


def build_clusters(notes_with_embeddings: list[dict], threshold: float = 0.72) -> list[list[int]]:
    """Greedy clustering — group notes that are similar to each other."""
    ids = [n["id"] for n in notes_with_embeddings]
    embs = [json.loads(n["embedding"]) for n in notes_with_embeddings]
    n = len(ids)

    visited = set()
    clusters = []

    for i in range(n):
        if ids[i] in visited:
            continue
        cluster = [ids[i]]
        visited.add(ids[i])
        for j in range(n):
            if ids[j] in visited:
                continue
            if cosine_similarity(embs[i], embs[j]) >= threshold:
                cluster.append(ids[j])
                visited.add(ids[j])
        clusters.append(cluster)

    return clusters


_recluster_lock = asyncio.Lock()
_graph_version = 0

async def auto_recluster():
    """Runs in background after every save — reclusters all notes silently."""
    if _recluster_lock.locked():
        return
    async with _recluster_lock:
        try:
            conn = get_db()
            rows = conn.execute(
                "SELECT id, title, content, embedding FROM notes WHERE embedding IS NOT NULL"
            ).fetchall()
            conn.close()

            if len(rows) < 2:
                return

            # Filter out stub notes with no real content
            notes_data = [
                dict(r) for r in rows
                if len((r["title"] + " " + r["content"]).strip()) > 20
                and r["title"].lower() not in ("new note", "untitled", "test", "")
            ]

            if len(notes_data) < 1:
                return
            clusters = build_clusters(notes_data, threshold=LINK_THRESHOLD)
            note_lookup = {r["id"]: f"{r['title']}\n{r['content']}" for r in notes_data}

            CATEGORY_COLOR_MAP.clear()

            for cluster in clusters:
                texts = [note_lookup[nid] for nid in cluster if nid in note_lookup]
                if len(cluster) == 1:
                    label = await classify_note(texts[0] if texts else "")
                else:
                    label = await reclassify_cluster(cluster, texts)

                color = get_category_color(label)
                conn = get_db()
                for nid in cluster:
                    conn.execute(
                        "UPDATE notes SET category=?, color=? WHERE id=?",
                        (label, color, nid)
                    )
                # Force-link all notes in the same cluster
                for i in range(len(cluster)):
                    for j in range(i + 1, len(cluster)):
                        a, b = cluster[i], cluster[j]
                        # Calculate actual score if both have embeddings, else use minimum threshold
                        try:
                            ea = json.loads(note_lookup.get(a, "") or "{}")
                            eb = json.loads(note_lookup.get(b, "") or "{}")
                        except Exception:
                            ea, eb = None, None
                        # Use stored embeddings for score
                        score = LINK_THRESHOLD  # fallback
                        try:
                            emb_a = next(n["embedding"] for n in notes_data if n["id"] == a)
                            emb_b = next(n["embedding"] for n in notes_data if n["id"] == b)
                            score = round(cosine_similarity(json.loads(emb_a), json.loads(emb_b)), 4)
                        except Exception:
                            pass
                        conn.execute(
                            "INSERT OR REPLACE INTO links (source_id, target_id, score) VALUES (?,?,?)",
                            (min(a, b), max(a, b), max(score, LINK_THRESHOLD))
                        )
                conn.commit()
                conn.close()
                print(f"[recluster] {cluster} -> '{label}'")
            global _graph_version
            _graph_version += 1
        except Exception as e:
            print(f"[recluster] error: {e}")


class NoteCreate(BaseModel):
    title: str
    content: str = ""


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@app.get("/api/notes")
def list_notes():
    conn = get_db()
    notes = conn.execute(
        "SELECT id, title, content, color, category, labels, created_at, updated_at FROM notes ORDER BY updated_at DESC"
    ).fetchall()
    conn.close()
    out = []
    for n in notes:
        row = dict(n)
        row["labels"] = json.loads(row["labels"]) if row.get("labels") else []
        out.append(row)
    return out


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
    labels = extract_labels(text)
    category, embedding = await asyncio.gather(classify_note(text), get_embedding(text))
    color = get_category_color(category)

    conn = get_db()
    conn.execute(
        "UPDATE notes SET category=?, color=?, embedding=?, labels=? WHERE id=?",
        (category, color, json.dumps(embedding) if embedding else None, json.dumps(labels), note_id)
    )
    conn.commit()
    conn.close()

    if embedding:
        await recompute_links(note_id, embedding)
        asyncio.create_task(auto_recluster())

    return {"id": note_id, "color": color, "category": category, "labels": labels}


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
    labels = extract_labels(text)
    category, embedding = await asyncio.gather(classify_note(text), get_embedding(text))
    color = get_category_color(category)

    conn = get_db()
    conn.execute(
        "UPDATE notes SET category=?, color=?, embedding=?, labels=? WHERE id=?",
        (category, color, json.dumps(embedding) if embedding else None, json.dumps(labels), note_id)
    )
    conn.commit()
    conn.close()

    if embedding:
        await recompute_links(note_id, embedding)
        asyncio.create_task(auto_recluster())

    return {"ok": True, "color": color, "category": category, "labels": labels}


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/api/graph/version")
def graph_version():
    return {"version": _graph_version}


@app.get("/api/graph")
def get_graph():
    conn = get_db()
    notes = conn.execute("SELECT id, title, color, category, labels FROM notes").fetchall()
    links = conn.execute("SELECT source_id, target_id, score FROM links").fetchall()
    label_links = build_label_links(notes)
    conn.close()
    existing = {(min(l["source_id"], l["target_id"]), max(l["source_id"], l["target_id"])) for l in links}
    merged_links = [{"source": l["source_id"], "target": l["target_id"], "score": l["score"]} for l in links]
    for ll in label_links:
        key = (ll["source"], ll["target"])
        if key in existing:
            continue
        merged_links.append(ll)
    return {
        "nodes": [{"id": n["id"], "title": n["title"], "color": n["color"], "category": n["category"]} for n in notes],
        "links": merged_links
    }


@app.get("/api/notes/{note_id}/connections")
def get_connections(note_id: int):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT n.id, n.title, n.color, l.score
        FROM links l
        JOIN notes n ON (n.id = CASE WHEN l.source_id=? THEN l.target_id ELSE l.source_id END)
        WHERE l.source_id=? OR l.target_id=?
        ORDER BY l.score DESC
        """,
        (note_id, note_id, note_id),
    ).fetchall()

    note_row = conn.execute("SELECT category, labels FROM notes WHERE id=?", (note_id,)).fetchone()
    note_labels = set()
    if note_row and note_row["labels"]:
        try:
            note_labels = {stem_word(x) for x in json.loads(note_row["labels"]) if isinstance(x, str)}
        except Exception:
            note_labels = set()

    label_matches = []
    if note_labels:
        candidates = conn.execute(
            """
            SELECT id, title, color, labels
            FROM notes
            WHERE id!=?
            ORDER BY updated_at DESC
            LIMIT 200
            """,
            (note_id,),
        ).fetchall()
        for c in candidates:
            try:
                labels = {stem_word(x) for x in json.loads(c["labels"] or "[]") if isinstance(x, str)}
            except Exception:
                labels = set()
            overlap = sorted(note_labels.intersection(labels))
            if overlap:
                label_matches.append({
                    "id": c["id"],
                    "title": c["title"],
                    "color": c["color"],
                    "score": 0.0,
                    "same_label": True,
                    "shared_labels": overlap[:3]
                })
    conn.close()

    connected = [dict(r) for r in rows]
    existing_ids = {r["id"] for r in connected}
    non_duplicate_label_matches = [m for m in label_matches if m["id"] not in existing_ids]
    connected.extend(non_duplicate_label_matches)
    connected.sort(key=lambda x: x.get("score", 0), reverse=True)
    return connected


@app.get("/api/path")
def find_path(source: int, target: int):
    conn = get_db()
    note_rows = conn.execute("SELECT id, title, color, labels FROM notes").fetchall()
    notes = {r["id"]: {"title": r["title"], "color": r["color"]} for r in note_rows}
    links = conn.execute("SELECT source_id, target_id, score FROM links").fetchall()
    label_links = build_label_links(note_rows)
    conn.close()

    if source not in notes or target not in notes:
        return {"found": False, "path": []}

    if source == target:
        n = notes[source]
        return {"found": True, "path": [{"id": source, "title": n["title"], "color": n["color"]}]}

    graph: dict[int, list[tuple[int, float]]] = {nid: [] for nid in notes}
    for l in links:
        s, t, sc = l["source_id"], l["target_id"], l["score"]
        w = 1.0 - sc
        graph[s].append((t, w))
        graph[t].append((s, w))
    existing = {(min(l["source_id"], l["target_id"]), max(l["source_id"], l["target_id"])) for l in links}
    for l in label_links:
        key = (l["source"], l["target"])
        if key in existing:
            continue
        s, t, sc = l["source"], l["target"], l["score"]
        w = 1.0 - sc
        graph[s].append((t, w))
        graph[t].append((s, w))

    dist = {nid: float("inf") for nid in notes}
    prev: dict[int, Optional[int]] = {nid: None for nid in notes}
    dist[source] = 0.0
    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == target:
            break
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    if dist[target] == float("inf"):
        return {"found": False, "path": []}

    path = []
    cur: Optional[int] = target
    while cur is not None:
        n = notes[cur]
        path.append({"id": cur, "title": n["title"], "color": n["color"]})
        cur = prev[cur]
    path.reverse()

    return {"found": True, "path": path, "hops": len(path) - 1}


@app.post("/api/recluster")
async def recluster():
    """
    Re-clusters all notes by embedding similarity and gives each cluster
    a consistent AI-generated category label.
    """
    conn = get_db()
    rows = conn.execute(
        "SELECT id, title, content, embedding FROM notes WHERE embedding IS NOT NULL"
    ).fetchall()
    conn.close()

    if not rows:
        return {"updated": 0, "clusters": 0}

    notes_data = [dict(r) for r in rows]
    clusters = build_clusters(notes_data, threshold=LINK_THRESHOLD)
    note_lookup = {r["id"]: f"{r['title']}\n{r['content']}" for r in notes_data}

    updated = 0
    # Reset color map so clusters get fresh consistent colors
    CATEGORY_COLOR_MAP.clear()

    for cluster in clusters:
        texts = [note_lookup[nid] for nid in cluster if nid in note_lookup]

        if len(cluster) == 1:
            label = await classify_note(texts[0] if texts else "")
        else:
            label = await reclassify_cluster(cluster, texts)

        color = get_category_color(label)

        conn = get_db()
        for nid in cluster:
            conn.execute(
                "UPDATE notes SET category=?, color=? WHERE id=?",
                (label, color, nid)
            )
        conn.commit()
        conn.close()
        updated += len(cluster)
        print(f"Cluster {cluster} → '{label}' ({color})")

    return {"updated": updated, "clusters": len(clusters)}


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
