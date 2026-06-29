#!/usr/bin/env python3
"""usecase_to_html.py — use case diagram markdown → Interactive HTML + Static SVG

Input format (inside a markdown file):
```usecase
title: Order Management

actor Guest
actor User
actor Admin

usecase "View Orders" as UC1
usecase "Create Order" as UC2
usecase "Cancel Own Order" as UC3
usecase "Cancel Any Order" as UC4
usecase "Manage Products" as UC5

Guest --> UC1
User --> UC1
User --> UC2
User --> UC3
Admin --> UC1
Admin --> UC2
Admin --> UC4
Admin --> UC5

UC3 ..> UC2 : <<include>>
```

Syntax rules:
  actor Name                  define an actor
  usecase "Label" as ALIAS    define a use case
  Actor --> UC                actor accesses use case
  UC ..> UC2 : <<label>>      relationship between use cases (include/extend)
  title: <text>               optional diagram title
  # comment                   ignored

Outputs:
  <name>.html  — interactive (pan/zoom)
  <name>.svg   — static (for PDF embedding)

Usage:
  python3 usecase_to_html.py <input.md> [-o output.html]
"""
import sys, os, re, math

def parse_usecase(content):
    # Accept either a full markdown file or a raw block string
    if '```usecase' in content:
        _m = re.search(r'```usecase\s*(.*?)```', content, re.DOTALL)
        raw = _m.group(1) if _m else content
    else:
        raw = content

    title = ""
    actors = []
    usecases = {}  # alias -> label
    relations = []

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        if line.lower().startswith('title:'):
            title = line[6:].strip(); continue

        if line.lower().startswith('actor '):
            actors.append(line[6:].strip()); continue

        m = re.match(r'^usecase\s+"([^"]+)"\s+as\s+(\w+)', line)
        if m:
            usecases[m.group(2)] = m.group(1); continue

        m = re.match(r'^(\w+)\s*(-->|\.\.>)\s*(\w+)(?:\s*:\s*(.*))?$', line)
        if m:
            kind = 'access' if m.group(2) == '-->' else 'dep'
            relations.append({'src': m.group(1), 'dst': m.group(3),
                               'kind': kind, 'label': (m.group(4) or '').strip()})

    return title, actors, usecases, relations


COLORS = {
    'bg':       '#F7FAFC',
    'actor_fg': '#1A365D',
    'uc_bg':    '#EBF8FF',
    'uc_bd':    '#3182CE',
    'uc_fg':    '#1A365D',
    'access':   '#4A5568',
    'dep':      '#718096',
    'title_fg': '#1A365D',
    'sys_bd':   '#CBD5E0',
}

ACTOR_W, ACTOR_H = 40, 70
UC_RX, UC_RY = 70, 22
MARGIN = 60


