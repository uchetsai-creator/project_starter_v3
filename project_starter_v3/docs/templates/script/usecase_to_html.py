#!/usr/bin/env python3
"""usecase_to_html.py — UML Use Case diagram → Interactive HTML + Static SVG

Syntax:
  title: Smart Manufacturing System
  system: Smart Manufacturing System   ← system boundary label

  actor Admin
  actor Engineer extends Admin         ← inheritance: Engineer inherits Admin's use cases
  actor Operator extends Engineer

  usecase "Monitor production line" as UC1
  usecase "Analyse line performance" as UC2

  Admin --> UC1
  Engineer --> UC2

  UC2 ..> UC1 : <<include>>            ← include / extend relationship

Rules:
  - Use verb-oriented use case names ("Monitor X", "Generate Y", "Manage Z")
  - Use actor inheritance to avoid drawing the same line to every actor
  - Keep use cases at the same abstraction level (all user goals, not UI pages)
  - System boundary is drawn automatically around all use cases
"""
import sys, os, re, math

COLORS = {
    'bg':         '#F8FAFC',
    'sys_bg':     '#EBF8FF',
    'sys_bd':     '#BEE3F8',
    'sys_label':  '#2B6CB0',
    'uc_bg':      '#DBEAFE',
    'uc_bd':      '#3B82F6',
    'uc_fg':      '#1E40AF',
    'actor_fg':   '#1E3A5F',
    'actor_bd':   '#1E3A5F',
    'arrow':      '#4B5563',
    'inherit':    '#6B7280',
    'dep_dash':   '#6366F1',
    'title_fg':   '#1E3A5F',
    'label_fg':   '#6B7280',
}

UC_RX = 72
UC_RY = 26
ACTOR_W = 24
ACTOR_H = 60
H_GAP   = 56
V_GAP   = 52
MARGIN  = 40


# ── Text wrap ─────────────────────────────────────────────────────────────────

def wrap(text, max_chars=14):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if len(cand) > max_chars and cur:
            lines.append(cur); cur = w
        else:
            cur = cand
    if cur: lines.append(cur)
    return lines or [text]


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_usecase(content):
    if '```usecase' in content:
        m = re.search(r'```usecase\s*(.*?)```', content, re.DOTALL)
        raw = m.group(1) if m else content
    else:
        raw = content

    title      = ""
    system     = ""
    actors     = []          # list of {'name': str, 'parent': str|None}
    actor_set  = set()
    usecases   = {}          # alias -> label
    relations  = []          # {'src', 'dst', 'kind', 'label'}

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('title:'):
            title = line[6:].strip(); continue
        if line.lower().startswith('system:'):
            system = line[7:].strip(); continue

        # actor Name [extends Parent]
        m = re.match(r'^actor\s+(\S+)(?:\s+extends\s+(\S+))?', line, re.IGNORECASE)
        if m:
            name, parent = m.group(1), m.group(2)
            if name not in actor_set:
                actors.append({'name': name, 'parent': parent})
                actor_set.add(name)
            continue

        # usecase "Label" as ALIAS
        m = re.match(r'^usecase\s+"([^"]+)"\s+as\s+(\w+)', line)
        if m:
            usecases[m.group(2)] = m.group(1); continue

        # Actor --> UC  or  UC ..> UC2 : <<label>>
        m = re.match(r'^(\w+)\s*(-->|\.\.>|-\|>)\s*(\w+)(?:\s*:\s*(.*))?$', line)
        if m:
            src, arrow, dst, lbl = m.group(1), m.group(2), m.group(3), (m.group(4) or '').strip()
            if arrow == '-|>':
                kind = 'inherit'
            elif arrow == '..>':
                kind = 'dep'
            else:
                kind = 'access'
            relations.append({'src': src, 'dst': dst, 'kind': kind, 'label': lbl})

    return title, system, actors, usecases, relations


# ── Layout ────────────────────────────────────────────────────────────────────

