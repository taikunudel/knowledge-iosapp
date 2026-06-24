#!/usr/bin/env python3
"""Build a self-contained folder-clustered graph (graph.html) of an OKF knowledge base.

Third root-level *view* over the bundle, alongside the catalog (index.md) and the
chronicle (log.md): index.md shows parent->child containment; this shows how pages
RELATE across folders -- the bridges between topic areas that the text catalog hides.

READ-ONLY. This script never writes to a knowledge page; it only reads them. The wiki
stays frozen. Output is a single graph.html with inline CSS/JS (no deps, no build).

Layout: folder-clustered. Each top-level folder is a labeled bubble holding its pages;
cross-folder relationships arc between bubbles, intra-folder ones stay inside. Spatial
separation is what makes ~200 relationships readable instead of a hairball.

Edge policy (rarity-weighted, IDF): a tag on every page is uninformative, exactly like
search ranking. weight(A,B) = sum over shared tags of log(N/(1+freq(tag))). Edges whose
score clears EDGE_MIN_TAG are drawn; weak "we're both in design" coincidences (score ~0)
draw no line. Explicit [[wikilinks]] are always drawn distinctly.

Re-run after editing pages:  python3 scripts/build_graph.py
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "graph.html"
RESERVED = {"index.md", "log.md"}

# ---- frontmatter (mirror of build_okf.split_frontmatter, kept dependency-free) --------
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)


def split_frontmatter(text: str):
    m = FM_RE.match(text)
    return (m.group(1).splitlines(), m.group(2)) if m else (None, text)


def parse_kv(fm_lines):
    """Tiny YAML reader for the flat frontmatter this bundle uses."""
    out: dict[str, object] = {}
    i = 0
    while i < len(fm_lines):
        ln = fm_lines[i].rstrip()
        if not ln or ln.startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$", ln)
        if not m:
            i += 1
            continue
        k, v = m.group(1), m.group(2).strip()
        if v == "":
            items = []
            i += 1
            while i < len(fm_lines) and re.match(r"^\s*-\s+", fm_lines[i]):
                items.append(re.sub(r"^\s*-\s+", "", fm_lines[i]).strip().strip('"'))
                i += 1
            out[k] = items
            continue
        if v.startswith("[") and v.endswith("]"):
            out[k] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
        else:
            out[k] = v.strip('"')
        i += 1
    return out


# ---- collect pages -------------------------------------------------------------------
def load_pages():
    pages = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel in RESERVED or "/.git/" in rel:
            continue
        fm_lines, body = split_frontmatter(p.read_text(encoding="utf-8"))
        if fm_lines is None:
            continue
        fm = parse_kv(fm_lines)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        parts = rel.split("/")
        folder = parts[0] if len(parts) > 1 else "(root)"
        pages.append({
            "id": rel[:-3],
            "file": rel,
            "title": str(fm.get("title", rel)).strip('"') or rel,
            "type": str(fm.get("type", "")).strip('"'),
            "status": str(fm.get("status", "")).strip('"'),
            "tags": [t.strip() for t in tags if t.strip()],
            "folder": folder,
            "body": body,
        })
    return pages


WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")


def build_edges(pages):
    """IDF-weighted shared-tag edges + explicit wikilinks. Returns (tag_edges, link_edges)
    where each edge is (a_id, b_id, weight, [shared_tags])."""
    by_id = {p["id"]: p for p in pages}
    slug = {p["id"].split("/")[-1].lower(): p for p in pages}
    N = len(pages)
    tag_freq = Counter()
    for p in pages:
        for tg in set(p["tags"]):
            tag_freq[tg] += 1

    def idf(tag):
        return max(0.0, math.log(N / (1 + tag_freq[tag])))

    raw = Counter()
    shared_map = {}
    for i, a in enumerate(pages):
        aset = set(a["tags"])
        for b in pages[i + 1:]:
            shared = aset & set(b["tags"])
            if not shared:
                continue
            score = sum(idf(tg) for tg in shared)
            if score >= EDGE_MIN_TAG:
                raw[(a["id"], b["id"])] = score
                shared_map[(a["id"], b["id"])] = sorted(shared)

    links = set()
    for a in pages:
        for target in WIKI_RE.findall(a["body"]):
            tgt = target.split("|")[0].split("#")[0].strip()
            b = by_id.get(tgt) or slug.get(tgt.lower())
            if b and b["id"] != a["id"]:
                links.add((a["id"], b["id"]))
    return raw, shared_map, links


EDGE_MIN_TAG = 1.5      # rarity score needed to draw a tag edge; weak folder-coincidences drop below this
FOLDER_COLORS = {
    "design-system": "#5e9eff", "engineering": "#34c759", "food-entry": "#ff9f0a",
    "today": "#ff375f", "navigation": "#bf5af2", "trends": "#64d2ff",
    "ai": "#ffd60a", "workflow": "#8e8e93", "(root)": "#b0b0b0",
}
TYPE_SHAPES = {"rule": "diamond", "decision": "circle", "guide": "square", "reference": "triangle"}


def is_tombstone(p):
    blob = (p["file"] + " " + p["title"] + " " + p["status"]).lower()
    return any(k in blob for k in ("retired", "rejected", "reverse"))


def build():
    pages = load_pages()
    pages.sort(key=lambda p: p["id"])
    tag_edges, shared_map, link_edges = build_edges(pages)
    by_id = {p["id"]: p for p in pages}

    # degree from kept edges (hub signal, for node sizing)
    deg = Counter()
    for (a, b) in tag_edges:
        deg[a] += 1; deg[b] += 1
    for a, b in link_edges:
        deg[a] += 1; deg[b] += 1

    # folder clusters: order pages within each folder, keep folder member counts
    folders = {}
    for p in pages:
        folders.setdefault(p["folder"], []).append(p["id"])
    # stable, readable order: by folder size desc then name
    folder_order = sorted(folders, key=lambda f: (-len(folders[f]), f))

    nodes = []
    for f in folder_order:
        for pid in folders[f]:
            p = by_id[pid]
            nodes.append({
                "id": pid,
                "title": p["title"],
                "short": pid.split("/")[-1],
                "folder": f,
                "type": p["type"],
                "tags": p["tags"],
                "href": p["file"],
                "degree": deg.get(pid, 0),
                "tombstone": is_tombstone(p),
                "color": FOLDER_COLORS.get(f, "#b0b0b0"),
                "shape": TYPE_SHAPES.get(p["type"], "circle"),
                "fidx": folder_order.index(f),     # which cluster ring slot
            })

    edges = []
    for (a, b), w in tag_edges.items():
        edges.append({"source": a, "target": b, "weight": round(w, 2),
                      "kind": "tag", "via": shared_map[(a, b)]})
    for a, b in link_edges:
        edges.append({"source": a, "target": b, "weight": 4, "kind": "link", "via": ["[[wikilink]]"]})

    OUT.write_text(render(nodes, edges, pages, folder_order, folders), encoding="utf-8")
    cross = sum(1 for e in edges if by_id[e["source"]]["folder"] != by_id[e["target"]]["folder"])
    intra = len(edges) - cross
    print(f"graph.html built: {len(nodes)} nodes in {len(folder_order)} folders, "
          f"{len(edges)} edges ({cross} cross-folder bridges, {intra} intra-folder). "
          f"Hubs: {[n['id'] for n in sorted(nodes,key=lambda x:-x['degree'])[:5]]}.")


# ---- self-contained HTML (plain string, @@TOKEN@@ injection) -------------------------
def render(nodes, edges, pages, folder_order, folders):
    payload = json.dumps({
        "nodes": nodes,
        "edges": edges,
        "folders": [{"name": f, "count": len(folders[f]), "color": FOLDER_COLORS.get(f, "#b0b0b0")}
                    for f in folder_order],
    }, ensure_ascii=False)
    n_cross = sum(1 for e in edges
                  if next(n for n in nodes if n["id"] == e["source"])["folder"]
                  != next(n for n in nodes if n["id"] == e["target"])["folder"])
    n_intra = len(edges) - n_cross
    built = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = _HTML_TEMPLATE
    for token, val in (("@@PAYLOAD@@", payload), ("@@NPAGES@@", str(len(pages))),
                       ("@@NFOLDERS@@", str(len(folder_order))), ("@@NEDGES@@", str(len(edges))),
                       ("@@NCROSS@@", str(n_cross)), ("@@NINTRA@@", str(n_intra)),
                       ("@@BUILT@@", built)):
        html = html.replace(token, val)
    return html


_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nutritionist Wiki — Knowledge Graph</title>
<style>
  :root { --bg:#0d1117; --panel:#161b22; --panel2:#1c2128; --ink:#c9d1d9; --dim:#8b949e;
          --line:#30363d; --link:#58a6ff; }
  * { box-sizing:border-box; }
  html,body { margin:0; height:100%; background:var(--bg); color:var(--ink);
           font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
  #app { display:flex; height:100vh; }
  #side { width:280px; min-width:280px; background:var(--panel); border-right:1px solid var(--line);
           padding:16px 16px 80px; overflow:auto; }
  #side h1 { font-size:15px; margin:0 0 2px; }
  #side .sub { color:var(--dim); font-size:12px; margin:0 0 14px; }
  #side h2 { font-size:10px; text-transform:uppercase; letter-spacing:.07em; color:var(--dim);
           margin:16px 0 6px; }
  .legend-row { display:flex; align-items:center; gap:8px; font-size:12px; margin:4px 0; }
  .legend-row .sw { width:12px; height:12px; flex:none; border-radius:3px; }
  .stat { font-size:12px; color:var(--dim); margin:3px 0; }
  .stat b { color:var(--ink); }
  #info { border-top:1px solid var(--line); margin-top:14px; padding-top:12px; font-size:12px;}
  #info .empty { color:var(--dim); font-style:italic; }
  #info .t { font-weight:600; font-size:13px; color:#fff; }
  #info .meta { color:var(--dim); margin:2px 0 8px; }
  #info .tags { display:flex; flex-wrap:wrap; gap:4px; margin:6px 0; }
  #info .tag { background:#ffffff14; border:1px solid var(--line); border-radius:10px;
            padding:1px 8px; font-size:11px; }
  #info a { color:var(--link); text-decoration:none; }
  #info a:hover { text-decoration:underline; }
  #info .nbr { margin-top:6px; }
  #info .nbr div { margin:2px 0; }
  #info .nbr .via { color:var(--dim); font-size:11px; }
  #stage { flex:1; position:relative; overflow:hidden; background:var(--bg); }
  canvas { display:block; }
  #hint { position:absolute; left:12px; bottom:12px; color:var(--dim); font-size:11px;
           background:#0d1117cc; padding:5px 9px; border-radius:6px; pointer-events:none;}
</style>
</head>
<body>
<div id="app">
  <aside id="side">
    <h1>Nutritionist Wiki</h1>
    <p class="sub">Knowledge graph — relationships across folders</p>
    <div class="stat"><b>@@NPAGES@@</b> pages &middot; <b>@@NFOLDERS@@</b> folders &middot; <b>@@NEDGES@@</b> relationships</div>
    <div class="stat">@@NCROSS@@ cross-folder bridges &middot; @@NINTRA@@ within-folder</div>
    <div class="stat" style="color:#6e7681">built @@BUILT@@ &middot; <i>regenerate: python3 scripts/build_graph.py</i></div>

    <h2>Folders (cluster color)</h2>
    <div id="folderlegend"></div>

    <h2>Page type (shape)</h2>
    <div class="legend-row" style="color:var(--dim)"><span>&#9670; rule</span>
      <span>&#9679; decision</span><span>&#9632; guide</span><span>&#9650; reference</span></div>

    <h2>Edge kind</h2>
    <div class="legend-row"><span class="sw" style="background:#58a6ff66"></span>shared distinguishing tag</div>
    <div class="legend-row"><span class="sw" style="background:#f0883e"></span>explicit [[wikilink]]</div>
    <div class="legend-row"><span class="sw" style="background:#ff375f"></span>tombstone (retired/rejected)</div>

    <h2>Selection</h2>
    <div id="info"><div class="empty">Click a node to see its relationships.</div></div>
  </aside>
  <main id="stage">
    <canvas id="cv"></canvas>
    <div id="hint">click a page to highlight its bridges &middot; scroll to zoom &middot; drag to pan</div>
  </main>
</div>
<script>
const DATA = @@PAYLOAD@@;
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
let W=0,H=0,DPR=1;
function resize(){ DPR=window.devicePixelRatio||1; W=cv.parentElement.clientWidth;
  H=cv.parentElement.clientHeight; cv.width=W*DPR; cv.height=H*DPR;
  cv.style.width=W+'px'; cv.style.height=H+'px'; }
window.addEventListener('resize',()=>{resize();layout();applyTransform();draw();});

// ---- cluster layout: each folder is a bubble on a ring; pages inside it on a small ring ----
const nodes = DATA.nodes.map(n=>({...n, x:0,y:0,vx:0,vy:0}));
const byId = Object.fromEntries(nodes.map(n=>[n.id,n]));
const folders = DATA.folders;
const RING = Math.min(W,H)*0.34;            // folder ring radius
const folderPos = {};
function layout(){
  const RING = Math.min(W,H)*0.34;
  const cx=W/2, cy=H/2;
  folders.forEach((f,i)=>{
    const ang = (i/folders.length)*Math.PI*2 - Math.PI/2;
    folderPos[f.name] = {x:cx+Math.cos(ang)*RING, y:cy+Math.sin(ang)*RING, ang};
    // place member pages on a small ring inside the cluster
    const mems = nodes.filter(n=>n.folder===f.name);
    const rr = 22 + mems.length*4.5;
    mems.forEach((m,j)=>{
      const a = (j/Math.max(mems.length,1))*Math.PI*2 + folderPos[f.name].ang;
      m.x = folderPos[f.name].x + Math.cos(a)*rr;
      m.y = folderPos[f.name].y + Math.sin(a)*rr;
      m.homeX=m.x; m.homeY=m.y; m.rr=rr; m.ang0=a;
    });
  });
}
// resolve edges to node objects
const edges = DATA.edges.map(e=>({source:byId[e.source], target:byId[e.target], ...e}))
  .filter(e=>e.source&&e.target);

// folder legend
const fl = document.getElementById('folderlegend');
fl.innerHTML = folders.map(f=>`<div class="legend-row"><span class="sw" style="background:${f.color}"></span>${f.name} <span style="color:var(--dim)">(${f.count})</span></div>`).join('');

let selected=null, hovered=null, zoom=1, panX=0, panY=0;
let dragPan=false, lastX=0,lastY=0, didDrag=false;

function applyTransform(){ ctx.setTransform(DPR*zoom,0,0,DPR*zoom,DPR*panX,DPR*panY); }

function shapePath(t,x,y,r){ ctx.beginPath();
  if(t==='diamond'){ ctx.moveTo(x,y-r);ctx.lineTo(x+r,y);ctx.lineTo(x,y+r);ctx.lineTo(x-r,y);ctx.closePath();}
  else if(t==='square'){ ctx.rect(x-r*0.85,y-r*0.85,r*1.7,r*1.7);}
  else if(t==='triangle'){ ctx.moveTo(x,y-r);ctx.lineTo(x+r*0.92,y+r*0.8);ctx.lineTo(x-r*0.92,y+r*0.8);ctx.closePath();}
  else { ctx.arc(x,y,r,0,Math.PI*2);} }

function conn(e,n){ return e.source.id===n.id||e.target.id===n.id; }
function other(e,n){ return e.source.id===n.id?e.target:e.source; }

function draw(){
  ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
  applyTransform();
  // cluster bubbles
  ctx.font='12px -apple-system';
  for(const f of folders){ const p=folderPos[f.name]; if(!p)continue;
    const mems=nodes.filter(n=>n.folder===f.name);
    const rr=22+mems.length*4.5+26;
    ctx.beginPath(); ctx.arc(p.x,p.y,rr,0,Math.PI*2);
    ctx.fillStyle=f.color+'12'; ctx.fill();
    ctx.strokeStyle=f.color+'55'; ctx.lineWidth=1.5; ctx.stroke();
    ctx.fillStyle=f.color; ctx.textAlign='center';
    ctx.fillText(f.name, p.x, p.y-rr-6);
  }
  // edges
  for(const e of edges){
    const isLink=e.kind==='link';
    const hi = selected && conn(e,selected);
    if(isLink){ ctx.strokeStyle = hi?'#f0883e':'#f0883e66'; ctx.lineWidth=hi?2.0:1.3;
                ctx.setLineDash([]); }
    else { ctx.strokeStyle = hi?'#79c0ff':(selected?'#30363d66':'#58a6ff44');
           ctx.lineWidth = hi?1.8:0.9; ctx.setLineDash(selected&&!hi?[3,3]:[]); }
    ctx.beginPath(); ctx.moveTo(e.source.x,e.source.y); ctx.lineTo(e.target.x,e.target.y); ctx.stroke();
  }
  ctx.setLineDash([]);
  // nodes
  for(const n of nodes){ const r=5+Math.min(6,Math.sqrt(n.degree)*1.7);
    const dim = selected && !edges.some(e=>conn(e,selected)&&other(e,selected).id===n.id) && n!==selected;
    ctx.globalAlpha = dim?0.25:1;
    shapePath(n.shape,n.x,n.y,r);
    ctx.fillStyle=n.color; ctx.fill();
    if(n.tombstone){ ctx.strokeStyle='#ff375f'; ctx.lineWidth=1.8; ctx.stroke(); }
    if(selected===n){ ctx.strokeStyle='#fff'; ctx.lineWidth=2.4; ctx.stroke(); }
    else if(hovered===n){ ctx.strokeStyle='#fff8'; ctx.lineWidth=1.6; ctx.stroke(); }
    ctx.globalAlpha=1;
    if(showLabels && (n.degree>=2||selected===n||hovered===n)){ ctx.fillStyle='#c9d1d9';
      ctx.font='11px -apple-system'; ctx.textAlign='center'; ctx.fillText(n.short,n.x,n.y-r-5); }
  }
  requestAnimationFrame(()=>{}); // draw is on-demand
}
let showLabels=true;

// interaction: click node = select; drag empty = pan; wheel = zoom
function screenToWorld(sx,sy){ return {x:(sx-panX)/zoom, y:(sy-panY)/zoom}; }
function hit(sx,sy){ const w=screenToWorld(sx,sy);
  for(let i=nodes.length-1;i>=0;i--){ const n=nodes[i]; const r=6+Math.sqrt(n.degree)*2;
    const dx=w.x-n.x,dy=w.y-n.y; if(dx*dx+dy*dy<=r*r) return n; } return null; }
function sp(e){ const r=cv.getBoundingClientRect(); return [e.clientX-r.left,e.clientY-r.top]; }

cv.addEventListener('pointerdown',e=>{ const [sx,sy]=sp(e); didDrag=false; const n=hit(sx,sy);
  if(n){ selected=n; renderInfo(n); } else { dragPan=true; } lastX=sx;lastY=sy;
  cv.setPointerCapture(e.pointerId); });
cv.addEventListener('pointermove',e=>{ const [sx,sy]=sp(e);
  if(dragPan){ panX+=sx-lastX; panY+=sy-lastY; lastX=sx;lastY=sy; didDrag=true; applyTransform(); draw(); }
  else { const n=hit(sx,sy); if(n!==hovered){ hovered=n; cv.style.cursor=n?'pointer':'grab'; draw(); } } });
cv.addEventListener('pointerup',e=>{ dragPan=false; cv.releasePointerCapture(e.pointerId); });
cv.addEventListener('wheel',e=>{ e.preventDefault(); const [sx,sy]=sp(e);
  const w=screenToWorld(sx,sy); const f=e.deltaY<0?1.12:0.89;
  zoom=Math.max(0.3,Math.min(3.5,zoom*f)); panX=sx-w.x*zoom; panY=sy-w.y*zoom;
  applyTransform(); draw(); }, {passive:false});
document.addEventListener('keydown',e=>{ if(e.key==='l'||e.key==='L'){showLabels=!showLabels;draw();}
  if(e.key==='0'){zoom=1;panX=0;panY=0;applyTransform();draw();}
  if(e.key==='Escape'){selected=null;renderInfo();draw();} });

function renderInfo(n){
  const el=document.getElementById('info');
  if(!n){ el.innerHTML='<div class="empty">Click a node to see its relationships.</div>'; return; }
  const es=edges.filter(e=>conn(e,n));
  const byKind={link:[],tag:[]};
  es.forEach(e=>{ byKind[e.kind].push({o:other(e,n),via:e.via||[]}); });
  const rows = [...byKind.link.map(x=>`<div><b>${esc(x.o.short)}</b> <span class="via">— ${x.via.join(', ')}</span> <span style="color:#f0883e">wikilink</span></div>`),
    ...byKind.tag.map(x=>`<div><b>${esc(x.o.short)}</b> <span class="via">— ${esc(x.o.folder)}</span> <span class="via">[${x.via.join(', ')}]</span></div>`)];
  el.innerHTML=`<div class="t">${esc(n.title)}</div>
    <div class="meta">${esc(n.folder)} &middot; ${esc(n.type)} ${n.tombstone?'<span style="color:#ff375f">tombstone</span>':''} &middot; ${es.length} relationships</div>
    <div class="tags">${n.tags.map(t=>`<span class=tag>${esc(t)}</span>`).join('')}</div>
    <a href="${n.href}" target="_blank">open ${esc(n.short)}.md &nearr;</a>
    <div class="nbr">${rows.join('')||'<div class="via">no relationships</div>'}</div>`;
}
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})); }

// init
resize(); layout(); applyTransform(); draw();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
