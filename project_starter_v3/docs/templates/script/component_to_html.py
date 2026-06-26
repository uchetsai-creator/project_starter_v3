#!/usr/bin/env python3
"""component_to_html.py — component diagram markdown → Interactive HTML + Static SVG

Describes software components, their interfaces, and dependencies.
Complements architecture.md (which shows runtime services) by showing
code-level package/module structure.

Input format (inside a markdown file):
```component
title: Frontend Module Structure

component "Auth Module" as Auth {
  provides: useAuth, AuthGuard
  requires: HTTP Client
}

component "Order Module" as Order {
  provides: OrderList, OrderDetail, useOrders
  requires: HTTP Client, Auth
}

component "HTTP Client" as HTTP {
  provides: apiGet, apiPost, apiPatch
  requires: Browser Fetch API
}

component "Router" as Router {
  provides: routes, navigate
  requires: Auth
}

Auth --> HTTP : uses
Order --> HTTP : uses
Order --> Auth : depends on
Router --> Auth : guards with
```

Syntax rules:
  component "Label" as ALIAS { ... }   component with provides/requires
  provides: A, B, C                     exported interfaces (inside component block)
  requires: X, Y                        required interfaces (inside component block)
  A --> B : label                       dependency arrow
  title: <text>                         optional title
  # comment                             ignored

Outputs:
  <name>.html  — interactive (pan/zoom)
  <name>.svg   — static (for PDF embedding)

Usage:
  python3 component_to_html.py <input.md> [-o output.html]
"""
import sys, os, re, math

# ── Parser ───────────────────────────────────────────────────────────────────

def parse_component(content):
    block_match = re.search(r'```component\s*(.*?)```', content, re.DOTALL)
    raw = block_match.group(1) if block_match else content

    title = ""
    components = {}
    relations = []

    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1; continue
        if line.lower().startswith('title:'):
            title = line[6:].strip(); i += 1; continue

        cm = re.match(r'^component\s+"([^"]+)"\s+as\s+(\w+)\s*\{?', line)
        if cm:
            label, alias = cm.group(1), cm.group(2)
            provides, requires = [], []
            i += 1
            if '{' in line:
                while i < len(lines):
                    ml = lines[i].strip()
                    if ml == '}':
                        i += 1; break
                    if ml.lower().startswith('provides:'):
                        provides = [p.strip() for p in ml[9:].split(',')]
                    elif ml.lower().startswith('requires:'):
                        requires = [r.strip() for r in ml[9:].split(',')]
                    i += 1
            components[alias] = {'label': label, 'provides': provides, 'requires': requires}
            continue

        rm = re.match(r'^(\w+)\s*-->\s*(\w+)(?:\s*:\s*(.*))?$', line)
        if rm:
            relations.append({'src': rm.group(1), 'dst': rm.group(2),
                               'label': (rm.group(3) or '').strip()})
        i += 1

    return title, components, relations


# ── Layout / SVG ─────────────────────────────────────────────────────────────

CARD_W = 200
HEAD_H = 32
IFACE_H = 18
COLS = 3
H_GAP = 70
V_GAP = 60
MARGIN = 50

COLORS = {
    'bg':        '#F7FAFC',
    'head_bg':   '#2D3748',
    'head_fg':   '#FFFFFF',
    'card_bg':   '#F7FAFC',
    'card_bd':   '#4A5568',
    'prov_fg':   '#276749',
    'req_fg':    '#C53030',
    'section_fg':'#718096',
    'arrow':     '#4A5568',
    'label_fg':  '#2D3748',
    'title_fg':  '#1A365D',
}


def card_height(comp):
    n_prov = len(comp['provides'])
    n_req  = len(comp['requires'])
    sections = 0
    if n_prov: sections += 1
    if n_req:  sections += 1
    return HEAD_H + (n_prov + n_req + sections) * IFACE_H + 8


def compute_positions(components):
    pos = {}
    names = list(components.keys())
    max_h = max((card_height(c) for c in components.values()), default=80)
    for i, name in enumerate(names):
        col = i % COLS
        row = i // COLS
        pos[name] = {
            'x': MARGIN + col * (CARD_W + H_GAP),
            'y': MARGIN + 40 + row * (max_h + V_GAP)
        }
    return pos