def build_svg(title, actors, usecases, relations):
    n_actors = len(actors)
    n_uc = len(usecases)

    actor_cx = MARGIN + ACTOR_W // 2
    uc_start_x = actor_cx + 120
    uc_names = list(usecases.keys())

    # Positions
    actor_pos = {}
    for i, a in enumerate(actors):
        actor_pos[a] = {'x': actor_cx, 'y': MARGIN + 50 + i * 90}

    uc_pos = {}
    for i, alias in enumerate(uc_names):
        uc_pos[alias] = {
            'x': uc_start_x + UC_RX + (i % 2) * (UC_RX * 2 + 40),
            'y': MARGIN + 50 + (i // 2) * (UC_RY * 2 + 30)
        }

    max_x = max(
        [p['x'] + UC_RX for p in uc_pos.values()] +
        [actor_cx + ACTOR_W // 2]
    ) + MARGIN if uc_pos else 400
    max_y = max(
        [p['y'] + UC_RY for p in uc_pos.values()] +
        [p['y'] + ACTOR_H for p in actor_pos.values()]
    ) + MARGIN if uc_pos else 300

    svg = [
        f'<svg viewBox="0 0 {max_x} {max_y}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{max_x}" height="{max_y}" fill="{COLORS["bg"]}"/>',
        '<defs>'
        '<marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["access"]}"/></marker>'
        '</defs>',
    ]

    if title:
        svg.append(
            f'<text x="{max_x//2}" y="24" text-anchor="middle" font-size="14" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # System boundary box
    if uc_pos:
        sx = uc_start_x - 20
        sy = MARGIN + 30
        sw = max_x - sx - MARGIN // 2
        sh = max_y - sy - MARGIN // 2
        svg.append(
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8" '
            f'fill="none" stroke="{COLORS["sys_bd"]}" stroke-width="1.5" stroke-dasharray="6,3"/>'
        )
        svg.append(
            f'<text x="{sx+8}" y="{sy+16}" font-size="10" fill="{COLORS["sys_bd"]}">System</text>'
        )

    # Relations
    all_pos = {**actor_pos, **uc_pos}
    for r in relations:
        p1 = all_pos.get(r['src'])
        p2 = all_pos.get(r['dst'])
        if not p1 or not p2: continue
        x1, y1 = p1['x'], p1['y'] + (ACTOR_H // 2 if r['src'] in actor_pos else 0)
        x2, y2 = p2['x'], p2['y']
        color = COLORS['access'] if r['kind'] == 'access' else COLORS['dep']
        dash = '' if r['kind'] == 'access' else '5,3'
        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="1.4" marker-end="url(#arr)"'
            + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
        )
        if r['label']:
            mx, my = (x1+x2)/2, (y1+y2)/2
            safe_label = r['label'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            svg.append(
                f'<text x="{mx}" y="{my-4}" text-anchor="middle" font-size="9" '
                f'fill="{color}" font-style="italic">{safe_label}</text>'
            )

    # Actors (stick figures)
    for name, p in actor_pos.items():
        cx, cy = p['x'], p['y']
        svg.extend([
            f'<circle cx="{cx}" cy="{cy}" r="10" fill="none" stroke="{COLORS["actor_fg"]}" stroke-width="2"/>',
            f'<line x1="{cx}" y1="{cy+10}" x2="{cx}" y2="{cy+35}" stroke="{COLORS["actor_fg"]}" stroke-width="2"/>',
            f'<line x1="{cx-15}" y1="{cy+20}" x2="{cx+15}" y2="{cy+20}" stroke="{COLORS["actor_fg"]}" stroke-width="2"/>',
            f'<line x1="{cx}" y1="{cy+35}" x2="{cx-12}" y2="{cy+55}" stroke="{COLORS["actor_fg"]}" stroke-width="2"/>',
            f'<line x1="{cx}" y1="{cy+35}" x2="{cx+12}" y2="{cy+55}" stroke="{COLORS["actor_fg"]}" stroke-width="2"/>',
            f'<text x="{cx}" y="{cy+68}" text-anchor="middle" font-size="11" '
            f'font-weight="bold" fill="{COLORS["actor_fg"]}">{name}</text>',
        ])

    # Use cases (ellipses)
    for alias, p in uc_pos.items():
        label = usecases[alias]
        svg.append(
            f'<ellipse cx="{p["x"]}" cy="{p["y"]}" rx="{UC_RX}" ry="{UC_RY}" '
            f'fill="{COLORS["uc_bg"]}" stroke="{COLORS["uc_bd"]}" stroke-width="1.8"/>'
        )
        # Wrap text
        words = label.split()
        if len(words) <= 3:
            svg.append(
                f'<text x="{p["x"]}" y="{p["y"]+5}" text-anchor="middle" '
                f'font-size="11" fill="{COLORS["uc_fg"]}">{label}</text>'
            )
        else:
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            svg.append(f'<text x="{p["x"]}" y="{p["y"]-4}" text-anchor="middle" font-size="11" fill="{COLORS["uc_fg"]}">{line1}</text>')
            svg.append(f'<text x="{p["x"]}" y="{p["y"]+12}" text-anchor="middle" font-size="11" fill="{COLORS["uc_fg"]}">{line2}</text>')

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
        print("Usage: python3 usecase_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path = sys.argv[1]
    base_output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find ALL ```usecase blocks in the file
    blocks = list(re.finditer(r'```usecase\s*(.*?)```', content, re.DOTALL))
    if not blocks:
        print("No ```usecase block found. Check your syntax."); sys.exit(1)

    # Strip existing suffix from base stem to avoid doubling (e.g. file-usecase-usecase.html)
    base_stem = os.path.splitext(base_output or input_path)[0]
    if base_stem.endswith('-usecase'):
        base_stem = base_stem[:-len('-usecase')]

    generated = 0

    for idx, match in enumerate(blocks):
        result = parse_usecase(match.group(1))
        title  = result[0] or ""

        # Single block → keep original naming; multiple → append title slug or index
        if len(blocks) == 1:
            out_stem = base_stem
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') if title else str(idx + 1)
            out_stem = base_stem + f'-{slug}'

        output_path = out_stem + '-usecase.html'
        svg_path    = out_stem + '-usecase.svg'

        svg        = build_svg(*result)
        html_title = title or 'Usecase Diagram'

        _write_html = globals().get('build_html', None)
        with open(output_path, 'w', encoding='utf-8') as f:
            if _write_html:
                f.write(_write_html(html_title, svg))
            else:
                f.write(HTML_TEMPLATE.replace('{title}', html_title).replace('{svg_content}', svg))
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg)

        print(f"Generated: {output_path}")
        print(f"Generated: {svg_path} (static, for PDF embedding)")
        generated += 1

    if generated > 1:
        print(f"\nTotal: {generated} diagrams from {os.path.basename(input_path)}")


if __name__ == '__main__':
    main()
