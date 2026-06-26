#!/usr/bin/env python3
"""state_to_html.py — state diagram markdown → Interactive HTML + Static SVG

Input format (inside a markdown file):
```state
title: Order Status

[*] -> draft
draft -> active: admin approves
draft -> cancelled: user cancels
active -> completed: all items shipped
active -> cancelled: admin cancels [refund issued]
completed -> [*]
cancelled -> [*]
```

Syntax rules:
  [*] -> A            initial transition (start)
  A -> [*]            final transition (end)
  A -> B: label       transition with label
  A -> B: label [guard]  transition with label and guard condition
  # comment           ignored
  title: <text>       optional diagram title

Outputs:
  <name>.html  — interactive (pan/zoom)
  <name>.svg   — static (for PDF embedding)

Usage:
  python3 state_to_html.py <input.md> [-o output.html]
"""
import sys, os, re, math

# ── Parser ───────────────────────────────────────────────────────────────────

def parse_state(content):
    block_match = re.search(r'```state\s*(.*?)```', content, re.DOTALL)
    raw = block_match.group(1) if block_match else content

    title = ""
    states = []
    seen = {}
    transitions = []

    def add_state(name):
        if name not in seen:
            seen[name] = len(states)
            states.append(name)

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('title:'):
            title = line[6:].strip()
            continue

        m = re.match(r'^(.+?)\s*->\s*(.+?)(?::\s*(.+))?$', line)
        if m:
            src = m.group(1).strip()
            dst = m.group(2).strip()
            label_raw = m.group(3).strip() if m.group(3) else ''

            label = label_raw
            guard = ''
            gm = re.match(r'^(.*?)\s*\[(.+)\]$', label_raw)
            if gm:
                label = gm.group(1).strip()
                guard = gm.group(2).strip()

            for s in (src, dst):
                if s != '[*]':
                    add_state(s)
            transitions.append({'src': src, 'dst': dst, 'label': label, 'guard': guard})

    return title, states, transitions


# ── Layout ───────────────────────────────────────────────────────────────────

NODE_W, NODE_H = 120, 36
H_GAP, V_GAP = 80, 70
COLS = 3
MARGIN = 60

COLORS = {
    'bg':        '#F7FAFC',
    'node_bg':   '#EBF8FF',
    'node_bd':   '#3182CE',
    'node_fg':   '#1A365D',
    'arrow':     '#4A5568',
    'label_bg':  '#FFFFFF',
    'label_fg':  '#2D3748',
    'guard_fg':  '#718096',
    'start_bg':  '#1A365D',
    'end_bg':    '#1A365D',
    'title_fg':  '#1A365D',
}


def compute_positions(states):
    pos = {}
    for i, s in enumerate(states):
        col = i % COLS
        row = i // COLS
        pos[s] = {
            'x': MARGIN + col * (NODE_W + H_GAP) + NODE_W // 2,
            'y': MARGIN + 40 + row * (NODE_H + V_GAP) + NODE_H // 2,
        }
    return pos


