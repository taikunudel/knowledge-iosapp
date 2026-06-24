#!/usr/bin/env python3
"""Build a self-contained force-directed graph (graph.html) of an OKF knowledge base.

Third root-level *view* over the bundle, alongside the catalog (index.md) and the
chronicle (log.md): index.md shows parent->child containment; this shows the
relationship fabric the text catalog hides -- tag co-occurrence and explicit links
across folders, plus hub/orphan/tombstone signals.

Honours OKF: reads only the .md files; index.md/log.md are reserved (no frontmatter)
and are not nodes. Output is a single graph.html with inline CSS/JS (no deps, no build).
Re-run after editing pages:  python3 scripts/build_graph.py

Edge policy (honesty over false precision):
  - structural edges: tag co-occurrence. Two pages sharing >=1 tag get an edge whose
    weight = #shared tags. This is the dense, real relationship fabric in this wiki.
  - explicit edges: [[wikilinks]] between pages. Drawn distinctly (brighter, on top).
  - supersession: NOT auto-extracted from prose (ambiguous). Tombstone/rejected pages
    are flagged by filename+status (retired/rejected/reverse) and drawn with a cue.
"""
from __future__ import annotations

import json
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
    """Tiny YAML reader for the flat frontmatter this bundle uses. Handles
    `key: value`, `key: "quoted"`, `key: [a, b, c]`, and `key:` block lists."""
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
        if v == "":                       # block list: following `- ...` lines
            items = []
            i += 1
            while i < len(fm_lines) and re.match(r"^\s*-\s+", fm_lines[i]):
                items.append(re.sub(r"^\s*-\s+", "", fm_lines[i]).strip().strip('"'))
                i += 1
            out[k] = items
            continue
        if v.startswith("[") and v.endswith("]"):                 # inline list
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
        folder = rel.split("/")[0] if "/" in rel else "(root)"
        # a subfolder like design-system/wwdc2026 -> keep both for the label
        parts = rel.split("/")
        sub = "/".join(parts[:-1]) if len(parts) > 1 else ""
        pages.append({
            "id": rel[:-3],                       # strip .md -> page_id used by [[links]]
            "file": rel,
            "title": str(fm.get("title", rel)).strip('"') or rel,
            "type": str(fm.get("type", "")).strip('"'),
            "status": str(fm.get("status", "")).strip('"'),
            "tags": [t.strip() for t in tags if t.strip()],
            "folder": folder,
            "subfolder": sub,
            "body": body,
        })
    return pages


WIKI_RE = re.compile(r"\[\[([^\]]+)\]\]")


def build_edges(pages):
    by_id = {p["id"]: p for p in pages}
    # page_id lookup is case- and path-insensitive on the slug
    slug = {p["id"].split("/")[-1].lower(): p for p in pages}

    structural = Counter()   # (a,b) -> shared-tag count
    for i, a in enumerate(pages):
        aset = set(a["tags"])
        for b in pages[i + 1:]:
            shared = aset & set(b["tags"])
            if shared:
                structural[(a["id"], b["id"])] = len(shared)

    explicit = set()
    for a in pages:
        for target in WIKI_RE.findall(a["body"]):
            tgt = target.split("|")[0].split("#")[0].strip()
            b = by_id.get(tgt) or slug.get(tgt.lower())
            if b and b["id"] != a["id"]:
                explicit.add((a["id"], b["id"]))
    return structural, explicit


def is_tombstone(p):
    name = p["file"].lower()
    blob = (p["title"] + " " + p["status"]).lower()
    return any(k in name or k in blob for k in ("retired", "rejected", "reverse"))


FOLDER_COLORS = {
    "design-system": "#5e9eff", "engineering": "#34c759", "food-entry": "#ff9f0a",
    "today": "#ff375f", "navigation": "#bf5af2", "trends": "#64d2ff",
    "ai": "#ffd60a", "workflow": "#8e8e93", "(root)": "#b0b0b0",
}
TYPE_SHAPES = {"rule": "diamond", "decision": "circle", "guide": "square", "reference": "triangle"}


