const API = '';
let notes = [];
let activeNoteId = null;
let saveTimer = null;
let graphData = { nodes: [], links: [] };
let currentView = 'notes';

const noteList = document.getElementById('note-list');
const emptyState = document.getElementById('empty-state');
const editorPanel = document.getElementById('editor-panel');
const noteTitleEl = document.getElementById('note-title');
const noteContentEl = document.getElementById('note-content');
const connectionsList = document.getElementById('connections-list');
const savingIndicator = document.getElementById('saving-indicator');
const editorView = document.getElementById('editor-view');
const graphView = document.getElementById('graph-view');
const graphCanvas = document.getElementById('graph-canvas');
const graphTooltip = document.getElementById('graph-tooltip');

async function fetchNotes() {
  const res = await fetch(`${API}/api/notes`);
  notes = await res.json();
  renderNoteList();
}

function renderNoteList() {
  noteList.innerHTML = '';
  if (notes.length === 0) {
    noteList.innerHTML = '<div style="padding:12px 8px;font-size:12px;color:var(--text3)">No notes yet</div>';
    return;
  }
  notes.forEach(n => {
    const item = document.createElement('div');
    item.className = 'note-item' + (n.id === activeNoteId ? ' active' : '');
    item.dataset.id = n.id;
    const d = new Date(n.updated_at * 1000);
    const dateStr = d.toLocaleDateString('en', { month: 'short', day: 'numeric' });
    item.innerHTML = `
      <div class="note-dot" style="background:${n.color}"></div>
      <span class="note-item-title">${escHtml(n.title || 'Untitled')}</span>
      <span class="note-item-date">${dateStr}</span>
    `;
    item.addEventListener('click', () => openNote(n.id));
    noteList.appendChild(item);
  });
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function renderCategoryTag(note) {
  const wrap = document.getElementById('category-tag-wrap');
  if (!wrap) return;
  if (!note || !note.category || note.category === 'other') {
    wrap.innerHTML = '';
    return;
  }
  const color = note.color || '#888';
  wrap.innerHTML = `
    <span class="category-tag" style="color:${color};border-color:${color}33;background:${color}11;">
      <span style="width:5px;height:5px;border-radius:50%;background:${color};display:inline-block;"></span>
      ${note.category}
    </span>
  `;
}

function openNote(id) {
  activeNoteId = id;
  const note = notes.find(n => n.id === id);
  if (!note) return;

  emptyState.classList.add('hidden');
  editorPanel.classList.remove('hidden');
  noteTitleEl.value = note.title;
  noteContentEl.value = note.content;
  renderNoteList();
  renderCategoryTag(note);
  loadConnections(id);

  if (currentView === 'graph') highlightGraphNode(id);
}

async function loadConnections(noteId) {
  connectionsList.innerHTML = '<span class="no-connections">Loading...</span>';
  try {
    const res = await fetch(`${API}/api/notes/${noteId}/connections`);
    const conns = await res.json();
    if (conns.length === 0) {
      connectionsList.innerHTML = '<span class="no-connections">No connections yet — keep writing</span>';
      return;
    }
    connectionsList.innerHTML = '';
    conns.forEach(c => {
      const chip = document.createElement('div');
      chip.className = 'conn-chip';
      chip.innerHTML = `
        <div class="conn-dot" style="background:${c.color}"></div>
        <span>${escHtml(c.title)}</span>
        <span class="conn-score">${Math.round(c.score * 100)}%</span>
      `;
      chip.addEventListener('click', () => openNote(c.id));
      connectionsList.appendChild(chip);
    });
  } catch(e) {
    connectionsList.innerHTML = '<span class="no-connections">Could not load connections</span>';
  }
}

async function createNote() {
  const res = await fetch(`${API}/api/notes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: 'New note', content: '' })
  });
  const data = await res.json();
  await fetchNotes();
  openNote(data.id);
  noteTitleEl.focus();
  noteTitleEl.select();
}

async function deleteNote() {
  if (!activeNoteId) return;
  if (!confirm('Delete this note?')) return;
  await fetch(`${API}/api/notes/${activeNoteId}`, { method: 'DELETE' });
  activeNoteId = null;
  editorPanel.classList.add('hidden');
  emptyState.classList.remove('hidden');
  await fetchNotes();
  if (currentView === 'graph') loadGraph();
}

function scheduleSave() {
  showSaving();
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNote, 1200);
}

async function saveNote() {
  if (!activeNoteId) return;
  const title = noteTitleEl.value.trim() || 'Untitled';
  const content = noteContentEl.value;
  const res = await fetch(`${API}/api/notes/${activeNoteId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content })
  });
  const data = await res.json();
  const note = notes.find(n => n.id === activeNoteId);
  if (note) {
    note.title = title;
    note.content = content;
    if (data.color) note.color = data.color;
    if (data.category) note.category = data.category;
  }
  renderNoteList();
  renderCategoryTag(note);
  hideSaving();
  loadConnections(activeNoteId);
  if (currentView === 'graph') loadGraph();
}