def compute_layout(actors, usecases):
    """
    Actors on the left column, use cases on the right in a grid.
    Actors with inheritance are stacked vertically.
    """
    n_actors = len(actors)
    n_uc     = len(usecases)

    # Actor positions — evenly spaced vertically
    actor_col_x = MARGIN + ACTOR_W
    actor_positions = {}
    uc_keys = list(usecases.keys())

    # Estimate total height needed
    uc_cols = 2 if n_uc > 4 else 1
    uc_rows = math.ceil(n_uc / uc_cols)
    uc_h    = uc_rows * (UC_RY * 2 + V_GAP) + UC_RY
    actor_h = n_actors * (ACTOR_H + V_GAP)
    total_content_h = max(uc_h, actor_h)

    actor_spacing = total_content_h / max(n_actors, 1)
    for i, a in enumerate(actors):
        y = MARGIN + 60 + i * actor_spacing + actor_spacing / 2
        actor_positions[a['name']] = {'x': actor_col_x, 'y': y}

    # Use case positions — grid, right of actors
    uc_start_x = actor_col_x + ACTOR_W * 2 + H_GAP + 100
    uc_positions = {}
    for i, alias in enumerate(uc_keys):
        col = i % uc_cols
        row = i // uc_cols
        x = uc_start_x + col * (UC_RX * 2 + H_GAP)
        y = MARGIN + 60 + row * (UC_RY * 2 + V_GAP) + UC_RY
        uc_positions[alias] = {'x': x, 'y': y}

    total_w = uc_start_x + uc_cols * (UC_RX * 2 + H_GAP) + MARGIN
    total_h = max(
        MARGIN * 2 + 60 + uc_rows * (UC_RY * 2 + V_GAP),
        MARGIN * 2 + 60 + n_actors * (ACTOR_H + V_GAP)
    )

    return actor_positions, uc_positions, int(total_w), int(total_h)


# ── SVG builder ───────────────────────────────────────────────────────────────

def actor_svg(name, x, y):
    parts = []
    # Head
    parts.append(f'<circle cx="{x}" cy="{y - 24}" r="10" fill="none" stroke="{COLORS["actor_bd"]}" stroke-width="2"/>')
    # Body
    parts.append(f'<line x1="{x}" y1="{y-14}" x2="{x}" y2="{y+10}" stroke="{COLORS["actor_bd"]}" stroke-width="2"/>')
    # Arms
    parts.append(f'<line x1="{x-14}" y1="{y-4}" x2="{x+14}" y2="{y-4}" stroke="{COLORS["actor_bd"]}" stroke-width="2"/>')
    # Legs
    parts.append(f'<line x1="{x}" y1="{y+10}" x2="{x-12}" y2="{y+26}" stroke="{COLORS["actor_bd"]}" stroke-width="2"/>')
    parts.append(f'<line x1="{x}" y1="{y+10}" x2="{x+12}" y2="{y+26}" stroke="{COLORS["actor_bd"]}" stroke-width="2"/>')
    # Label
    safe = name.replace('&', '&amp;').replace('<', '&lt;')
    parts.append(
        f'<text x="{x}" y="{y+40}" text-anchor="middle" font-size="11" '
        f'font-weight="bold" fill="{COLORS["actor_fg"]}">{safe}</text>'
    )
    return parts