def build():
    pages = load_pages()
    pages.sort(key=lambda p: p["id"])
    structural, explicit = build_edges(pages)

    # node degree (hub signal)
    deg = Counter()
    for (a, b), w in structural.items():
        deg[a] += w; deg[b] += w
    for a, b in explicit:
        deg[a] += 2; deg[b] += 2        # explicit links count more

    nodes = []
    for p in pages:
        d = deg.get(p["id"], 0)
        nodes.append({
            "id": p["id"],
            "title": p["title"],
            "folder": p["folder"],
            "type": p["type"],
            "tags": p["tags"],
            "href": p["file"],
            "degree": d,
            "orphan": d == 0,
            "tombstone": is_tombstone(p),
            "color": FOLDER_COLORS.get(p["folder"], "#b0b0b0"),
            "shape": TYPE_SHAPES.get(p["type"], "circle"),
        })

    edges = []
    for (a, b), w in structural.items():
        edges.append({"source": a, "target": b, "weight": w, "kind": "tag"})
    for a, b in explicit:
        edges.append({"source": a, "target": b, "weight": 2, "kind": "link"})

    out = render(nodes, edges, pages)
    OUT.write_text(out, encoding="utf-8")
    print(f"graph.html built: {len(nodes)} nodes, {len(edges)} edges "
          f"({sum(1 for e in edges if e['kind']=='tag')} tag, "
          f"{sum(1 for e in edges if e['kind']=='link')} link). "
          f"Hubs: {[n['id'] for n in sorted(nodes,key=lambda x:-x['degree'])[:5]]}. "
          f"Orphans: {[n['id'] for n in nodes if n['orphan']]}.")


# ---- self-contained HTML -------------------------------------------------------------
# The HTML/JS body is a PLAIN string (no f-string) so JS template literals (`${...}`)
# and CSS braces don't collide with Python formatting. Python values are injected via
# unique @@PLACEHOLDER@@ tokens replaced at the end.
def render(nodes, edges, pages):
    data = {"nodes": nodes, "edges": edges}
    payload = json.dumps(data, ensure_ascii=False)
    n_pages = len(pages)
    n_tag = sum(1 for e in edges if e["kind"] == "tag")
    n_link = sum(1 for e in edges if e["kind"] == "link")
    folders = sorted({p["folder"] for p in pages})
    legend_folders = "".join(
        f'<div class="legend-row"><span class="sw" style="background:{FOLDER_COLORS.get(f, "#b0b0b0")}"></span>{escape(f)}</div>'
        for f in folders)
    built = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = _HTML_TEMPLATE
    for token, val in (("@@PAYLOAD@@", payload), ("@@NPAGES@@", str(n_pages)),
                       ("@@NEDGES@@", str(len(edges))), ("@@NTAG@@", str(n_tag)),
                       ("@@NLINK@@", str(n_link)), ("@@BUILT@@", built),
                       ("@@LEGEND_FOLDERS@@", legend_folders)):
        html = html.replace(token, val)
    return html