function showSaving() {
  savingIndicator.classList.add('visible');
}
function hideSaving() {
  savingIndicator.classList.remove('visible');
}

function switchView(view) {
  currentView = view;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.view === view));

  if (view === 'notes') {
    editorView.classList.remove('hidden');
    graphView.classList.add('hidden');
  } else {
    editorView.classList.add('hidden');
    graphView.classList.remove('hidden');
    loadGraph();
  }
}

async function loadGraph() {
  const res = await fetch(`${API}/api/graph`);
  graphData = await res.json();
  renderGraph();
}

let sim, graphCtx;

function renderGraph() {
  const container = graphCanvas.parentElement;
  const W = container.clientWidth;
  const H = container.clientHeight;
  const dpr = window.devicePixelRatio || 1;

  graphCanvas.width = W * dpr;
  graphCanvas.height = H * dpr;
  graphCanvas.style.width = W + 'px';
  graphCanvas.style.height = H + 'px';

  graphCtx = graphCanvas.getContext('2d');
  graphCtx.scale(dpr, dpr);

  const nodes = graphData.nodes.map(n => ({ ...n }));
  const links = graphData.links.map(l => ({ ...l }));

  if (sim) sim.stop();

  sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(140).strength(0.4))
    .force('charge', d3.forceManyBody().strength(-350))
    .force('center', d3.forceCenter(W / 2, H / 2))
    .force('collide', d3.forceCollide(55))
    .on('tick', () => drawGraph(nodes, links, W, H));

  setupGraphInteraction(nodes, W, H);
}

function drawGraph(nodes, links, W, H) {
  graphCtx.clearRect(0, 0, W, H);

  graphCtx.lineWidth = 1;
  links.forEach(l => {
    const alpha = 0.08 + (l.score || 0) * 0.2;
    graphCtx.strokeStyle = `rgba(255,255,255,${alpha})`;
    graphCtx.beginPath();
    graphCtx.moveTo(l.source.x, l.source.y);
    graphCtx.lineTo(l.target.x, l.target.y);
    graphCtx.stroke();
  });

  nodes.forEach(n => {
    const isActive = n.id === activeNoteId;
    const r = isActive ? 11 : 8;

    if (isActive) {
      graphCtx.beginPath();
      graphCtx.arc(n.x, n.y, r + 5, 0, Math.PI * 2);
      graphCtx.fillStyle = n.color + '22';
      graphCtx.fill();
    }

    graphCtx.beginPath();
    graphCtx.arc(n.x, n.y, r, 0, Math.PI * 2);
    graphCtx.fillStyle = n.color;
    graphCtx.fill();

    graphCtx.font = `${isActive ? '500 ' : ''}12px DM Sans, sans-serif`;
    graphCtx.fillStyle = isActive ? 'rgba(232,232,240,0.95)' : 'rgba(136,136,168,0.85)';
    graphCtx.fillText(n.title, n.x + r + 6, n.y + 4);
  });
}

function setupGraphInteraction(nodes, W, H) {
  let dragging = null;

  function getNode(ex, ey) {
    const rect = graphCanvas.getBoundingClientRect();
    const mx = ex - rect.left;
    const my = ey - rect.top;
    return nodes.find(n => Math.hypot((n.x || 0) - mx, (n.y || 0) - my) < 16);
  }

  graphCanvas.onmousedown = e => {
    const n = getNode(e.clientX, e.clientY);
    if (n) { dragging = n; sim.alphaTarget(0.08).restart(); }
  };

  graphCanvas.onmousemove = e => {
    const rect = graphCanvas.getBoundingClientRect();
    if (dragging) {
      dragging.fx = e.clientX - rect.left;
      dragging.fy = e.clientY - rect.top;
    }
    const n = getNode(e.clientX, e.clientY);
    if (n) {
      graphTooltip.style.display = 'block';
      graphTooltip.style.left = (e.clientX - rect.left + 16) + 'px';
      graphTooltip.style.top = (e.clientY - rect.top - 10) + 'px';
      graphTooltip.textContent = n.title;
      graphCanvas.style.cursor = 'grab';
    } else {
      graphTooltip.style.display = 'none';
      graphCanvas.style.cursor = 'default';
    }
  };

  graphCanvas.onmouseup = () => {
    if (dragging) { dragging.fx = null; dragging.fy = null; dragging = null; sim.alphaTarget(0); }
  };

  graphCanvas.onclick = e => {
    const n = getNode(e.clientX, e.clientY);
    if (n) {
      switchView('notes');
      openNote(n.id);
    }
  };

  graphCanvas.onmouseleave = () => { graphTooltip.style.display = 'none'; };
}

function highlightGraphNode(id) {
  if (graphData.nodes.length) renderGraph();
}

document.getElementById('new-note-btn').addEventListener('click', createNote);
document.getElementById('delete-note-btn').addEventListener('click', deleteNote);
noteTitleEl.addEventListener('input', scheduleSave);
noteContentEl.addEventListener('input', scheduleSave);

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => switchView(tab.dataset.view));
});

fetchNotes();