def build_svg(title, states, transitions):
    pos = compute_positions(states)

    # Add pseudo positions for [*]
    all_xs = [p['x'] for p in pos.values()] or [MARGIN + NODE_W // 2]
    cx_avg = sum(all_xs) / len(all_xs)
    min_y = min((p['y'] for p in pos.values()), default=MARGIN + 40)
    max_y = max((p['y'] for p in pos.values()), default=MARGIN + 40)

    pos['[*]_start'] = {'x': cx_avg, 'y': min_y - V_GAP}
    pos['[*]_end']   = {'x': cx_avg, 'y': max_y + V_GAP}

    def resolve(name, is_src):
        if name == '[*]':
            return pos['[*]_start'] if is_src else pos['[*]_end']
        return pos.get(name, {'x': 100, 'y': 100})

    max_x = max((p['x'] for p in pos.values()), default=200) + NODE_W // 2 + MARGIN
    max_y_val = pos['[*]_end']['y'] + 30

    svg = [
        f'<svg viewBox="0 0 {max_x} {max_y_val}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{max_x}" height="{max_y_val}" fill="{COLORS["bg"]}"/>',
    ]

    if title:
        svg.append(
            f'<text x="{max_x//2}" y="22" text-anchor="middle" font-size="14" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # Transitions (drawn under nodes)
    for t in transitions:
        p1 = resolve(t['src'], True)
        p2 = resolve(t['dst'], False)
        x1, y1, x2, y2 = p1['x'], p1['y'], p2['x'], p2['y']

        # Offset slightly for parallel edges
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length * 8, dx / length * 8

        cx = (x1 + x2) / 2 + nx
        cy = (y1 + y2) / 2 + ny

        svg.append(
            f'<path d="M {x1},{y1} Q {cx},{cy} {x2},{y2}" '
            f'stroke="{COLORS["arrow"]}" stroke-width="1.6" fill="none" marker-end="url(#arr)"/>'
        )

        # Label
        if t['label'] or t['guard']:
            lx, ly = (x1 + x2) / 2 + nx, (y1 + y2) / 2 + ny - 6
            label_text = t['label']
            guard_text = f'[{t["guard"]}]' if t['guard'] else ''
            svg.append(
                f'<rect x="{lx-36}" y="{ly-12}" width="72" height="14" rx="3" '
                f'fill="{COLORS["label_bg"]}" opacity="0.9"/>'
            )
            svg.append(
                f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="9" '
                f'fill="{COLORS["label_fg"]}">{label_text}</text>'
            )
            if guard_text:
                svg.append(
                    f'<text x="{lx}" y="{ly+12}" text-anchor="middle" font-size="8" '
                    f'font-style="italic" fill="{COLORS["guard_fg"]}">{guard_text}</text>'
                )

    # Arrow marker def
    svg.insert(2,
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker></defs>'
    )

    # Start/end pseudostates
    sp = pos['[*]_start']
    svg.append(f'<circle cx="{sp["x"]}" cy="{sp["y"]}" r="10" fill="{COLORS["start_bg"]}"/>')
    ep = pos['[*]_end']
    svg.append(f'<circle cx="{ep["x"]}" cy="{ep["y"]}" r="10" fill="{COLORS["end_bg"]}"/>')
    svg.append(f'<circle cx="{ep["x"]}" cy="{ep["y"]}" r="6" fill="{COLORS["bg"]}"/>')
    svg.append(f'<circle cx="{ep["x"]}" cy="{ep["y"]}" r="4" fill="{COLORS["end_bg"]}"/>')

    # State nodes
    for s, p in pos.items():
        if s.startswith('[*]'):
            continue
        x, y = p['x'] - NODE_W // 2, p['y'] - NODE_H // 2
        svg.append(
            f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="18" '
            f'fill="{COLORS["node_bg"]}" stroke="{COLORS["node_bd"]}" stroke-width="2"/>'
        )
        svg.append(
            f'<text x="{p["x"]}" y="{p["y"]+5}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="{COLORS["node_fg"]}">{s}</text>'
        )

    svg.append('</svg>')
    return '\n'.join(svg)


# ── HTML wrapper (same pan/zoom as sequence) ─────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #F7FAFC; overflow: hidden; }}
#wrap {{ position: fixed; inset: 0; overflow: hidden; cursor: grab; }}
#wrap:active {{ cursor: grabbing; }}
#stage {{ position: absolute; transform-origin: 0 0; padding: 24px; }}
#hint {{
  position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
  background: #2D3748; color: #90CDF4; font-size: 11px;
  padding: 5px 14px; border-radius: 20px; pointer-events: none;
  z-index: 999; border: 1px solid #4A5568;
}}
</style>
</head>
<body>
<div id="wrap"><div id="stage">{svg_content}</div></div>
<div id="hint">Scroll to zoom · Drag to pan</div>
<script>
const wrap = document.getElementById('wrap');
let scale = 1, px = 0, py = 0, panning = false, lmx = 0, lmy = 0;
wrap.addEventListener('wheel', e => {{
  e.preventDefault();
  const d = e.deltaY > 0 ? 0.9 : 1.1;
  const ns = Math.min(Math.max(scale * d, 0.2), 5);
  const r = wrap.getBoundingClientRect();
  px = e.clientX - r.left - (e.clientX - r.left - px) * (ns / scale);
  py = e.clientY - r.top  - (e.clientY - r.top  - py) * (ns / scale);
  scale = ns; applyT();
}}, {{ passive: false }});
wrap.addEventListener('mousedown', e => {{ panning = true; lmx = e.clientX; lmy = e.clientY; }});
window.addEventListener('mouseup', () => panning = false);
window.addEventListener('mousemove', e => {{
  if (panning) {{ px += e.clientX-lmx; py += e.clientY-lmy; lmx=e.clientX; lmy=e.clientY; applyT(); }}
}});
function applyT() {{
  document.getElementById('stage').style.transform = `translate(${{px}}px,${{py}}px) scale(${{scale}})`;
}}
</script>
</body>
</html>"""


def build_html(title, svg_content):
    return HTML_TEMPLATE.replace('{title}', title or 'State Diagram').replace('{svg_content}', svg_content)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 state_to_html.py <input.md> [-o output.html]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title, states, transitions = parse_state(content)

    if not states:
        print("No states found. Check your ```state block."); sys.exit(1)

    svg = build_svg(title, states, transitions)

    if not output_path:
        output_path = os.path.splitext(input_path)[0] + '-state.html'
    svg_path = os.path.splitext(output_path)[0] + '.svg'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(build_html(title, svg))
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f"Generated: {output_path} ({len(states)} states, {len(transitions)} transitions)")
    print(f"Generated: {svg_path} (static, for PDF embedding)")


if __name__ == '__main__':
    main()
