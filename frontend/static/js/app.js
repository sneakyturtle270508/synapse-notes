const API = '';
let notes = [];
let activeNoteId = null;
let saveTimer = null;
let graphData = { nodes: [], links: [] };
let currentView = 'notes';
let noteFilter = '';

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
const noteSearchInput = document.getElementById('note-search');
const graphFitBtn = document.getElementById('graph-fit-btn');

async function fetchNotes() {
  const res = await fetch(`${API}/api/notes`);
  notes = await res.json();
  renderNoteList();
}

function renderNoteList() {
  noteList.innerHTML = '';
  const visibleNotes = notes.filter(matchesNoteFilter);
  if (visibleNotes.length === 0) {
    const msg = notes.length === 0 ? 'No notes yet' : 'No matching notes';
    noteList.innerHTML = `<div style="padding:12px 8px;font-size:12px;color:var(--text3)">${msg}</div>`;
    return;
  }
  visibleNotes.forEach(n => {
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

function matchesNoteFilter(note) {
  if (!noteFilter) return true;
  const haystack = `${note.title} ${note.category || ''} ${note.content || ''}`.toLowerCase();
  return haystack.includes(noteFilter);
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

function showSaving() { savingIndicator.classList.add('visible'); }
function hideSaving() { savingIndicator.classList.remove('visible'); }

function switchView(view) {
  currentView = view;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.view === view));
  if (view === 'notes') {
    editorView.classList.remove('hidden');
    graphView.classList.add('hidden');
    pathPanel.style.display = 'none';
    pathBtn.style.display = 'none';
  } else {
    editorView.classList.add('hidden');
    graphView.classList.remove('hidden');
    pathBtn.style.display = 'block';
    loadGraph();
  }
}

async function loadGraph() {
  const res = await fetch(`${API}/api/graph`);
  graphData = await res.json();
  renderGraph();
}

let sim, graphCtx;
let pan = { x: 0, y: 0 };
let zoom = 1;
let isPanning = false;
let panStart = { x: 0, y: 0 };
let graphNodes = [];
let graphLinks = [];

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

  graphNodes = graphData.nodes.map(n => ({ ...n }));
  graphLinks = graphData.links.map(l => ({ ...l }));

  if (sim) sim.stop();
  pan = { x: 0, y: 0 };
  zoom = 1;

  sim = d3.forceSimulation(graphNodes)
    .force('link', d3.forceLink(graphLinks).id(d => d.id).distance(140).strength(0.4))
    .force('charge', d3.forceManyBody().strength(-350))
    .force('center', d3.forceCenter(W / 2, H / 2))
    .force('collide', d3.forceCollide(55))
    .on('tick', () => drawGraph(graphNodes, graphLinks, W, H))
    .on('end', () => fitGraphToViewport(W, H));

  setupGraphInteraction(graphNodes, graphLinks, W, H);
}

function drawGraph(nodes, links, W, H) {
  graphCtx.save();
  graphCtx.clearRect(0, 0, W, H);
  graphCtx.translate(pan.x, pan.y);
  graphCtx.scale(zoom, zoom);

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
      graphCtx.arc(n.x, n.y, r + 6, 0, Math.PI * 2);
      graphCtx.fillStyle = n.color + '22';
      graphCtx.fill();
    }

    graphCtx.beginPath();
    graphCtx.arc(n.x, n.y, r, 0, Math.PI * 2);
    graphCtx.fillStyle = n.color;
    graphCtx.fill();

    if (n.category && n.category !== 'other') {
      graphCtx.font = '10px DM Sans, sans-serif';
      graphCtx.fillStyle = n.color + 'aa';
      graphCtx.fillText(n.category, n.x - graphCtx.measureText(n.category).width / 2, n.y - r - 6);
    }

    graphCtx.font = `${isActive ? '500 ' : ''}12px DM Sans, sans-serif`;
    graphCtx.fillStyle = isActive ? 'rgba(232,232,240,0.95)' : 'rgba(136,136,168,0.85)';
    graphCtx.fillText(n.title, n.x + r + 6, n.y + 4);
  });

  graphCtx.restore();
}

