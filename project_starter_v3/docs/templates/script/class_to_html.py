#!/usr/bin/env python3
"""class_to_html.py — class diagram markdown → Interactive HTML + Static SVG

Describes code-level classes (Services, Repositories, etc.) — NOT database tables.
For database tables use schema_to_html.py instead.

Input format (inside a markdown file):
```class
title: Order Module

class OrderService {
  +create(input: CreateOrderInput): Order
  +cancel(id: string, userId: string): void
  -validateStock(items: Item[]): boolean
}

class OrderRepository {
  +findById(id: string): Order
  +findByUser(userId: string): Order[]
  +save(order: Order): Order
}

class OrderController {
  +post(req, res): void
  +delete(req, res): void
}

OrderController --> OrderService: uses
OrderService --> OrderRepository: uses
```

Syntax rules:
  class ClassName { ... }     class block
  +method(params): return     public method
  -method(params): return     private method
  #method(params): return     protected method
  +field: Type                public field
  A --> B: label              dependency (uses)
  A --|> B                    inheritance (extends)
  A --o B: label              composition/aggregation
  title: <text>               optional diagram title
  # comment                   ignored

Outputs:
  <name>.html  — interactive (pan/zoom)
  <name>.svg   — static (for PDF embedding)

Usage:
  python3 class_to_html.py <input.md> [-o output.html]
"""
import sys, os, re, math

# ── Parser ───────────────────────────────────────────────────────────────────

def parse_class(content):
    block_match = re.search(r'```class\s*(.*?)```', content, re.DOTALL)
    raw = block_match.group(1) if block_match else content

    title = ""
    classes = {}   # name -> {members: []}
    relations = [] # {src, dst, kind, label}

    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1; continue
        if line.lower().startswith('title:'):
            title = line[6:].strip(); i += 1; continue

        # class block
        cm = re.match(r'^class\s+(\w+)\s*\{', line)
        if cm:
            cname = cm.group(1)
            members = []
            i += 1
            while i < len(lines):
                ml = lines[i].strip()
                if ml == '}':
                    i += 1; break
                if ml and not ml.startswith('#'):
                    members.append(ml)
                i += 1
            classes[cname] = {'members': members}
            continue

        # relations
        rm = re.match(r'^(\w+)\s*(-->|--\|>|--o)\s*(\w+)(?::\s*(.*))?$', line)
        if rm:
            kind_map = {'-->': 'uses', '--|>': 'extends', '--o': 'aggregates'}
            relations.append({
                'src': rm.group(1), 'dst': rm.group(3),
                'kind': kind_map.get(rm.group(2), 'uses'),
                'label': (rm.group(4) or '').strip()
            })
        i += 1

    return title, classes, relations


# ── Layout ───────────────────────────────────────────────────────────────────

CARD_W = 200
HEAD_H = 32
MEM_H  = 20
COLS   = 3
H_GAP  = 60
V_GAP  = 50
MARGIN = 50

COLORS = {
    'bg':       '#F7FAFC',
    'head_bg':  '#1A365D',
    'head_fg':  '#FFFFFF',
    'card_bg':  '#EBF8FF',
    'card_bd':  '#3182CE',
    'pub_fg':   '#276749',
    'priv_fg':  '#C53030',
    'prot_fg':  '#744210',
    'mem_fg':   '#2D3748',
    'uses':     '#4A5568',
    'extends':  '#3182CE',
    'aggregates':'#805AD5',
    'title_fg': '#1A365D',
}

VISIBILITY = {'+': COLORS['pub_fg'], '-': COLORS['priv_fg'], '#': COLORS['prot_fg']}


def card_height(cls):
    return HEAD_H + max(len(cls['members']), 1) * MEM_H + 8


def compute_positions(classes):
    pos = {}
    names = list(classes.keys())
    for i, name in enumerate(names):
        col = i % COLS
        row = i // COLS
        pos[name] = {
            'x': MARGIN + col * (CARD_W + H_GAP),
            'y': MARGIN + 40 + row * (max(card_height(c) for c in classes.values()) + V_GAP)
        }
    return pos


