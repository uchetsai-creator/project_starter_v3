#!/usr/bin/env python3
"""activity_to_html.py — activity diagram markdown → Interactive HTML + Static SVG

Input format (inside a markdown file):
```activity
title: Order Processing Flow

start
:Receive Order;
if (Stock available?) then (yes)
  :Reserve Stock;
  :Process Payment;
  if (Payment OK?) then (yes)
    :Confirm Order;
    :Send Confirmation Email;
  else (no)
    :Release Stock;
    :Notify Payment Failed;
  endif
else (no)
  :Notify Out of Stock;
endif
stop
```

Syntax rules:
  start                       start node
  stop                        end node
  :Action Label;              action (step)
  if (condition?) then (yes)  decision branch start
  else (no)                   else branch
  endif                       end of decision
  fork                        parallel split (basic, renders as note)
  join                        parallel join
  # comment                   ignored
  title: <text>               optional diagram title

Outputs:
  <name>.html  — interactive (pan/zoom)
  <name>.svg   — static (for PDF embedding)

Usage:
  python3 activity_to_html.py <input.md> [-o output.html]
"""
import sys, os, re

# ── Parser ───────────────────────────────────────────────────────────────────

def parse_activity(content):
    block_match = re.search(r'```activity\s*(.*?)```', content, re.DOTALL)
    raw = block_match.group(1) if block_match else content

    title = ""
    nodes = []   # list of node dicts
    edges = []   # list of {src, dst, label}

    def add(node):
        nodes.append(node)
        return len(nodes) - 1

    branch_stack = []  # stack of {if_idx, else_idx, ends: []}
    prev = None

    def connect(src, dst, label=''):
        if src is not None:
            edges.append({'src': src, 'dst': dst, 'label': label})

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        if line.lower().startswith('title:'):
            title = line[6:].strip(); continue

        if line == 'start':
            idx = add({'type': 'start'})
            prev = idx

        elif line == 'stop':
            idx = add({'type': 'stop'})
            connect(prev, idx)
            prev = idx

        elif re.match(r'^:.+;$', line):
            label = line[1:-1].strip()
            idx = add({'type': 'action', 'label': label})
            connect(prev, idx)
            prev = idx

        elif line.lower().startswith('if '):
            m = re.match(r'^if\s*\((.+?)\)\s*then\s*\((.+?)\)', line, re.IGNORECASE)
            cond = m.group(1) if m else line
            yes_label = m.group(2) if m else 'yes'
            idx = add({'type': 'decision', 'label': cond})
            connect(prev, idx)
            branch_stack.append({'if_idx': idx, 'yes_label': yes_label, 'prev_yes': idx, 'prev_else': None, 'ends': []})
            prev = idx

        elif line.lower().startswith('else'):
            m = re.match(r'^else\s*\((.+?)\)', line, re.IGNORECASE)
            no_label = m.group(1) if m else 'no'
            if branch_stack:
                branch_stack[-1]['prev_else'] = prev
                branch_stack[-1]['no_label'] = no_label
                prev = branch_stack[-1]['if_idx']

        elif line.lower() == 'endif':
            if branch_stack:
                frame = branch_stack.pop()
                merge_idx = add({'type': 'merge'})
                connect(prev, merge_idx)
                if frame['prev_else'] is not None:
                    connect(frame['prev_else'], merge_idx)
                prev = merge_idx

        elif line.lower() == 'fork':
            idx = add({'type': 'fork', 'label': 'fork'})
            connect(prev, idx)
            prev = idx

        elif line.lower() == 'join':
            idx = add({'type': 'join', 'label': 'join'})
            connect(prev, idx)
            prev = idx

    # Fix edges: for decision nodes, label yes/no on outgoing edges
    for frame in []:  # already handled inline
        pass

    # Retroactively label yes/no edges from decisions
    # (rebuild edge labels for decision -> next action)
    # Simple approach: first edge from decision = yes, second = no
    decision_edge_count = {}
    for e in edges:
        src = e['src']
        if src < len(nodes) and nodes[src]['type'] == 'decision':
            decision_edge_count[src] = decision_edge_count.get(src, 0) + 1

    decision_edge_seen = {}
    for e in edges:
        src = e['src']
        if src < len(nodes) and nodes[src]['type'] == 'decision' and not e['label']:
            count = decision_edge_seen.get(src, 0)
            if count == 0:
                e['label'] = 'yes'
            else:
                e['label'] = 'no'
            decision_edge_seen[src] = count + 1

    return title, nodes, edges


# ── Layout ───────────────────────────────────────────────────────────────────

NODE_W, NODE_H = 160, 34
V_STEP = 60
MARGIN = 50
DEC_SIZE = 28