function setupGraphInteraction(nodes, links, W, H) {
  let draggingNode = null;

  function canvasPos(clientX, clientY) {
    const rect = graphCanvas.getBoundingClientRect();
    return {
      x: (clientX - rect.left - pan.x) / zoom,
      y: (clientY - rect.top - pan.y) / zoom
    };
  }

  function getNode(clientX, clientY) {
    const { x, y } = canvasPos(clientX, clientY);
    return nodes.find(n => Math.hypot((n.x || 0) - x, (n.y || 0) - y) < 16);
  }

  graphCanvas.onmousedown = e => {
    const n = getNode(e.clientX, e.clientY);
    if (n) {
      draggingNode = n;
      sim.alphaTarget(0.08).restart();
    } else {
      isPanning = true;
      panStart = { x: e.clientX - pan.x, y: e.clientY - pan.y };
      graphCanvas.style.cursor = 'grabbing';
    }
  };

  graphCanvas.onmousemove = e => {
    if (draggingNode) {
      const { x, y } = canvasPos(e.clientX, e.clientY);
      draggingNode.fx = x;
      draggingNode.fy = y;
      return;
    }
    if (isPanning) {
      pan.x = e.clientX - panStart.x;
      pan.y = e.clientY - panStart.y;
      drawGraph(nodes, links, W, H);
      return;
    }
    const n = getNode(e.clientX, e.clientY);
    if (n) {
      const rect = graphCanvas.getBoundingClientRect();
      graphTooltip.style.display = 'block';
      graphTooltip.style.left = (e.clientX - rect.left + 16) + 'px';
      graphTooltip.style.top = (e.clientY - rect.top - 10) + 'px';
      graphTooltip.textContent = n.title + (n.category && n.category !== 'other' ? ` · ${n.category}` : '');
      graphCanvas.style.cursor = 'grab';
    } else {
      graphTooltip.style.display = 'none';
      graphCanvas.style.cursor = 'default';
    }
  };

  graphCanvas.onmouseup = () => {
    if (draggingNode) {
      draggingNode.fx = null;
      draggingNode.fy = null;
      draggingNode = null;
      sim.alphaTarget(0);
    }
    isPanning = false;
    graphCanvas.style.cursor = 'default';
  };

  graphCanvas.onclick = e => {
    const n = getNode(e.clientX, e.clientY);
    if (n) { switchView('notes'); openNote(n.id); }
  };

  graphCanvas.onwheel = e => {
    e.preventDefault();
    const rect = graphCanvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    const worldX = (mouseX - pan.x) / zoom;
    const worldY = (mouseY - pan.y) / zoom;
    zoom = Math.max(0.35, Math.min(2.5, zoom * (e.deltaY > 0 ? 0.92 : 1.08)));
    pan.x = mouseX - worldX * zoom;
    pan.y = mouseY - worldY * zoom;
    drawGraph(nodes, links, W, H);
  };

  graphCanvas.onmouseleave = () => {
    graphTooltip.style.display = 'none';
    isPanning = false;
  };
}

function fitGraphToViewport(W, H) {
  if (!graphNodes.length) return;
  const minX = Math.min(...graphNodes.map(n => n.x || 0));
  const maxX = Math.max(...graphNodes.map(n => n.x || 0));
  const minY = Math.min(...graphNodes.map(n => n.y || 0));
  const maxY = Math.max(...graphNodes.map(n => n.y || 0));
  const graphW = Math.max(1, maxX - minX);
  const graphH = Math.max(1, maxY - minY);
  const padding = 70;
  zoom = Math.min((W - padding * 2) / graphW, (H - padding * 2) / graphH, 1.6);
  zoom = Math.max(0.35, zoom);
  pan.x = W / 2 - ((minX + maxX) / 2) * zoom;
  pan.y = H / 2 - ((minY + maxY) / 2) * zoom;
  drawGraph(graphNodes, graphLinks, W, H);
}

function highlightGraphNode(id) {
  if (graphData.nodes.length) renderGraph();
}

// ── Path Finder ────────────────────────────────────────────────
const pathBtn = document.createElement('button');
pathBtn.innerHTML = '🔗 Find Path';
pathBtn.style.cssText = `
  position:fixed;bottom:20px;right:20px;
  background:#7c6af7;color:#fff;border:none;border-radius:8px;
  padding:9px 15px;cursor:pointer;font-size:13px;
  font-family:'DM Sans',sans-serif;z-index:999;
  display:none;box-shadow:0 4px 16px rgba(124,106,247,0.4);
`;
document.body.appendChild(pathBtn);