def build_svg(title, system, actors, usecases, relations):
    actor_pos, uc_pos, total_w, total_h = compute_layout(actors, usecases)
    title_h = 32 if title else 0
    total_h += title_h

    # Shift y positions down by title height
    for p in actor_pos.values(): p['y'] += title_h
    for p in uc_pos.values():    p['y'] += title_h

    svg = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<defs>'
        f'<marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker>'
        f'<marker id="arr_dep" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["dep_dash"]}"/></marker>'
        f'<marker id="arr_inh" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
        f'<polygon points="0,0 12,6 0,12" fill="none" stroke="{COLORS["inherit"]}" stroke-width="1.5"/>'
        f'</marker>'
        f'</defs>',
        f'<rect width="{total_w}" height="{total_h}" fill="{COLORS["bg"]}"/>',
    ]

    # Title
    if title:
        svg.append(
            f'<text x="{total_w//2}" y="26" text-anchor="middle" font-size="15" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # System boundary — box around all use cases
    if uc_pos:
        xs = [p['x'] for p in uc_pos.values()]
        ys = [p['y'] for p in uc_pos.values()]
        bx1 = min(xs) - UC_RX - 20
        by1 = min(ys) - UC_RY - 36
        bx2 = max(xs) + UC_RX + 20
        by2 = max(ys) + UC_RY + 20
        bw, bh = bx2 - bx1, by2 - by1
        svg.append(
            f'<rect x="{bx1}" y="{by1}" width="{bw}" height="{bh}" rx="8" '
            f'fill="{COLORS["sys_bg"]}" stroke="{COLORS["sys_bd"]}" '
            f'stroke-width="1.5" stroke-dasharray="6,3"/>'
        )
        sys_label = system or title or "System"
        safe_sys = sys_label.replace('&', '&amp;').replace('<', '&lt;')
        svg.append(
            f'<text x="{bx1+10}" y="{by1+18}" font-size="11" font-style="italic" '
            f'fill="{COLORS["sys_label"]}">{safe_sys}</text>'
        )

    # ── Relations ──────────────────────────────────────────────────────────────
    actor_names = {a['name'] for a in actors}

    for r in relations:
        src, dst, kind, lbl = r['src'], r['dst'], r['kind'], r['label']

        # Inheritance between actors
        if kind == 'inherit':
            p1 = actor_pos.get(src) or actor_pos.get(dst)
            p2 = actor_pos.get(dst) or actor_pos.get(src)
            if not p1 or not p2: continue
            x1, y1, x2, y2 = p1['x'], p1['y'], p2['x'], p2['y']
            svg.append(
                f'<line x1="{x1}" y1="{y1-30}" x2="{x2}" y2="{y2+30}" '
                f'stroke="{COLORS["inherit"]}" stroke-width="1.5" '
                f'marker-end="url(#arr_inh)"/>'
            )
            continue

        # Actor -> use case access
        if kind == 'access':
            ap = actor_pos.get(src)
            up = uc_pos.get(dst)
            if not ap or not up: continue
            x1, y1 = ap['x'] + ACTOR_W, ap['y']
            # End at left edge of ellipse
            x2 = up['x'] - UC_RX
            y2 = up['y']
            svg.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{COLORS["arrow"]}" stroke-width="1.2" '
                f'marker-end="url(#arr)"/>'
            )
            continue

        # Use case dependency (include / extend)
        if kind == 'dep':
            p1 = uc_pos.get(src)
            p2 = uc_pos.get(dst)
            if not p1 or not p2: continue
            x1, y1 = p1['x'], p1['y']
            x2, y2 = p2['x'], p2['y']
            # End at ellipse border
            dx, dy = x2-x1, y2-y1
            L = (dx**2+dy**2)**0.5 or 1
            ex = x2 - dx/L*UC_RX
            ey = y2 - dy/L*UC_RY
            safe_lbl = lbl.replace('&','&amp;').replace('<','&lt;')
            svg.append(
                f'<line x1="{x1}" y1="{y1}" x2="{ex}" y2="{ey}" '
                f'stroke="{COLORS["dep_dash"]}" stroke-width="1.2" '
                f'stroke-dasharray="5,3" marker-end="url(#arr_dep)"/>'
            )
            if lbl:
                mx, my = (x1+ex)/2, (y1+ey)/2 - 8
                svg.append(
                    f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="8.5" '
                    f'font-style="italic" fill="{COLORS["dep_dash"]}">{safe_lbl}</text>'
                )
            continue

    # ── Use cases ─────────────────────────────────────────────────────────────
    for alias, label in usecases.items():
        p = uc_pos[alias]
        cx, cy = p['x'], p['y']
        lines = wrap(label, max_chars=16)
        # Dynamic ellipse height based on line count
        ry = max(UC_RY, len(lines) * 10 + 6)
        svg.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{UC_RX}" ry="{ry}" '
            f'fill="{COLORS["uc_bg"]}" stroke="{COLORS["uc_bd"]}" stroke-width="1.8"/>'
        )
        start_y = cy - (len(lines)-1) * 9 + 4
        for li, ll in enumerate(lines):
            safe = ll.replace('&','&amp;').replace('<','&lt;')
            svg.append(
                f'<text x="{cx}" y="{start_y + li*18}" text-anchor="middle" '
                f'font-size="11" fill="{COLORS["uc_fg"]}">{safe}</text>'
            )

    # ── Actors ────────────────────────────────────────────────────────────────
    for a in actors:
        p = actor_pos[a['name']]
        svg.extend(actor_svg(a['name'], p['x'], p['y']))

    svg.append('</svg>')
    return '\n'.join(svg)