_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nutritionist Wiki — Knowledge Graph</title>
<style>
  :root { --bg:#0d1117; --panel:#161b22; --ink:#c9d1d9; --dim:#8b949e; --line:#30363d;
          --tag:#30363d99; --link:#58a6ff; }
  * { box-sizing:border-box; }
  html,body { margin:0; height:100%; background:var(--bg); color:var(--ink);
           font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
  #app { display:flex; height:100vh; }
  #side { width:300px; min-width:300px; background:var(--panel); border-right:1px solid var(--line);
           padding:18px 18px 80px; overflow:auto; }
  #side h1 { font-size:16px; margin:0 0 2px; }
  #side .sub { color:var(--dim); font-size:12px; margin:0 0 14px; }
  #side h2 { font-size:11px; text-transform:uppercase; letter-spacing:.06em; color:var(--dim);
           margin:18px 0 8px; border-bottom:1px solid var(--line); padding-bottom:4px; }
  .legend-row { display:flex; align-items:center; gap:8px; font-size:12px; margin:5px 0; color:var(--ink);}
  .legend-row .sw { width:14px; height:14px; flex:none; border:1px solid #0006; }
  .legend-row.shape { color:var(--dim); }
  .stat { font-size:12px; color:var(--dim); margin:3px 0; }
  .stat b { color:var(--ink); }
  #info { border-top:1px solid var(--line); margin-top:18px; padding-top:12px; font-size:12px;}
  #info .empty { color:var(--dim); font-style:italic; }
  #info .t { font-weight:600; font-size:13px; color:#fff; }
  #info .meta { color:var(--dim); margin:2px 0 8px; }
  #info .tags { display:flex; flex-wrap:wrap; gap:4px; margin:6px 0; }
  #info .tag { background:#ffffff14; border:1px solid var(--line); border-radius:10px;
            padding:1px 8px; font-size:11px; }
  #info a { color:var(--link); text-decoration:none; }
  #info a:hover { text-decoration:underline; }
  #stage { flex:1; position:relative; overflow:hidden; }
  canvas { display:block; cursor:grab; }
  canvas:active { cursor:grabbing; }
  #hint { position:absolute; left:12px; bottom:12px; color:var(--dim); font-size:11px;
           background:#0d1117cc; padding:4px 8px; border-radius:6px; pointer-events:none;}
  #filter { width:100%; background:#0d1117; border:1px solid var(--line); color:var(--ink);
           border-radius:6px; padding:6px 9px; font-size:12px; margin-bottom:6px; }
  .pill { font-size:10px; vertical-align:middle; opacity:.8; }
</style>
</head>
<body>
<div id="app">
  <aside id="side">
    <h1>Nutritionist Wiki</h1>
    <p class="sub">Knowledge graph — relationships across folders</p>
    <input id="filter" placeholder="Filter pages or tags…" autocomplete="off">
    <div class="stat"><b>@@NPAGES@@</b> pages &middot; <b>@@NEDGES@@</b> edges</div>
    <div class="stat">@@NTAG@@ tag co-occurrence &middot; @@NLINK@@ explicit links</div>
    <div class="stat" style="color:#8b949e">built @@BUILT@@ &middot; <i>regenerate: python3 scripts/build_graph.py</i></div>

    <h2>Folders (color)</h2>
    @@LEGEND_FOLDERS@@

    <h2>Page type (shape)</h2>
    <div class="legend-row shape">&#9670; rule &nbsp; &#9679; decision &nbsp; &#9632; guide &nbsp; &#9650; reference</div>

    <h2>Edge kind</h2>
    <div class="legend-row"><span class="sw" style="background:#30363d99"></span>tag co-occurrence (shared tags)</div>
    <div class="legend-row"><span class="sw" style="background:var(--link)"></span>explicit [[wikilink]]</div>
    <div class="legend-row"><span class="sw" style="background:#ff375f"></span>tombstone (retired/rejected)</div>

    <h2>Selection</h2>
    <div id="info"><div class="empty">Click a node to inspect.</div></div>
  </aside>
  <main id="stage">
    <canvas id="cv"></canvas>
    <div id="hint">drag nodes &middot; scroll to zoom &middot; click to select &middot; space=pause &middot; L=labels &middot; 0=reset</div>
  </main>
</div>
<script>
const DATA = @@PAYLOAD@@;
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
let W=0,H=0,DPR=1;
function resize(){ DPR=window.devicePixelRatio||1; W=cv.clientWidth=cv.parentElement.clientWidth;
  H=cv.clientHeight=cv.parentElement.clientHeight; cv.width=W*DPR; cv.height=H*DPR;
  ctx.setTransform(DPR,0,0,DPR,0,0); }
window.addEventListener('resize',()=>{resize();applyTransform();});

const nodes = DATA.nodes.map(n=>Object.assign({
  x:W/2+(Math.random()-0.5)*W*0.6, y:H/2+(Math.random()-0.5)*H*0.6, vx:0, vy:0}, n));
