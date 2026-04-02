# Synapse Notes

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Solution Overview](#solution-overview)
4. [Features and Capabilities](#features-and-capabilities)
5. [Technical Architecture](#technical-architecture)
6. [System Requirements](#system-requirements)
7. [Installation Guide](#installation-guide)
8. [Configuration](#configuration)
9. [API Documentation](#api-documentation)
10. [Frontend Guide](#frontend-guide)
11. [Database Schema](#database-schema)
12. [AI and Machine Learning](#ai-and-machine-learning)
13. [Graph Visualization](#graph-visualization)
14. [Docker Deployment](#docker-deployment)
15. [Troubleshooting](#troubleshooting)
16. [Development Guide](#development-guide)
17. [Performance Optimization](#performance-optimization)
18. [Security Considerations](#security-considerations)
19. [Use Cases](#use-cases)
20. [FAQ](#faq)
21. [Contributing](#contributing)
22. [Roadmap](#roadmap)
23. [Changelog](#changelog)
24. [License](#license)
25. [Acknowledgments](#acknowledgments)
26. [Contact and Support](#contact-and-support)

---

## Introduction

Synapse Notes represents a paradigm shift in personal knowledge management. Traditional note-taking applications treat each note as an isolated entity, forcing users to manually create links, tags, and folders to establish relationships between their thoughts. This approach fails to capture the inherent interconnected nature of human knowledge and ideas.

Synapse Notes solves this fundamental problem by leveraging artificial intelligence to automatically discover and visualize connections between your notes. Every time you write or update a note, the system generates a semantic embedding that captures the meaning of your text, then compares it against all other notes in your collection to find meaningful relationships.

The result is a dynamic knowledge graph that grows and evolves with your thinking. Instead of spending time organizing notes into rigid hierarchies, you can focus on capturing ideas while Synapse handles the relationship mapping automatically.

This comprehensive documentation covers every aspect of Synapse Notes, from initial setup and configuration to advanced customization and deployment. Whether you're a developer looking to extend the application, a researcher exploring knowledge management tools, or a curious user wanting to understand how it all works, this guide provides the information you need.

### What Makes Synapse Notes Different

Unlike conventional note-taking apps that rely on manual tagging and linking, Synapse Notes employs sophisticated natural language processing to understand the semantic meaning behind your words. The system recognizes that two notes discussing related concepts should be connected, even if they use different vocabulary or come from different contexts.

For example, a note about "neural networks" and another about "backpropagation" would automatically be linked because they share conceptual territory in the machine learning domain. Similarly, a note about "healthy eating" might connect to one about "weight management" because the underlying topics are related, even if the specific words don't match exactly.

This semantic understanding enables a more natural, flowing workflow where you can focus on thinking and writing while the system builds the connections between your ideas automatically.

---

## Problem Statement

Modern knowledge workers face unprecedented challenges in managing information. The exponential growth of digital content, combined with the fragmentation of attention across multiple platforms and projects, creates a situation where valuable insights are easily lost in the noise.

Traditional note-taking approaches suffer from several critical limitations that prevent users from fully leveraging their accumulated knowledge.

### The Isolation Problem

Most note-taking applications treat each note as an independent unit. While tags and folders provide some organization, they require constant manual maintenance and often lead to inconsistent categorization. A note about "machine learning" might be tagged as "AI," "technology," "data science," or any number of other labels depending on the user's mood or context at the time of creation.

This isolation prevents users from discovering unexpected connections between their notes. An insight from a psychology note might have profound implications for a software architecture discussion, but without explicit linking, these connections remain invisible.

### The Organization Trap

The need to organize notes into meaningful structures creates a cognitive burden that interrupts the creative flow. Users must constantly decide where a new note belongs, which folder to place it in, and what tags to apply. This decision fatigue accumulates over time, leading to inconsistent organization and, eventually, abandoned note-taking systems altogether.

### The Scale Problem

As note collections grow, manual linking becomes impractical. With hundreds or thousands of notes, the manual effort required to establish and maintain connections exceeds what any user can sustain. The result is a graveyard of disconnected notes that once seemed important but can no longer be found or understood in context.

### The Context Loss

Notes taken in specific contexts—during a meeting, while reading a book, or in the middle of a coding session—lose that contextual information over time. Without external references to anchor them, isolated notes become increasingly difficult to understand and use effectively.

---

## Solution Overview

Synapse Notes addresses these challenges through a fundamentally different approach to knowledge management. Instead of requiring users to manually create and maintain connections, the system uses artificial intelligence to automatically discover relationships between notes based on semantic similarity.

The core workflow is simple and intuitive. Users write notes in natural language, and the system handles everything else: generating embeddings, computing similarities, creating connections, and visualizing the resulting knowledge graph.

### Key Principles

Several guiding principles shape the design and development of Synapse Notes:

**Automatic is Better than Manual.** The system should require as little manual intervention as possible. Users write; the system connects. This philosophy extends to auto-save, auto-categorization, and auto-linking.

**Semantic over Syntactic.** Connections should be based on meaning, not just keyword matching. Two notes that discuss the same concepts should be linked regardless of the specific words used.

**Visual over List-based.** The knowledge graph provides a more intuitive view of a note collection than traditional list or folder-based interfaces. Patterns and clusters emerge naturally in visual form.

**Local over Cloud.** Synapse Notes runs entirely on the user's machine, giving them full control over their data. No cloud dependency means no subscription fees, no privacy concerns, and no risk of service discontinuation.

**Simple over Complex.** The interface prioritizes simplicity and usability. Advanced features should be discoverable but not overwhelming. The common case—writing and viewing notes—should require minimal friction.

---

## Features and Capabilities

Synapse Notes provides a comprehensive set of features designed to enhance personal knowledge management through automated connection discovery.

### Automatic Note Linking

The core feature of Synapse Notes is automatic link creation. When a note is created or updated, the system generates a semantic embedding and compares it against all existing notes. Notes with similarity scores above the configured threshold are automatically linked together.

This process happens in the background, requiring no user action. The more notes you create, the richer the web of connections becomes, revealing unexpected relationships between your ideas.

The linking algorithm considers not just direct matches but also conceptual relationships. A note about "deep learning" might link to notes about "neural networks," "gradient descent," and "computer vision" because they share conceptual territory in the machine learning domain.

### Interactive Knowledge Graph

The knowledge graph visualization provides a bird's-eye view of your entire note collection. Built with D3.js, the graph displays notes as nodes and connections as edges, with visual properties (size, color, position) encoding additional information.

The visualization supports multiple interaction modes. You can drag nodes to rearrange the layout, zoom in and out to explore clusters, and hover over nodes to see note previews. Clicking a node opens the corresponding note for editing.

The graph automatically updates when notes are created, updated, or deleted. Connected components are identified and visually grouped, making it easy to see how different topic areas relate to each other.

### AI-Powered Categorization

Synapse Notes uses a language model to automatically categorize notes into topic clusters. When notes are created, the system analyzes their content and assigns them to groups based on semantic similarity.

Each category receives a unique color, visible both in the graph visualization and in the note list. This color coding makes it easy to identify topic areas at a glance and to understand how different domains connect.

Categories are dynamic—they evolve as your note collection grows. When sufficient notes on a topic exist, the system may split or merge categories to better reflect the structure of your knowledge.

### Path Finding

Have you ever wondered how two seemingly unrelated notes might be connected? The path-finding feature answers this question by computing the shortest path through your knowledge graph between any two notes.

This capability reveals hidden connections and demonstrates the surprising ways that different topic areas relate to each other. A path from "meditation" to "software architecture" might pass through "focus," "productivity," and "flow state," illustrating how the mental skills developed through meditation can inform programming practices.

### Real-time Updates

Synapse Notes provides immediate feedback as you write. Notes auto-save after a brief idle period, triggering the embedding and linking process in the background. The graph view updates to reflect new connections, often within seconds of saving.

This real-time behavior creates a responsive, alive feeling to the application. As you write, you can see your knowledge graph growing and connecting in real-time.

### Full-text Search

Every note is indexed for full-text search, allowing you to find specific content quickly. The search function supports both title and content matching, with results ranked by relevance.

### Export and Import

Notes can be exported in JSON format for backup or migration purposes. The export includes all note content, metadata, and connection information. Import functionality allows you to restore from backups or move notes between installations.

---

## Technical Architecture

Understanding the technical architecture of Synapse Notes helps explain how the various components work together to deliver the system's capabilities.

### System Overview

Synapse Notes follows a client-server architecture with a clean separation of concerns. The backend, built with FastAPI, handles data persistence, AI processing, and API endpoints. The frontend, built with vanilla JavaScript and D3.js, provides the user interface and graph visualization.

Communication between client and server occurs over HTTP REST APIs. The frontend makes requests to create, read, update, and delete notes, and to fetch graph data for visualization. All business logic resides in the backend.

### Backend Architecture

The backend is organized around several key modules:

**Database Layer.** SQLite provides lightweight, zero-configuration data persistence. The database schema includes tables for notes, links, and metadata. Foreign key constraints ensure referential integrity, and cascading deletes maintain consistency when notes are removed.

**Embedding Service.** When a note is created or updated, the embedding service sends its content to Ollama for vectorization. The resulting embedding—a list of floating-point numbers representing the semantic content—is stored alongside the note in the database.

**Similarity Engine.** The similarity engine compares embeddings using cosine similarity. For each new or updated note, the engine computes similarity scores against all other notes in the collection, creating links for pairs that exceed the threshold.

**Categorization Service.** The categorization service analyzes note clusters and assigns category labels using a language model. Categories are stored with notes and used for color coding in the visualization.

**API Layer.** FastAPI routes handle incoming requests, validate input data, and return responses. The API follows REST conventions, with clear resource-based endpoints and standard HTTP methods.

### Frontend Architecture

The frontend is a single-page application that communicates with the backend via AJAX requests. Key components include:

**Note Editor.** The editor provides a clean writing interface with title and content fields. Auto-save triggers after 1.2 seconds of inactivity, debouncing rapid keystrokes.

**Note List.** The note list displays all notes in reverse chronological order. Each entry shows the title, color-coded category, and connection count. Search filtering narrows the displayed notes based on user input.

**Graph Visualization.** The D3.js force-directed graph renders notes as circles and connections as lines. Node size reflects connection count, node color reflects category, and line thickness reflects similarity strength.

**Connection Panel.** When editing a note, the connection panel shows all linked notes with similarity scores. Clicking a connection opens that note for viewing or editing.

---

## System Requirements

Synapse Notes runs on any system that supports Python and Ollama. The following requirements ensure optimal performance.

### Hardware Requirements

**Minimum Configuration:**
- CPU: Any x86-64 processor (ARM supported for Apple Silicon)
- RAM: 4 GB
- Disk: 100 MB for application, additional space for notes database
- GPU: Optional but recommended for faster embeddings (Ollama with GPU support)

**Recommended Configuration:**
- CPU: Modern multi-core processor
- RAM: 8 GB or more
- Disk: SSD with 1 GB free space
- GPU: NVIDIA GPU with CUDA support for accelerated embeddings

### Software Requirements

**Operating System:**
- macOS 10.14 or later
- Linux (Ubuntu 20.04+, Debian 11+, or equivalent)
- Windows 10 or later with WSL2

**Software Dependencies:**
- Python 3.9 or later
- Ollama installed and running
- Web browser (Chrome, Firefox, Safari, or Edge)

---

## Installation Guide

This section provides detailed instructions for installing and running Synapse Notes.

### Step 1: Install Ollama

Ollama provides the AI models that power Synapse Notes. Download and install Ollama from the official website (https://ollama.ai) or use your system's package manager.

After installation, verify that Ollama is running:

```bash
ollama --version
```

### Step 2: Pull Required Models

Synapse Notes uses two Ollama models: an embedding model and a chat model.

Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

This model converts text into semantic vectors. The nomic-embed-text model provides good quality embeddings at a reasonable size.

Pull the chat model for categorization:

```bash
ollama pull qwen2.5:7b
```

This model generates category labels based on note content. The 7-billion parameter version offers a good balance of quality and speed.

Verify the models are available:

```bash
ollama list
```

You should see both models listed.

### Step 3: Install Python Dependencies

Clone or download the Synapse Notes repository, then navigate to the backend directory:

```bash
cd synapse-notes/backend
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

The requirements file includes FastAPI, Uvicorn, Pydantic, httpx, and other dependencies.

### Step 4: Start Ollama (if not running)

Ensure Ollama is running in the background:

```bash
ollama serve
```

This starts the Ollama server on port 11434 by default. Keep this terminal open or run it as a background process.

### Step 5: Run the Backend Server

With Ollama running, start the Synapse Notes backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload during development. For production, remove this flag and use a proper process manager.

### Step 6: Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

You should see the Synapse Notes interface. Create your first note by clicking the "+" button in the sidebar.

---

## Configuration

Synapse Notes behavior can be customized through environment variables and configuration files.

### Environment Variables

Set environment variables before starting the server or add them to a `.env` file in the backend directory.

**OLLAMA_URL**
- Default: `http://localhost:11434`
- Description: The base URL for the Ollama API. Change this if Ollama runs on a different host or port.

**EMBED_MODEL**
- Default: `nomin-embed-text`
- Description: The Ollama model used for generating embeddings.

**CHAT_MODEL**
- Default: `qwen2.5:7b`
- Description: The Ollama model used for chat interactions (categorization).

**LINK_THRESHOLD**
- Default: `0.65`
- Description: Cosine similarity threshold for creating links. Higher values create fewer links; lower values create more.

Example `.env` file:

```
OLLAMA_URL=http://localhost:11434
EMBED_MODEL=nomic-embed-text
CHAT_MODEL=qwen2.5:7b
LINK_THRESHOLD=0.70
```

### Tuning Link Sensitivity

The LINK_THRESHOLD variable controls how aggressively notes are connected. Finding the right value depends on your content and preferences.

**High Threshold (0.75-0.85):** Creates fewer, more confident connections. Use when you want only strongly related notes linked. Good for smaller collections with very focused topics.

**Medium Threshold (0.60-0.75):** Balanced approach. Creates meaningful connections while avoiding false positives. Recommended starting point for most users.

**Low Threshold (0.50-0.60):** Creates many connections, including weaker relationships. Use when you want to discover unexpected connections. May include some noise in large collections.

### Using Different Models

Synapse Notes supports any Ollama embedding model. To use a different model:

1. Pull the model: `ollama pull <model-name>`
2. Update the EMBED_MODEL environment variable
3. Restart the server

Some alternative embedding models to consider:
- `all-minilm` - Smaller, faster model
- `mxbai-embed-large` - Higher quality, larger model
- `bge-large` - Balanced quality and size

For categorization, any Ollama chat model works. Smaller models (2-7B parameters) provide faster responses, while larger models (13B+) provide more accurate categorization.

---

## API Documentation

Synapse Notes provides a comprehensive REST API for all operations.

### Base URL

```
http://localhost:8000/api
```

All endpoints are relative to this base URL.

### Authentication

The API does not currently implement authentication. For production deployments, add authentication middleware to protect your notes.

### Endpoints

#### GET /api/notes

Retrieves all notes.

**Response:**
```json
[
  {
    "id": 1,
    "title": "My Note",
    "content": "Note content here",
    "color": "#4a90d9",
    "category": "programming",
    "created_at": 1704067200,
    "updated_at": 1704067200
  }
]
```

#### POST /api/notes

Creates a new note.

**Request:**
```json
{
  "title": "New Note",
  "content": "Note content"
}
```

**Response:**
```json
{
  "id": 2,
  "color": "#a8c44e",
  "category": "research"
}
```

#### GET /api/notes/{id}

Retrieves a specific note.

**Response:**
```json
{
  "id": 1,
  "title": "My Note",
  "content": "Note content",
  "color": "#4a90d9",
  "category": "programming",
  "created_at": 1704067200,
  "updated_at": 1704067200
}
```

#### PUT /api/notes/{id}

Updates an existing note.

**Request:**
```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Response:**
```json
{
  "ok": true,
  "color": "#9b7fd4",
  "category": "research"
}
```

#### DELETE /api/notes/{id}

Deletes a note and all its connections.

**Response:**
```json
{
  "ok": true
}
```

#### GET /api/graph

Retrieves the complete graph data for visualization.

**Response:**
```json
{
  "nodes": [
    {"id": 1, "title": "Note 1", "color": "#4a90d9", "category": "tech"}
  ],
  "links": [
    {"source": 1, "target": 2, "score": 0.82}
  ]
}
```

#### GET /api/graph/version

Returns the current graph version number. Use for polling to detect changes.

**Response:**
```json
{
  "version": 5
}
```

#### GET /api/notes/{id}/connections

Gets all notes connected to the specified note.

**Response:**
```json
[
  {"id": 2, "title": "Connected Note", "color": "#a8c44e", "score": 0.85}
]
```

#### GET /api/path

Finds the shortest path between two notes.

**Parameters:**
- `source`: Source note ID
- `target`: Target note ID

**Response:**
```json
{
  "found": true,
  "path": [
    {"id": 1, "title": "Start", "color": "#4a90d9"},
    {"id": 5, "title": "Middle", "color": "#9b7fd4"},
    {"id": 10, "title": "End", "color": "#e05c5c"}
  ],
  "hops": 2
}
```

#### POST /api/recluster

Manually triggers a re-clustering of all notes. Normally clustering happens automatically, but this endpoint allows manual refresh.

**Response:**
```json
{
  "updated": 42,
  "clusters": 8
}
```

### Error Responses

Errors return appropriate HTTP status codes with JSON error messages:

```json
{
  "detail": "Note not found"
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

---

## Frontend Guide

This section describes how to use the Synapse Notes interface.

### The Sidebar

The sidebar appears on the left side of the screen and contains:

- **Logo and New Note Button:** Click the "+" button to create a new note
- **View Tabs:** Switch between "Notes" (list view) and "Graph" (visualization)
- **Search Bar:** Filter notes by title or content
- **Note List:** Scrollable list of all notes with title, category color, and connection count

### Creating a Note

1. Click the "+" button in the sidebar
2. Enter a title in the title field
3. Write content in the main text area
4. Notes auto-save after 1.2 seconds of inactivity

The saving indicator appears briefly when saving is in progress.

### Editing a Note

Click any note in the list to open it for editing. The editor panel shows:

- Title field (editable)
- Content textarea (editable)
- Connections panel (read-only) showing linked notes with similarity scores

Click the "X" button in the top-right corner to close the editor.

### Deleting a Note

Click the trash icon in the editor panel while editing a note. The note and all its connections are permanently deleted.

### The Graph View

Switch to the "Graph" tab to see the knowledge graph visualization.

**Navigation:**
- Drag the background to pan the view
- Scroll to zoom in and out
- Drag nodes to reposition them

**Interactions:**
- Hover over a node to see a preview tooltip
- Click a node to select it and see its connections highlighted
- Double-click a node to open it for editing

**Controls:**
- Click "Fit view" to reset the zoom and center the graph

### Searching Notes

Type in the search bar to filter notes by title or content. The list updates in real-time as you type. Clear the search box to show all notes.

---

## Database Schema

Synapse Notes uses SQLite for data persistence. Understanding the schema helps with debugging and custom extensions.

### Tables

#### notes

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique note identifier |
| title | TEXT | Note title |
| content | TEXT | Note content |
| color | TEXT | Hex color code for category |
| category | TEXT | Category label |
| embedding | TEXT | JSON-encoded embedding vector |
| created_at | INTEGER | Unix timestamp of creation |
| updated_at | INTEGER | Unix timestamp of last update |

#### links

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique link identifier |
| source_id | INTEGER | First note in the link |
| target_id | INTEGER | Second note in the link |
| score | REAL | Cosine similarity score |

The links table has a unique constraint on (source_id, target_id) to prevent duplicate links. Note that the order doesn't matter—source_id is always the smaller ID.

### Foreign Key Constraints

Foreign key constraints ensure referential integrity. When a note is deleted, SQLite automatically removes all corresponding links via CASCADE delete.

### Indexes

Indexes on frequently queried columns improve performance:

- `notes.category` for category filtering
- `links.source_id` and `links.target_id` for connection lookups
- `notes.updated_at` for chronological listing

---

## AI and Machine Learning

The AI capabilities of Synapse Notes rely on two Ollama models working together.

### Embedding Generation

When you create or update a note, the system sends its text content to Ollama for embedding. The embedding model (nomic-embed-text) converts the text into a 768-dimensional vector that captures semantic meaning.

The embedding process follows these steps:

1. Concatenate note title and content
2. Send the combined text to Ollama's `/api/embeddings` endpoint
3. Receive the embedding vector
4. Store the vector as a JSON string in the database

### Cosine Similarity

Similarity between notes is computed using cosine similarity, which measures the angle between two vectors:

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Where A·B is the dot product and ||A|| is the vector magnitude. Cosine similarity ranges from -1 (opposite) to 1 (identical), with 0 indicating orthogonality.

For note linking, we use only positive similarities above a threshold (typically 0.65-0.75).

### Categorization

Notes are categorized using a chat model that analyzes clusters of semantically similar notes. The process works as follows:

1. After clustering, select all notes in a cluster
2. Send a prompt to the chat model asking for a category label
3. Receive a 1-3 word label in lowercase
4. Assign the label and a corresponding color to all notes in the cluster

The category assignment updates whenever notes are re-clustered, which happens automatically after significant changes to the note collection.

### Clustering Algorithm

Notes are grouped into clusters using a greedy algorithm:

1. Sort notes by embedding
2. Start with the first unvisited note as the cluster seed
3. Add all notes with similarity >= threshold to the seed
4. Mark all added notes as visited
5. Repeat from step 2 with remaining unvisited notes

This algorithm produces overlapping clusters in the sense that notes can belong to only one cluster, but the clusters themselves are defined by transitive similarity.

---

## Graph Visualization

The knowledge graph visualization is built with D3.js, a powerful library for data-driven documents.

### Force-Directed Layout

The graph uses a force-directed layout where nodes repel each other and links act as springs. Over time, this simulation settles into a stable configuration that naturally groups connected notes together.

Forces in the simulation:
- **Charge force:** Nodes repel each other (default: -300)
- **Link force:** Connected nodes attract (default: distance 100)
- **Center force:** All nodes pulled toward center
- **Collision force:** Nodes cannot overlap

### Rendering

The visualization renders as an SVG with:
- Circles for nodes (size proportional to connections)
- Lines for links (thickness proportional to similarity)
- Text labels for nodes (truncated titles)

### Color Coding

Node colors represent categories, assigned by the AI categorization system. The color palette cycles through 12 distinct colors:

1. #4a90d9 (Blue)
2. #a8c44e (Green)
3. #9b7fd4 (Purple)
4. #d4a017 (Gold)
5. #4ecdc4 (Teal)
6. #f7a35c (Orange)
7. #e05c5c (Red)
8. #e07cb5 (Pink)
9. #5cc8e0 (Light Blue)
10. #d4724a (Burnt Orange)
11. #7dd48a (Light Green)
12. #c4a44e (Olive)

### Interactions

The visualization supports mouse and touch interactions:

- **Drag node:** Reposition a node (temporarily fixes its position)
- **Drag background:** Pan the view
- **Scroll:** Zoom in/out
- **Hover:** Show tooltip with note title
- **Click:** Select node, highlight connections
- **Double-click:** Open note for editing

---

## Docker Deployment

For containerized deployment, Synapse Notes includes Docker configuration.

### Docker Compose

The `docker-compose.yml` file defines the complete stack:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
      - LINK_THRESHOLD=0.65
    volumes:
      - ./backend/synapse.db:/app/synapse.db
    restart: unless-stopped
```

### Building the Image

```bash
docker compose build
```

### Running the Container

```bash
docker compose up -d
```

### Ollama Connection

The Docker container needs to connect to Ollama running on the host machine. The `OLLAMA_URL` environment variable points to `host.docker.internal:11434`, which resolves to the host's localhost from inside the container.

On Linux, you may need to add `--network=host` to the Docker run command instead of using `host.docker.internal`.

### Production Considerations

For production deployments:

1. Add authentication to protect your notes
2. Use a reverse proxy (nginx) with HTTPS
3. Set up regular backups of the SQLite database
4. Consider using a managed database for better concurrency
5. Monitor resource usage and scale as needed

---

## Troubleshooting

This section addresses common issues and their solutions.

### Notes Not Saving

**Symptom:** Notes don't save, or saving takes very long.

**Possible Causes:**
1. Ollama is not running
2. Network connectivity to Ollama is blocked
3. The embedding model is not downloaded

**Solutions:**
1. Verify Ollama is running: `ollama list`
2. Check OLLAMA_URL environment variable
3. Pull the model: `ollama pull nomic-embed-text`

### No Connections Between Notes

**Symptom:** Graph shows no links between notes.

**Possible Causes:**
1. LINK_THRESHOLD is too high
2. Notes don't have embeddings (API might have failed)
3. Not enough notes for similarity calculation

**Solutions:**
1. Lower LINK_THRESHOLD (try 0.55)
2. Check server logs for embedding errors
3. Create more diverse notes

### Too Many Connections

**Symptom:** Graph is a hairball with too many overlapping links.

**Possible Causes:**
1. LINK_THRESHOLD is too low
2. Notes are very short or generic

**Solutions:**
1. Raise LINK_THRESHOLD (try 0.75)
2. Add more specific content to notes

### Slow Performance

**Symptom:** App feels sluggish, especially with many notes.

**Possible Causes:**
1. Large embedding vectors
2. Many simultaneous requests
3. Slow Ollama responses

**Solutions:**
1. Use a smaller embedding model
2. Add database indexes
3. Enable Ollama GPU acceleration

### Docker Connection Issues

**Symptom:** Cannot connect to Ollama from Docker container.

**Solutions:**
1. On Mac/Windows: Ensure Ollama is accessible on the network
2. On Linux: Add `--network=host` or configure Docker networking
3. Check firewall rules

### Database Locked

**Symptom:** "database is locked" errors.

**Solutions:**
1. Ensure only one instance of the server is running
2. Check file permissions on the database
3. Restart the server

---

## Development Guide

This section is for developers who want to extend or modify Synapse Notes.

### Project Structure

```
synapse-notes/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── requirements.txt # Python dependencies
│   ├── synapse.db       # SQLite database (created at runtime)
│   └── generate_notes.py # Helper script for testing
├── frontend/
│   ├── index.html       # Main HTML file
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── docker-compose.yml
├── Dockerfile
├── README.md
└── PROJECT.md
```

### Backend Development

The backend is a single-file FastAPI application in `main.py`. Key functions include:

- `init_db()`: Creates database tables
- `get_embedding()`: Calls Ollama for embeddings
- `cosine_similarity()`: Computes similarity between vectors
- `recompute_links()`: Updates links for a note
- `auto_recluster()`: Re-runs categorization

### Frontend Development

The frontend consists of:
- `index.html`: Main HTML structure
- `static/css/style.css`: All styles
- `static/js/app.js`: Application logic

Key frontend functions:
- `createNote()`: Creates a new note via API
- `updateNote()`: Updates an existing note
- `deleteNote()`: Removes a note
- `loadNotes()`: Fetches and displays note list
- `loadGraph()`: Fetches and renders the graph

### Testing

To add test notes for development:

```bash
cd backend
python generate_notes.py
```

This script creates sample notes with realistic content about software development topics.

### Code Style

Follow these conventions:
- Python: Use Black formatter, type hints where possible
- JavaScript: Use ES6+ features, camelCase for variables
- CSS: BEM naming convention

---

## Performance Optimization

Optimize Synapse Notes for your hardware and use case.

### Embedding Speed

For faster embedding generation:

1. Use GPU acceleration with Ollama
2. Use a smaller embedding model
3. Batch embedding requests where possible

### Database Performance

Improve database speed:

1. Ensure indexes exist on frequently queried columns
2. Vacuum the database periodically: `sqlite3 synapse.db "VACUUM;"`
3. Consider switching to PostgreSQL for large collections

### Graph Rendering

For large graphs (1000+ notes):

1. Implement viewport culling (only render visible nodes)
2. Use WebGL rendering instead of SVG
3. Reduce simulation complexity
4. Disable label rendering at low zoom levels

---

## Security Considerations

Protect your notes and deployment.

### Local Deployment

For local-only use, no additional security is needed. Your notes stay on your machine.

### Network Deployment

If exposing Synapse Notes on a network:

1. Add authentication middleware
2. Use HTTPS with a valid certificate
3. Implement rate limiting
4. Validate all user input
5. Sanitize note content before rendering

### Ollama Security

Ollama runs locally and doesn't require authentication by default. For networked deployments:

1. Configure firewall rules
2. Consider adding authentication proxy
3. Keep Ollama updated for security patches

---

## Use Cases

Synapse Notes adapts to various workflows and use cases.

### Personal Knowledge Management

Capture and connect ideas from books, articles, and research. Synapse Notes helps you build a personal knowledge base that reveals connections between sources and topics.

### Project Documentation

Document project decisions, technical choices, and lessons learned. The knowledge graph shows how different aspects of a project relate to each other.

### Learning Tool

Study a new subject by creating notes on key concepts. Synapse Notes automatically identifies relationships, helping you understand how topics connect.

### Brainstorming

Capture ideas during brainstorming sessions. The visualization helps identify clusters and gaps in your thinking.

### Meeting Notes

Record meeting notes and see how topics connect across meetings. Discover recurring themes and action items.

---

## FAQ

### How does Synapse Notes compare to Obsidian/Roam Research?

Synapse Notes focuses on automatic connection discovery, while Obsidian and Roam require manual linking with wikilinks. Synapse Notes uses AI to understand meaning rather than relying on explicit connections.

### Can I use my own AI models?

Yes. Synapse Notes uses Ollama, which supports many models. Configure EMBED_MODEL and CHAT_MODEL to use different models.

### Where is my data stored?

All data is stored locally in `synapse.db` (SQLite). No cloud sync by default.

### How do I back up my notes?

Copy the `synapse.db` file to a backup location. You can also export notes as JSON using the API.

### Can I import notes from other apps?

Not directly, but you can write a script to import from JSON or other formats using the API.

### How many notes can Synapse Notes handle?

Performance varies by hardware, but Synapse Notes has been tested with thousands of notes. For very large collections, consider optimizing the graph rendering.

### Does Synapse Notes work offline?

Yes. Once Ollama models are downloaded, everything runs locally without internet.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Coding Standards

- Python: PEP 8 with Black formatting
- JavaScript: ESLint with standard config
- CSS: Stylelint with standard config

### Pull Request Guidelines

- Reference related issues
- Include tests for new features
- Update documentation as needed
- Be responsive to review feedback

---

## Roadmap

Planned features and improvements:

### Near Term
- Improved search with fuzzy matching
- Export to Markdown
- Dark mode support
- Keyboard shortcuts

### Medium Term
- Real-time collaboration
- Plugin system
- Mobile app
- Cloud sync option

### Long Term
- Spaced repetition integration
- AI-powered note suggestions
- Graph analytics
- Custom embedding models

---

## Changelog

### v1.0.0
- Initial release
- Basic CRUD operations
- Semantic linking
- Graph visualization
- AI categorization

### v1.1.0
- Path finding feature
- Performance improvements
- Bug fixes

---

## License

MIT License

Copyright (c) 2024 Synapse Notes

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Acknowledgments

Synapse Notes builds on many excellent open-source projects:

- **FastAPI** - Modern Python web framework
- **D3.js** - Data visualization library
- **Ollama** - Local AI model running
- **SQLite** - Embedded database engine
- **Pydantic** - Data validation for Python

Special thanks to the maintainers and communities of these projects.

---

## Contact and Support

- **GitHub Issues:** Report bugs and feature requests
- **Documentation:** You're reading it!
- **Discussions:** Share ideas and get help

For general questions and discussions, open a GitHub Discussion. For bugs, open a GitHub Issue with details about the problem and your environment.

---

*This documentation was last updated for Synapse Notes v1.1.0*