COLORS = {
    'bg':       '#F7FAFC',
    'action_bg':'#EBF8FF',
    'action_bd':'#3182CE',
    'action_fg':'#1A365D',
    'dec_bg':   '#FEFCBF',
    'dec_bd':   '#D69E2E',
    'dec_fg':   '#744210',
    'merge_bg': '#F0FFF4',
    'merge_bd': '#38A169',
    'start_bg': '#1A365D',
    'stop_bg':  '#1A365D',
    'arrow':    '#4A5568',
    'label_fg': '#718096',
    'title_fg': '#1A365D',
    'fork_bg':  '#2D3748',
}


def build_svg(title, nodes, edges):
    cx = MARGIN + NODE_W // 2
    positions = []
    y = MARGIN + 40
    for node in nodes:
        positions.append({'x': cx, 'y': y})
        y += V_STEP + NODE_H

    total_w = NODE_W + MARGIN * 2
    total_h = y + MARGIN

    svg = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker></defs>',
        f'<rect width="{total_w}" height="{total_h}" fill="{COLORS["bg"]}"/>',
    ]

    if title:
        svg.append(
            f'<text x="{total_w//2}" y="24" text-anchor="middle" font-size="14" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # Edges
    for e in edges:
        p1, p2 = positions[e['src']], positions[e['dst']]
        n1, n2 = nodes[e['src']], nodes[e['dst']]
        x1, y1 = p1['x'], p1['y'] + NODE_H // 2
        x2, y2 = p2['x'], p2['y'] - NODE_H // 2
        if n1['type'] == 'start':
            y1 = p1['y'] + 10
        if n1['type'] == 'stop':
            y1 = p1['y'] + 10
        if n2['type'] == 'stop':
            y2 = p2['y'] - 10
        svg.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{COLORS["arrow"]}" stroke-width="1.6" marker-end="url(#arr)"/>'
        )
        if e.get('label'):
            mx, my = (x1+x2)/2, (y1+y2)/2
            svg.append(
                f'<text x="{mx+6}" y="{my}" font-size="9" fill="{COLORS["label_fg"]}">{e["label"]}</text>'
            )

    # Nodes
    for i, node in enumerate(nodes):
        p = positions[i]
        cx_, cy_ = p['x'], p['y']

        if node['type'] == 'start':
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="10" fill="{COLORS["start_bg"]}"/>')

        elif node['type'] == 'stop':
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="10" fill="{COLORS["stop_bg"]}"/>')
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="6" fill="{COLORS["bg"]}"/>')
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="4" fill="{COLORS["stop_bg"]}"/>')

        elif node['type'] == 'action':
            x = cx_ - NODE_W // 2
            y = cy_ - NODE_H // 2
            svg.append(
                f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="6" '
                f'fill="{COLORS["action_bg"]}" stroke="{COLORS["action_bd"]}" stroke-width="1.8"/>'
            )
            svg.append(
                f'<text x="{cx_}" y="{cy_+5}" text-anchor="middle" font-size="11" '
                f'fill="{COLORS["action_fg"]}">{node["label"]}</text>'
            )

        elif node['type'] == 'decision':
            s = DEC_SIZE
            svg.append(
                f'<polygon points="{cx_},{cy_-s} {cx_+s*1.8},{cy_} {cx_},{cy_+s} {cx_-s*1.8},{cy_}" '
                f'fill="{COLORS["dec_bg"]}" stroke="{COLORS["dec_bd"]}" stroke-width="1.8"/>'
            )
            safe = node['label'].replace('&', '&amp;').replace('<', '&lt;')
            svg.append(
                f'<text x="{cx_}" y="{cy_+4}" text-anchor="middle" font-size="9.5" '
                f'fill="{COLORS["dec_fg"]}">{safe}</text>'
            )

        elif node['type'] == 'merge':
            s = DEC_SIZE * 0.6
            svg.append(
                f'<polygon points="{cx_},{cy_-s} {cx_+s*1.8},{cy_} {cx_},{cy_+s} {cx_-s*1.8},{cy_}" '
                f'fill="{COLORS["merge_bg"]}" stroke="{COLORS["merge_bd"]}" stroke-width="1.5"/>'
            )

        elif node['type'] in ('fork', 'join'):
            svg.append(
                f'<rect x="{cx_-60}" y="{cy_-5}" width="120" height="10" '
                f'rx="2" fill="{COLORS["fork_bg"]}"/>'
            )

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
        print("Usage: python3 activity_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    title, nodes, edges = parse_activity(content)
    if not nodes:
        print("No nodes found. Check your ```activity block."); sys.exit(1)
    svg = build_svg(title, nodes, edges)
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + '-activity.html'
    svg_path = os.path.splitext(output_path)[0] + '.svg'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE.replace('{title}', title or 'Activity Diagram').replace('{svg_content}', svg))
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {output_path} ({len(nodes)} nodes, {len(edges)} edges)")
    print(f"Generated: {svg_path} (static, for PDF embedding)")

if __name__ == '__main__':
    main()