const idx = Object.fromEntries(nodes.map(n=>[n.id,n]));
const edges = DATA.edges.map(e=>({source:idx[e.source], target:idx[e.target], ...e}))
  .filter(e=>e.source&&e.target);

// physics
const REPEL=4200, LINK=0.012, CENTER=0.004, DAMP=0.86, MAXV=6;
function step(){
  for(const n of nodes){ let fx=0,fy=0;
    for(const m of nodes){ if(m===n)continue; let dx=n.x-m.x,dy=n.y-m.y; let d2=dx*dx+dy*dy+0.01;
      let f=REPEL/d2; fx+=dx/Math.sqrt(d2)*f; fy+=dy/Math.sqrt(d2)*f; }
    fx+=(W/2-n.x)*CENTER; fy+=(H/2-n.y)*CENTER; n.fx=fx; n.fy=fy; }
  for(const e of edges){ let dx=e.target.x-e.source.x, dy=e.target.y-e.source.y;
    let d=Math.sqrt(dx*dx+dy*dy)||0.01; let want=70/Math.sqrt(e.weight);
    let f=(d-want)*LINK*e.weight; let ux=dx/d,uy=dy/d;
    e.source.fx+=ux*f; e.source.fy+=uy*f; e.target.fx-=ux*f; e.target.fy-=uy*f; }
  for(const n of nodes){ if(n.pinned)continue; n.vx=(n.vx+n.fx)*DAMP; n.vy=(n.vy+n.fy)*DAMP;
    n.vx=Math.max(-MAXV,Math.min(MAXV,n.vx)); n.vy=Math.max(-MAXV,Math.min(MAXV,n.vy));
    n.x+=n.vx; n.y+=n.vy; }
}
function draw(){ ctx.clearRect(0,0,W,H);
  for(const e of edges){ const hi=selected&&(e.source.id===selected.id||e.target.id===selected.id);
    ctx.strokeStyle = e.kind==='link' ? (hi?'#79c0ff':'#58a6ff66') : (hi?'#c9d1d9':'#30363d99');
    ctx.lineWidth = hi ? 1.6 : (e.kind==='link'?1.1:Math.min(1.4,0.4+e.weight*0.15));
    ctx.beginPath(); ctx.moveTo(e.source.x,e.source.y); ctx.lineTo(e.target.x,e.target.y); ctx.stroke(); }
  for(const n of nodes){ const r = 4+Math.min(7,Math.sqrt(n.degree)*1.6);
    ctx.beginPath(); ctx.fillStyle = n.orphan?'#4a4a4a':n.color;
    shape(ctx,n.shape,n.x,n.y,r); ctx.fill();
    if(n.tombstone){ ctx.strokeStyle='#ff375f'; ctx.lineWidth=1.8; ctx.stroke(); }
    if(selected===n){ ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.stroke(); }
    if(showLabels&&(n.degree>=3||selected===n||hovered===n)){ ctx.fillStyle='#c9d1d9';
      ctx.font='11px -apple-system'; ctx.textAlign='center'; ctx.fillText(n.title.slice(0,34),n.x,n.y-r-4); }
  } requestAnimationFrame(loop); }
function shape(ctx,t,x,y,r){ ctx.save(); ctx.translate(x,y);
  if(t==='diamond'){ ctx.moveTo(0,-r);ctx.lineTo(r,0);ctx.lineTo(0,r);ctx.lineTo(-r,0);ctx.closePath();}
  else if(t==='square'){ ctx.beginPath();ctx.rect(-r*0.85,-r*0.85,r*1.7,r*1.7);}
  else if(t==='triangle'){ ctx.beginPath();ctx.moveTo(0,-r);ctx.lineTo(r*0.92,r*0.8);ctx.lineTo(-r*0.92,r*0.8);ctx.closePath();}
  else { ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2);} ctx.restore(); }

let selected=null,hovered=null,paused=false,showLabels=true;
let zoom=1,panX=0,panY=0;
function loop(){ if(!paused)step(); draw(); }
function applyTransform(){ ctx.setTransform(DPR*zoom,0,0,DPR*zoom,DPR*panX,DPR*panY); }
function resetView(){ zoom=1;panX=0;panY=0; applyTransform(); }