def build_svg(title, classes, relations):
    pos = compute_positions(classes)

    max_x = max((p['x'] + CARD_W for p in pos.values()), default=400) + MARGIN
    max_y = max((p['y'] + card_height(classes[n]) for n, p in pos.items()), default=300) + MARGIN

    svg = [
        f'<svg viewBox="0 0 {max_x} {max_y}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        '<defs>'
        '<marker id="arr-uses" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["uses"]}"/></marker>'
        '<marker id="arr-extends" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
        f'<polygon points="0,0 10,5 0,10" fill="none" stroke="{COLORS["extends"]}" stroke-width="1.5"/></marker>'
        '<marker id="arr-aggregates" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">'
        f'<polygon points="0,5 5,0 10,5 5,10" fill="{COLORS["aggregates"]}"/></marker>'
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
        if r['src'] not in pos or r['dst'] not in pos:
            continue
        p1, p2 = pos[r['src']], pos[r['dst']]
        h1 = card_height(classes[r['src']])
        h2 = card_height(classes[r['dst']])
        x1 = p1['x'] + CARD_W // 2
        y1 = p1['y'] + h1
        x2 = p2['x'] + CARD_W // 2
        y2 = p2['y']
        color = COLORS.get(r['kind'], COLORS['uses'])
        marker = f"url(#arr-{r['kind']})"
        dash = '6,3' if r['kind'] == 'uses' else ''
        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="1.6" fill="none" marker-end="{marker}"'
            + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
        )
        if r['label']:
            mx, my = (x1+x2)/2, (y1+y2)/2
            svg.append(
                f'<text x="{mx+4}" y="{my}" font-size="9" fill="{color}" font-style="italic">{r["label"]}</text>'
            )

    # Class cards
    for name, cls in classes.items():
        if name not in pos:
            continue
        p = pos[name]
        x, y = p['x'], p['y']
        h = card_height(cls)

        svg.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{h}" rx="6" '
            f'fill="{COLORS["card_bg"]}" stroke="{COLORS["card_bd"]}" stroke-width="1.5"/>'
        )
        svg.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{HEAD_H}" rx="6" fill="{COLORS["head_bg"]}"/>'
        )
        svg.append(f'<rect x="{x}" y="{y+HEAD_H-6}" width="{CARD_W}" height="6" fill="{COLORS["head_bg"]}"/>')
        svg.append(
            f'<text x="{x+CARD_W//2}" y="{y+HEAD_H//2+5}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="{COLORS["head_fg"]}">«class» {name}</text>'
        )

        if cls['members']:
            svg.append(
                f'<line x1="{x}" y1="{y+HEAD_H}" x2="{x+CARD_W}" y2="{y+HEAD_H}" '
                f'stroke="{COLORS["card_bd"]}" stroke-width="1"/>'
            )
            for mi, mem in enumerate(cls['members']):
                my = y + HEAD_H + mi * MEM_H + MEM_H // 2 + 4
                vis = mem[0] if mem and mem[0] in VISIBILITY else ''
                color = VISIBILITY.get(vis, COLORS['mem_fg'])
                safe_mem = mem.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                svg.append(
                    f'<text x="{x+8}" y="{my}" font-size="9.5" fill="{color}" font-family="monospace">{safe_mem}</text>'
                )

    svg.append('</svg>')
    return '\n'.join(svg)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><title>{title}</title>
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:'Segoe UI',Arial,sans-serif; background:#F7FAFC; overflow:hidden; }}
#wrap {{ position:fixed; inset:0; overflow:hidden; cursor:grab; }}
#wrap:active {{ cursor:grabbing; }}
#stage {{ position:absolute; transform-origin:0 0; padding:24px; }}
#hint {{ position:fixed; bottom:16px; left:50%; transform:translateX(-50%);
  background:#2D3748; color:#90CDF4; font-size:11px; padding:5px 14px;
  border-radius:20px; pointer-events:none; z-index:999; border:1px solid #4A5568; }}
</style>
</head>
<body>
<div id="wrap"><div id="stage">{svg_content}</div></div>
<div id="hint">Scroll to zoom · Drag to pan</div>
<script>
const wrap=document.getElementById('wrap');
let scale=1,px=0,py=0,panning=false,lmx=0,lmy=0;
wrap.addEventListener('wheel',e=>{{e.preventDefault();const d=e.deltaY>0?.9:1.1;const ns=Math.min(Math.max(scale*d,.2),5);const r=wrap.getBoundingClientRect();px=e.clientX-r.left-(e.clientX-r.left-px)*(ns/scale);py=e.clientY-r.top-(e.clientY-r.top-py)*(ns/scale);scale=ns;applyT();}},{{passive:false}});
wrap.addEventListener('mousedown',e=>{{panning=true;lmx=e.clientX;lmy=e.clientY;}});
window.addEventListener('mouseup',()=>panning=false);
window.addEventListener('mousemove',e=>{{if(panning){{px+=e.clientX-lmx;py+=e.clientY-lmy;lmx=e.clientX;lmy=e.clientY;applyT();}}}});
function applyT(){{document.getElementById('stage').style.transform=`translate(${{px}}px,${{py}}px) scale(${{scale}})`;}}
</script>
</body>
</html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 class_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    title, classes, relations = parse_class(content)
    if not classes:
        print("No classes found. Check your ```class block."); sys.exit(1)
    svg = build_svg(title, classes, relations)
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + '-class.html'
    svg_path = os.path.splitext(output_path)[0] + '.svg'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE.replace('{title}', title or 'Class Diagram').replace('{svg_content}', svg))
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {output_path} ({len(classes)} classes, {len(relations)} relations)")
    print(f"Generated: {svg_path} (static, for PDF embedding)")

if __name__ == '__main__':
    main()