# ── HTML wrapper ──────────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{title}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0;}}body{{font-family:'Segoe UI',Arial,sans-serif;background:#F8FAFC;overflow:hidden;}}#wrap{{position:fixed;inset:0;overflow:hidden;cursor:grab;}}#wrap:active{{cursor:grabbing;}}#stage{{position:absolute;transform-origin:0 0;padding:24px;}}#hint{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:#1E3A5F;color:#93C5FD;font-size:11px;padding:5px 14px;border-radius:20px;pointer-events:none;z-index:999;}}</style>
</head><body>
<div id="wrap"><div id="stage">{svg_content}</div></div>
<div id="hint">Scroll to zoom · Drag to pan</div>
<script>
const wrap=document.getElementById('wrap');let scale=1,px=0,py=0,pan=false,lx=0,ly=0;
wrap.addEventListener('wheel',e=>{{e.preventDefault();const d=e.deltaY>0?.9:1.1;const ns=Math.min(Math.max(scale*d,.15),6);const r=wrap.getBoundingClientRect();px=e.clientX-r.left-(e.clientX-r.left-px)*(ns/scale);py=e.clientY-r.top-(e.clientY-r.top-py)*(ns/scale);scale=ns;go();}},{{passive:false}});
wrap.addEventListener('mousedown',e=>{{pan=true;lx=e.clientX;ly=e.clientY;}});
window.addEventListener('mouseup',()=>pan=false);
window.addEventListener('mousemove',e=>{{if(pan){{px+=e.clientX-lx;py+=e.clientY-ly;lx=e.clientX;ly=e.clientY;go();}}}});
function go(){{document.getElementById('stage').style.transform=`translate(${{px}}px,${{py}}px) scale(${{scale}})`;}}
</script></body></html>"""

def build_html(title, svg):
    return HTML_TEMPLATE.replace('{title}', title or 'Use Case Diagram').replace('{svg_content}', svg)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 usecase_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path  = sys.argv[1]
    base_output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = list(re.finditer(r'```usecase\s*(.*?)```', content, re.DOTALL))
    if not blocks:
        print("No ```usecase block found. Check your syntax."); sys.exit(1)

    base_stem = os.path.splitext(base_output or input_path)[0]
    if base_stem.endswith('-usecase'):
        base_stem = base_stem[:-len('-usecase')]

    generated = 0
    for idx, match in enumerate(blocks):
        result = parse_usecase(match.group(1))
        title  = result[0] or ""

        if len(blocks) == 1:
            out_stem = base_stem
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') if title else str(idx+1)
            out_stem = base_stem + f'-{slug}'

        output_path = out_stem + '-usecase.html'
        svg_path    = out_stem + '-usecase.svg'

        svg = build_svg(*result)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(build_html(title, svg))
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg)

        _, _, actors, usecases, _ = result
        print(f"Generated: {output_path} ({len(actors)} actors, {len(usecases)} use cases)")
        print(f"Generated: {svg_path} (static, for PDF embedding)")
        generated += 1

    if generated > 1:
        print(f"\nTotal: {generated} diagrams from {os.path.basename(input_path)}")


if __name__ == '__main__':
    main()