// interaction (screen-space hit test, world-space drag)
function hit(sx,sy){ const wx=(sx-panX)/zoom, wy=(sy-panY)/zoom;
  for(let i=nodes.length-1;i>=0;i--){ const n=nodes[i];
    const dx=wx-n.x,dy=wy-n.y; if(dx*dx+dy*dy<=(7+Math.sqrt(n.degree)*2)**2) return n; } return null; }
function screenPos(e){ const r=cv.getBoundingClientRect(); return [e.clientX-r.left, e.clientY-r.top]; }
let drag=null;
cv.addEventListener('pointerdown',e=>{ const [sx,sy]=screenPos(e); const n=hit(sx,sy);
  if(n){ drag=n; n.pinned=true; selected=n; renderInfo(n); } else { selected=null; renderInfo(); } });
cv.addEventListener('pointermove',e=>{ const [sx,sy]=screenPos(e);
  if(drag){ drag.x=(sx-panX)/zoom; drag.y=(sy-panY)/zoom; drag.vx=0; drag.vy=0; }
  else { hovered=hit(sx,sy); cv.style.cursor=hovered?'pointer':'grab'; } });
cv.addEventListener('pointerup',()=>{ if(drag){ drag.pinned=false; drag=null; } });
cv.addEventListener('pointercancel',()=>{ if(drag){ drag.pinned=false; drag=null; } });
cv.addEventListener('wheel',e=>{ e.preventDefault(); const [sx,sy]=screenPos(e);
  const f=e.deltaY<0?1.12:0.89;
  const wx0=(sx-panX)/zoom, wy0=(sy-panY)/zoom;
  zoom=Math.max(0.3,Math.min(3,zoom*f));
  panX=sx-wx0*zoom; panY=sy-wy0*zoom; applyTransform(); }, {passive:false});

document.addEventListener('keydown',e=>{ if(e.key===' '){paused=!paused;}
  if(e.key==='l'||e.key==='L')showLabels=!showLabels; if(e.key==='0')resetView(); });

const filterEl=document.getElementById('filter');
filterEl.addEventListener('input',e=>{ const q=e.target.value.toLowerCase().trim();
  filterSet = q? new Set(nodes.filter(n=> n.title.toLowerCase().includes(q)||
    n.tags.some(t=>t.includes(q))||n.folder.includes(q)).map(n=>n.id)) : null;
});

function renderInfo(n){
  const el=document.getElementById('info');
  if(!n){ if(selected) n=selected; else { el.innerHTML='<div class="empty">Click a node to inspect.</div>'; return; } }
  const deg=edges.filter(e=>e.source.id===n.id||e.target.id===n.id).length;
  const neigh=[...new Set(edges.filter(e=>e.source.id===n.id).map(e=>e.target.id)
    .concat(edges.filter(e=>e.target.id===n.id).map(e=>e.source.id)))];
  el.innerHTML = `<div class="t">${esc(n.title)}</div>
    <div class="meta">${esc(n.folder)} &middot; ${esc(n.type)} ${n.orphan?'<span class=pill>&#9888; orphan</span>':''}${n.tombstone?'<span class=pill>&#9904; tombstone</span>':''}</div>
    <div class="meta">degree ${n.degree} &middot; ${deg} edges &middot; ${neigh.length} neighbors</div>
    <div class="tags">${n.tags.map(t=>`<span class=tag>${esc(t)}</span>`).join('')}</div>
    <a href="${n.href}" target="_blank">open ${esc(n.id)}.md &nearr;</a>
    ${neigh.length?'<div class="meta" style="margin-top:8px">linked: '+neigh.slice(0,12).map(id=>esc(id)).join(', ')+(neigh.length>12?'…':'')+'</div>':''}`;
}
function esc(s){ return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})); }

// init
resize(); applyTransform(); loop();
for(let i=0;i<60;i++)step();   // settle a little before first paint
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