const pathPanel = document.createElement('div');
pathPanel.style.cssText = `
  display:none;position:fixed;bottom:64px;right:20px;
  background:#13131b;border:1px solid rgba(255,255,255,0.1);
  border-radius:12px;padding:18px;width:270px;z-index:999;
  color:#e8e8f0;font-size:13px;font-family:'DM Sans',sans-serif;
  box-shadow:0 8px 32px rgba(0,0,0,0.5);
`;
pathPanel.innerHTML = `
  <div style="font-weight:500;margin-bottom:14px;">Find connection path</div>
  <div style="font-size:11px;color:#555570;margin-bottom:4px;text-transform:uppercase;letter-spacing:.06em;">From</div>
  <select id="path-from" style="width:100%;margin-bottom:12px;background:#1a1a26;color:#e8e8f0;border:1px solid rgba(255,255,255,0.1);border-radius:7px;padding:7px 9px;font-size:13px;font-family:'DM Sans',sans-serif;"></select>
  <div style="font-size:11px;color:#555570;margin-bottom:4px;text-transform:uppercase;letter-spacing:.06em;">To</div>
  <select id="path-to" style="width:100%;margin-bottom:14px;background:#1a1a26;color:#e8e8f0;border:1px solid rgba(255,255,255,0.1);border-radius:7px;padding:7px 9px;font-size:13px;font-family:'DM Sans',sans-serif;"></select>
  <button id="path-go" style="width:100%;background:#7c6af7;color:#fff;border:none;border-radius:7px;padding:9px;cursor:pointer;font-size:13px;font-family:'DM Sans',sans-serif;">Find Path</button>
  <div id="path-result" style="margin-top:14px;line-height:2;"></div>
`;
document.body.appendChild(pathPanel);

pathBtn.addEventListener('click', () => {
  const isOpen = pathPanel.style.display === 'block';
  pathPanel.style.display = isOpen ? 'none' : 'block';
  if (!isOpen) populatePathSelects();
});

function populatePathSelects() {
  const from = document.getElementById('path-from');
  const to = document.getElementById('path-to');
  from.innerHTML = '';
  to.innerHTML = '';
  notes.forEach(n => {
    from.innerHTML += `<option value="${n.id}">${escHtml(n.title)}</option>`;
    to.innerHTML += `<option value="${n.id}">${escHtml(n.title)}</option>`;
  });
  if (to.options.length > 1) to.selectedIndex = 1;
}

document.getElementById('path-go').addEventListener('click', async () => {
  const from = document.getElementById('path-from').value;
  const to = document.getElementById('path-to').value;
  const result = document.getElementById('path-result');
  if (from === to) { result.innerHTML = '<span style="color:#555570">Pick two different notes.</span>'; return; }
  result.innerHTML = '<span style="color:#555570">Searching...</span>';
  try {
    const data = await fetch(`${API}/api/path?source=${from}&target=${to}`).then(r => r.json());
    if (!data.found) {
      result.innerHTML = '<span style="color:#e05c5c;">No path found — these notes are not connected.</span>';
    } else {
      const hops = data.hops === 1 ? 'direct connection' : `${data.hops} hops`;
      result.innerHTML = `
        <div style="font-size:11px;color:#555570;margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em;">${hops}</div>
        <div style="display:flex;flex-wrap:wrap;align-items:center;gap:4px;">
          ${data.path.map((n, i) => `
            <span style="background:${n.color}22;color:${n.color};border:1px solid ${n.color}44;border-radius:20px;padding:3px 10px;font-size:12px;cursor:pointer;"
              onclick="openNote(${n.id});switchView('notes')">${escHtml(n.title)}</span>
            ${i < data.path.length - 1 ? '<span style="color:#555570">→</span>' : ''}
          `).join('')}
        </div>
      `;
    }
  } catch(e) {
    result.innerHTML = '<span style="color:#e05c5c;">Error finding path.</span>';
  }
});

// ── Event listeners ────────────────────────────────────────────
document.getElementById('new-note-btn').addEventListener('click', createNote);
document.getElementById('delete-note-btn').addEventListener('click', deleteNote);
noteTitleEl.addEventListener('input', scheduleSave);
noteContentEl.addEventListener('input', scheduleSave);

noteSearchInput.addEventListener('input', e => {
  noteFilter = e.target.value.trim().toLowerCase();
  renderNoteList();
});

graphFitBtn.addEventListener('click', () => {
  const W = graphCanvas.parentElement.clientWidth;
  const H = graphCanvas.parentElement.clientHeight;
  fitGraphToViewport(W, H);
});

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => switchView(tab.dataset.view));
});

fetchNotes();

// Poll for recluster updates every 4s
let _lastGraphVersion = -1;
setInterval(async () => {
  try {
    const { version } = await fetch(`${API}/api/graph/version`).then(r => r.json());
    if (_lastGraphVersion !== -1 && version !== _lastGraphVersion) {
      await fetchNotes();
      if (activeNoteId) {
        const note = notes.find(n => n.id === activeNoteId);
        if (note) renderCategoryTag(note);
        loadConnections(activeNoteId);
      }
      if (currentView === 'graph') loadGraph();
    }
    _lastGraphVersion = version;
  } catch(e) {}
}, 4000);