def build_svg(title, components, relations):
    pos = compute_positions(components)

    max_x = max((p['x'] + CARD_W for p in pos.values()), default=400) + MARGIN
    max_y = max((p['y'] + card_height(components[n]) for n, p in pos.items()), default=300) + MARGIN

    svg = [
        f'<svg viewBox="0 0 {max_x} {max_y}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        '<defs>'
        '<marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker>'
        '</defs>',
        f'<rect width="{max_x}" height="{max_y}" fill="{COLORS["bg"]}"/>',
    ]

    if title:
        svg.append(
            f'<text x="{max_x//2}" y="24" text-anchor="middle" font-size="14" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # Relations
    for r in relations:
        p1 = pos.get(r['src'])
        p2 = pos.get(r['dst'])
        if not p1 or not p2: continue
        h1 = card_height(components[r['src']])
        h2 = card_height(components[r['dst']])
        x1 = p1['x'] + CARD_W // 2
        y1 = p1['y'] + h1
        x2 = p2['x'] + CARD_W // 2
        y2 = p2['y']
        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{COLORS["arrow"]}" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arr)"/>'
        )
        if r['label']:
            mx, my = (x1+x2)/2 + 4, (y1+y2)/2
            svg.append(
                f'<text x="{mx}" y="{my}" font-size="9" fill="{COLORS["label_fg"]}" font-style="italic">{r["label"]}</text>'
            )

    # Component cards
    for alias, comp in components.items():
        if alias not in pos: continue
        p = pos[alias]
        x, y = p['x'], p['y']
        h = card_height(comp)

        # Card border with component icon (⊞)
        svg.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{h}" rx="6" '
            f'fill="{COLORS["card_bg"]}" stroke="{COLORS["card_bd"]}" stroke-width="1.5"/>'
        )
        # Header
        svg.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{HEAD_H}" rx="6" fill="{COLORS["head_bg"]}"/>'
        )
        svg.append(f'<rect x="{x}" y="{y+HEAD_H-6}" width="{CARD_W}" height="6" fill="{COLORS["head_bg"]}"/>')
        svg.append(
            f'<text x="{x+CARD_W//2}" y="{y+HEAD_H//2+5}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="{COLORS["head_fg"]}">⊞ {comp["label"]}</text>'
        )

        cy = y + HEAD_H + 4
        if comp['provides']:
            svg.append(
                f'<text x="{x+6}" y="{cy+IFACE_H//2+4}" font-size="8.5" '
                f'fill="{COLORS["section_fg"]}" font-style="italic">provides</text>'
            )
            cy += IFACE_H
            for prov in comp['provides']:
                svg.append(
                    f'<text x="{x+12}" y="{cy+IFACE_H//2+4}" font-size="10" '
                    f'fill="{COLORS["prov_fg"]}">▸ {prov}</text>'
                )
                cy += IFACE_H

        if comp['requires']:
            svg.append(
                f'<text x="{x+6}" y="{cy+IFACE_H//2+4}" font-size="8.5" '
                f'fill="{COLORS["section_fg"]}" font-style="italic">requires</text>'
            )
            cy += IFACE_H
            for req in comp['requires']:
                svg.append(
                    f'<text x="{x+12}" y="{cy+IFACE_H//2+4}" font-size="10" '
                    f'fill="{COLORS["req_fg"]}">◂ {req}</text>'
                )
                cy += IFACE_H

    svg.append('</svg>')
    return '\n'.join(svg)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{title}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0;}}body{{font-family:'Segoe UI',Arial,sans-serif;background:#F7FAFC;overflow:hidden;}}#wrap{{position:fixed;inset:0;overflow:hidden;cursor:grab;}}#wrap:active{{cursor:grabbing;}}#stage{{position:absolute;transform-origin:0 0;padding:24px;}}#hint{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:#2D3748;color:#90CDF4;font-size:11px;padding:5px 14px;border-radius:20px;pointer-events:none;z-index:999;border:1px solid #4A5568;}}</style>
</head><body>
<div id="wrap"><div id="stage">{svg_content}</div></div>
<div id="hint">Scroll to zoom · Drag to pan</div>
<script>
const wrap=document.getElementById('wrap');let scale=1,px=0,py=0,panning=false,lmx=0,lmy=0;
wrap.addEventListener('wheel',e=>{{e.preventDefault();const d=e.deltaY>0?.9:1.1;const ns=Math.min(Math.max(scale*d,.2),5);const r=wrap.getBoundingClientRect();px=e.clientX-r.left-(e.clientX-r.left-px)*(ns/scale);py=e.clientY-r.top-(e.clientY-r.top-py)*(ns/scale);scale=ns;applyT();}},{{passive:false}});
wrap.addEventListener('mousedown',e=>{{panning=true;lmx=e.clientX;lmy=e.clientY;}});
window.addEventListener('mouseup',()=>panning=false);
window.addEventListener('mousemove',e=>{{if(panning){{px+=e.clientX-lmx;py+=e.clientY-lmy;lmx=e.clientX;lmy=e.clientY;applyT();}}}});
function applyT(){{document.getElementById('stage').style.transform=`translate(${{px}}px,${{py}}px) scale(${{scale}})`;}}
</script></body></html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 component_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    title, components, relations = parse_component(content)
    if not components:
        print("No components found. Check your ```component block."); sys.exit(1)
    svg = build_svg(title, components, relations)
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + '-component.html'
    svg_path = os.path.splitext(output_path)[0] + '.svg'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE.replace('{title}', title or 'Component Diagram').replace('{svg_content}', svg))
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {output_path} ({len(components)} components, {len(relations)} relations)")
    print(f"Generated: {svg_path} (static, for PDF embedding)")

if __name__ == '__main__':
    main()
