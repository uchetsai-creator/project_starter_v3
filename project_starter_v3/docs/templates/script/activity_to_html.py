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
    # Accept either a full markdown file or a raw block string
    if '```activity' in content:
        _m = re.search(r'```activity\s*(.*?)```', content, re.DOTALL)
        raw = _m.group(1) if _m else content
    else:
        raw = content

    title = ""
    nodes = []   # list of node dicts
    edges = []   # list of {src, dst, label}

    def add(node):
        nodes.append(node)
        return len(nodes) - 1

    branch_stack = []  # stack of {if_idx, else_idx, ends: []}
    decision_labels = {}  # decision node idx -> {'yes': label, 'no': label}
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
            decision_labels[idx] = {'yes': yes_label}
            prev = idx

        elif line.lower().startswith('else'):
            m = re.match(r'^else\s*\((.+?)\)', line, re.IGNORECASE)
            no_label = m.group(1) if m else 'no'
            if branch_stack:
                branch_stack[-1]['prev_else'] = prev
                branch_stack[-1]['no_label'] = no_label
                if_idx = branch_stack[-1]['if_idx']
                if if_idx in decision_labels:
                    decision_labels[if_idx]['no'] = no_label
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
            labels = decision_labels.get(src, {})
            if count == 0:
                e['label'] = labels.get('yes', 'yes')
            else:
                e['label'] = labels.get('no', 'no')
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


def wrap_text(text, max_chars=22):
    """Wrap text into multiple lines at word boundaries, max_chars per line."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > max_chars and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [text]


def node_height(label, base_height=NODE_H, line_height=14, max_chars=22):
    """Compute the height needed for a node based on wrapped text line count."""
    lines = wrap_text(label, max_chars)
    extra_lines = max(0, len(lines) - 1)
    return base_height + extra_lines * line_height



def build_svg(title, nodes, edges):
    cx = MARGIN + NODE_W // 2
    positions = []
    heights = []
    y = MARGIN + 40
    for node in nodes:
        label = node.get('label', '')
        h = node_height(label) if node['type'] in ('action', 'decision') else NODE_H
        heights.append(h)
        positions.append({'x': cx, 'y': y, 'h': h})
        y += V_STEP + h

    # Decision diamonds can be wider than NODE_W when labels are long — widen canvas to fit
    max_label_chars = max((len(n.get('label', '')) for n in nodes if n['type'] == 'decision'), default=0)
    decision_extra_w = max(0, max_label_chars * 5.5 - NODE_W // 2) if max_label_chars else 0
    total_w = NODE_W + MARGIN * 2 + int(decision_extra_w * 2)
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
        x1, y1 = p1['x'], p1['y'] + p1['h'] // 2
        x2, y2 = p2['x'], p2['y'] - p2['h'] // 2
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
            label_lines = wrap_text(e['label'], max_chars=18)
            for li, lline in enumerate(label_lines):
                safe_lline = lline.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                svg.append(
                    f'<text x="{mx+6}" y="{my + li * 11}" font-size="9" fill="{COLORS["label_fg"]}">{safe_lline}</text>'
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
            h = p['h']
            x = cx_ - NODE_W // 2
            y = cy_ - h // 2
            svg.append(
                f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{h}" rx="6" '
                f'fill="{COLORS["action_bg"]}" stroke="{COLORS["action_bd"]}" stroke-width="1.8"/>'
            )
            lines = wrap_text(node['label'])
            line_h = 14
            start_y = cy_ - (len(lines) - 1) * line_h / 2 + 4
            for li, line in enumerate(lines):
                safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                svg.append(
                    f'<text x="{cx_}" y="{start_y + li * line_h}" text-anchor="middle" font-size="11" '
                    f'fill="{COLORS["action_fg"]}">{safe_line}</text>'
                )

        elif node['type'] == 'decision':
            lines = wrap_text(node['label'], max_chars=16)
            # Scale diamond size to fit wrapped text — widen and heighten for longer labels
            s = max(DEC_SIZE, DEC_SIZE * 0.55 * len(lines) + 14)
            longest_line = max((len(l) for l in lines), default=1)
            half_w = max(s * 1.8, longest_line * 5.5)
            svg.append(
                f'<polygon points="{cx_},{cy_-s} {cx_+half_w},{cy_} {cx_},{cy_+s} {cx_-half_w},{cy_}" '
                f'fill="{COLORS["dec_bg"]}" stroke="{COLORS["dec_bd"]}" stroke-width="1.8"/>'
            )
            line_h = 12
            start_y = cy_ - (len(lines) - 1) * line_h / 2 + 3.5
            for li, line in enumerate(lines):
                safe = line.replace('&', '&amp;').replace('<', '&lt;')
                svg.append(
                    f'<text x="{cx_}" y="{start_y + li * line_h}" text-anchor="middle" font-size="9.5" '
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
    base_output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find ALL ```activity blocks in the file
    blocks = list(re.finditer(r'```activity\s*(.*?)```', content, re.DOTALL))
    if not blocks:
        print("No ```activity block found. Check your syntax."); sys.exit(1)

    # Strip existing suffix from base stem to avoid doubling (e.g. file-activity-activity.html)
    base_stem = os.path.splitext(base_output or input_path)[0]
    if base_stem.endswith('-activity'):
        base_stem = base_stem[:-len('-activity')]

    generated = 0

    for idx, match in enumerate(blocks):
        result = parse_activity(match.group(1))
        title  = result[0] or ""

        # Single block → keep original naming; multiple → append title slug or index
        if len(blocks) == 1:
            out_stem = base_stem
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') if title else str(idx + 1)
            out_stem = base_stem + f'-{slug}'

        output_path = out_stem + '-activity.html'
        svg_path    = out_stem + '-activity.svg'

        svg        = build_svg(*result)
        html_title = title or 'Activity Diagram'

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
