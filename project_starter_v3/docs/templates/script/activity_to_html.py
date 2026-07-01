#!/usr/bin/env python3
"""activity_to_html.py — activity diagram markdown → Interactive HTML + Static SVG

Supports two modes:
  1. Single-column flow  (no lanes: declaration)
  2. Swim lane diagram   (add  lanes: Role A | Role B | Role C)

Swim lane syntax:
  lanes: Sales Person | Consultant | Corporate Technician

  [Sales Person] :Call Client and Setup Appointment;
  if (appointment made?) then (yes)
    [Consultant] :Prepare a Laptop;
    [Consultant] :Meet with the Client;
    if (statement of problem?) then (yes)
      [Consultant] :Create Proposal;
      [Consultant] :Send Proposal to Client;
    else (no)
      [Sales Person] :Send Follow-up Letter;
    endif
  else (no)
    [Corporate Technician] :Prepare a Conference Room;
  endif
  stop

Without lanes:, the diagram renders as a single vertical flow (original behaviour).
"""
import sys, os, re

# ── Parser ────────────────────────────────────────────────────────────────────

def parse_activity(content):
    if '```activity' in content:
        m = re.search(r'```activity\s*(.*?)```', content, re.DOTALL)
        raw = m.group(1) if m else content
    else:
        raw = content

    title = ""
    lanes = []          # ordered lane names; empty = no swim lane
    nodes = []
    edges = []

    def add(node):
        nodes.append(node)
        return len(nodes) - 1

    def connect(src, dst, label=''):
        if src is not None:
            edges.append({'src': src, 'dst': dst, 'label': label})

    branch_stack  = []
    prev          = None
    decision_labels = {}

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('title:'):
            title = line[6:].strip()
            continue
        if line.lower().startswith('lanes:'):
            lanes = [l.strip() for l in line[6:].split('|')]
            continue

        # Detect optional [Lane] prefix on action lines
        lane = None
        lane_m = re.match(r'^\[([^\]]+)\]\s*(.*)', line)
        if lane_m:
            lane = lane_m.group(1).strip()
            line = lane_m.group(2).strip()

        if line == 'start':
            idx = add({'type': 'start', 'lane': lane})
            prev = idx

        elif line == 'stop':
            idx = add({'type': 'stop', 'lane': lane})
            connect(prev, idx)
            prev = idx

        elif re.match(r'^:.+;$', line):
            label = line[1:-1].strip()
            idx = add({'type': 'action', 'label': label, 'lane': lane})
            connect(prev, idx)
            prev = idx

        elif line.lower().startswith('if '):
            m2 = re.match(r'^if\s*\((.+?)\)\s*then\s*\((.+?)\)', line, re.IGNORECASE)
            cond      = m2.group(1) if m2 else line
            yes_label = m2.group(2) if m2 else 'yes'
            idx = add({'type': 'decision', 'label': cond, 'lane': lane})
            connect(prev, idx)
            decision_labels[idx] = {'yes': yes_label}
            branch_stack.append({
                'if_idx':   idx,
                'yes_label': yes_label,
                'yes_end':  None,
            })
            prev = idx

        elif line.lower().startswith('else'):
            m2 = re.match(r'^else\s*\((.+?)\)', line, re.IGNORECASE)
            no_label = m2.group(1) if m2 else 'no'
            if branch_stack:
                frame = branch_stack[-1]
                frame['yes_end'] = prev
                decision_labels.setdefault(frame['if_idx'], {})['no'] = no_label
                prev = frame['if_idx']

        elif line.lower() == 'endif':
            if branch_stack:
                frame = branch_stack.pop()
                merge_idx = add({'type': 'merge', 'lane': None})
                if frame.get('yes_end') is not None:
                    connect(frame['yes_end'], merge_idx)
                if prev != frame['if_idx'] and prev != frame.get('yes_end'):
                    connect(prev, merge_idx)
                prev = merge_idx

        elif line.lower() == 'fork':
            idx = add({'type': 'fork', 'lane': lane})
            connect(prev, idx)
            prev = idx

        elif line.lower() == 'join':
            idx = add({'type': 'join', 'lane': lane})
            connect(prev, idx)
            prev = idx

    # Label decision edges
    dec_seen = {}
    for e in edges:
        src = e['src']
        if src < len(nodes) and nodes[src]['type'] == 'decision' and not e['label']:
            cnt = dec_seen.get(src, 0)
            lbls = decision_labels.get(src, {})
            e['label'] = lbls.get('yes', 'yes') if cnt == 0 else lbls.get('no', 'no')
            dec_seen[src] = cnt + 1

    return title, lanes, nodes, edges


# ── Shared helpers ────────────────────────────────────────────────────────────

COLORS = {
    'bg':        '#F7FAFC',
    'action_bg': '#EBF8FF',
    'action_bd': '#3182CE',
    'action_fg': '#1A365D',
    'dec_bg':    '#FEFCBF',
    'dec_bd':    '#D69E2E',
    'dec_fg':    '#744210',
    'merge_bd':  '#38A169',
    'start_bg':  '#1A365D',
    'stop_bg':   '#1A365D',
    'arrow':     '#4A5568',
    'label_fg':  '#718096',
    'title_fg':  '#1A365D',
    'lane_hd':   '#2D3748',
    'lane_hd_fg':'#FFFFFF',
    'lane_alt':  '#EDF2F7',
    'fork_bg':   '#2D3748',
}

LANE_COLORS = [
    '#EBF8FF',  # blue
    '#F0FFF4',  # green
    '#FFFAF0',  # orange
    '#FAF5FF',  # purple
    '#FFF5F7',  # pink
    '#E6FFFA',  # teal
]

NODE_W  = 160
NODE_H  = 36
V_GAP   = 44
MARGIN  = 50
LINE_H  = 14
CHARS   = 20
DEC_CH  = 14

def wrap(text, max_chars):
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

def node_h(node):
    t = node['type']
    if t == 'action':
        return NODE_H + max(0, len(wrap(node.get('label',''), CHARS)) - 1) * LINE_H
    if t == 'decision':
        ls = wrap(node.get('label',''), DEC_CH)
        s = max(28, 28 * 0.55 * len(ls) + 14)
        return int(s * 2)
    if t == 'merge':
        return 16
    return NODE_H


# ── Single-column layout (original) ──────────────────────────────────────────

def compute_layout_single(nodes, edges):
    n = len(nodes)
    children = {i: [] for i in range(n)}
    for e in edges:
        children[e['src']].append((e['dst'], e['label']))

    visited, order = [False]*n, []
    def topo(i):
        if visited[i]: return
        visited[i] = True
        for j,_ in children[i]: topo(j)
        order.append(i)
    for i in range(n): topo(i)
    order.reverse()

    y = MARGIN + 40
    y_pos = [0]*n
    for i in order:
        y_pos[i] = y
        y += node_h(nodes[i]) + V_GAP

    cx = MARGIN + NODE_W//2 + 60
    x_pos = [cx]*n

    def nudge(i, dx, vis=None):
        if vis is None: vis = set()
        if i in vis: return
        vis.add(i)
        if nodes[i]['type'] == 'merge': return
        x_pos[i] += dx
        for j,_ in children[i]:
            if nodes[j]['type'] != 'merge':
                nudge(j, dx, vis)

    for i, nd in enumerate(nodes):
        if nd['type'] != 'decision': continue
        ch = children[i]
        if len(ch) >= 2:
            nudge(ch[0][0], -NODE_W*0.65)
            nudge(ch[1][0], +NODE_W*0.65)

    total_w = max(x_pos) + NODE_W//2 + MARGIN + 80
    total_h = y + MARGIN
    pos = [{'x': x_pos[i], 'y': y_pos[i], 'h': node_h(nodes[i])} for i in range(n)]
    return pos, int(total_w), int(total_h)


# ── Swim-lane layout ──────────────────────────────────────────────────────────

LANE_W      = 200   # width of each lane column
LANE_HDR_H  = 40    # height of lane header row
SL_MARGIN_X = 20
SL_MARGIN_Y = 20

def lane_cx(lane_idx):
    return SL_MARGIN_X + lane_idx * LANE_W + LANE_W // 2

def compute_layout_swimlane(lanes, nodes, edges):
    n = len(nodes)
    lane_map = {name: i for i, name in enumerate(lanes)}

    # Topological sort
    children = {i: [] for i in range(n)}
    for e in edges:
        children[e['src']].append((e['dst'], e['label']))
    visited, order = [False]*n, []
    def topo(i):
        if visited[i]: return
        visited[i] = True
        for j,_ in children[i]: topo(j)
        order.append(i)
    for i in range(n): topo(i)
    order.reverse()

    # Assign y positions top to bottom
    y = SL_MARGIN_Y + LANE_HDR_H + V_GAP
    y_pos = [0]*n
    for i in order:
        y_pos[i] = y
        y += node_h(nodes[i]) + V_GAP

    # Assign x by lane
    x_pos = []
    for nd in nodes:
        ln = nd.get('lane')
        if ln and ln in lane_map:
            x_pos.append(lane_cx(lane_map[ln]))
        else:
            # No lane specified: centre across all lanes
            x_pos.append(SL_MARGIN_X + len(lanes) * LANE_W // 2)

    total_w = SL_MARGIN_X * 2 + len(lanes) * LANE_W
    total_h = y + SL_MARGIN_Y
    pos = [{'x': x_pos[i], 'y': y_pos[i], 'h': node_h(nodes[i])} for i in range(n)]
    return pos, total_w, total_h


# ── SVG: draw edges (shared) ──────────────────────────────────────────────────

def draw_edges(svg, nodes, edges, pos):
    for e in edges:
        si, di = e['src'], e['dst']
        p1, p2 = pos[si], pos[di]
        n1, n2 = nodes[si], nodes[di]

        # Source anchor
        if n1['type'] == 'start':
            x1, y1 = p1['x'], p1['y'] + 10
        elif n1['type'] == 'decision':
            x1, y1 = p1['x'], p1['y'] + p1['h']//2
        elif n1['type'] == 'merge':
            x1, y1 = p1['x'], p1['y'] + 8
        else:
            x1, y1 = p1['x'], p1['y'] + p1['h']

        # Dest anchor
        if n2['type'] == 'stop':
            x2, y2 = p2['x'], p2['y'] - 10
        elif n2['type'] == 'merge':
            x2, y2 = p2['x'], p2['y'] - 8
        elif n2['type'] == 'decision':
            x2, y2 = p2['x'], p2['y'] - p2['h']//2
        else:
            x2, y2 = p2['x'], p2['y']

        if abs(x1 - x2) > 12:
            mid_y = (y1 + y2) / 2
            path = f'M {x1},{y1} L {x1},{mid_y} L {x2},{mid_y} L {x2},{y2}'
            svg.append(
                f'<path d="{path}" stroke="{COLORS["arrow"]}" stroke-width="1.6" '
                f'fill="none" marker-end="url(#arr)"/>'
            )
            if e.get('label'):
                lx, ly = (x1+x2)/2, mid_y - 6
                for li, ll in enumerate(wrap(e['label'], 18)):
                    safe = ll.replace('&','&amp;').replace('<','&lt;')
                    svg.append(
                        f'<text x="{lx}" y="{ly+li*11}" text-anchor="middle" '
                        f'font-size="9" fill="{COLORS["label_fg"]}">{safe}</text>'
                    )
        else:
            svg.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{COLORS["arrow"]}" stroke-width="1.6" marker-end="url(#arr)"/>'
            )
            if e.get('label'):
                lx, ly = x1+6, (y1+y2)/2
                for li, ll in enumerate(wrap(e['label'], 18)):
                    safe = ll.replace('&','&amp;').replace('<','&lt;')
                    svg.append(
                        f'<text x="{lx}" y="{ly+li*11}" '
                        f'font-size="9" fill="{COLORS["label_fg"]}">{safe}</text>'
                    )


# ── SVG: draw nodes (shared) ──────────────────────────────────────────────────

def draw_nodes(svg, nodes, pos):
    for i, node in enumerate(nodes):
        p = pos[i]
        cx_, cy_, h = p['x'], p['y'], p['h']

        if node['type'] == 'start':
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="10" fill="{COLORS["start_bg"]}"/>')

        elif node['type'] == 'stop':
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="10" fill="{COLORS["stop_bg"]}"/>')
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="6"  fill="{COLORS["bg"]}"/>')
            svg.append(f'<circle cx="{cx_}" cy="{cy_}" r="4"  fill="{COLORS["stop_bg"]}"/>')

        elif node['type'] == 'action':
            x = cx_ - NODE_W//2
            svg.append(
                f'<rect x="{x}" y="{cy_}" width="{NODE_W}" height="{h}" rx="6" '
                f'fill="{COLORS["action_bg"]}" stroke="{COLORS["action_bd"]}" stroke-width="1.8"/>'
            )
            lines = wrap(node['label'], CHARS)
            sy = cy_ + h/2 - (len(lines)-1)*LINE_H/2 + 4
            for li, ll in enumerate(lines):
                safe = ll.replace('&','&amp;').replace('<','&lt;')
                svg.append(
                    f'<text x="{cx_}" y="{sy+li*LINE_H}" text-anchor="middle" '
                    f'font-size="11" fill="{COLORS["action_fg"]}">{safe}</text>'
                )

        elif node['type'] == 'decision':
            s  = h//2
            hw = max(s*1.8, max(len(l) for l in wrap(node['label'], DEC_CH))*5.5)
            svg.append(
                f'<polygon points="{cx_},{cy_-s} {cx_+hw},{cy_} {cx_},{cy_+s} {cx_-hw},{cy_}" '
                f'fill="{COLORS["dec_bg"]}" stroke="{COLORS["dec_bd"]}" stroke-width="1.8"/>'
            )
            lines = wrap(node['label'], DEC_CH)
            sy = cy_ - (len(lines)-1)*6 + 3.5
            for li, ll in enumerate(lines):
                safe = ll.replace('&','&amp;').replace('<','&lt;')
                svg.append(
                    f'<text x="{cx_}" y="{sy+li*12}" text-anchor="middle" '
                    f'font-size="9.5" fill="{COLORS["dec_fg"]}">{safe}</text>'
                )

        elif node['type'] == 'merge':
            svg.append(
                f'<line x1="{cx_-30}" y1="{cy_}" x2="{cx_+30}" y2="{cy_}" '
                f'stroke="{COLORS["merge_bd"]}" stroke-width="3" stroke-linecap="round"/>'
            )

        elif node['type'] in ('fork', 'join'):
            svg.append(
                f'<rect x="{cx_-60}" y="{cy_-5}" width="120" height="10" '
                f'rx="2" fill="{COLORS["fork_bg"]}"/>'
            )


# ── Build SVG: single-column ──────────────────────────────────────────────────

def build_svg_single(title, nodes, edges):
    pos, total_w, total_h = compute_layout_single(nodes, edges)

    svg = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker></defs>',
        f'<rect width="{total_w}" height="{total_h}" fill="{COLORS["bg"]}"/>',
    ]
    if title:
        svg.append(
            f'<text x="{total_w//2}" y="28" text-anchor="middle" font-size="14" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )
    draw_edges(svg, nodes, edges, pos)
    draw_nodes(svg, nodes, pos)
    svg.append('</svg>')
    return '\n'.join(svg)


# ── Build SVG: swim lane ──────────────────────────────────────────────────────

def build_svg_swimlane(title, lanes, nodes, edges):
    pos, total_w, total_h = compute_layout_swimlane(lanes, nodes, edges)
    title_h = 32 if title else 0
    total_h += title_h

    # Shift all y positions down by title height
    for p in pos:
        p['y'] += title_h

    svg = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker></defs>',
        f'<rect width="{total_w}" height="{total_h}" fill="{COLORS["bg"]}"/>',
    ]

    # Title
    if title:
        svg.append(
            f'<text x="{total_w//2}" y="22" text-anchor="middle" font-size="14" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # Lane backgrounds and headers
    lane_top = title_h + SL_MARGIN_Y
    for i, lane_name in enumerate(lanes):
        lx = SL_MARGIN_X + i * LANE_W
        bg = LANE_COLORS[i % len(LANE_COLORS)]
        # Background stripe
        svg.append(
            f'<rect x="{lx}" y="{lane_top + LANE_HDR_H}" width="{LANE_W}" '
            f'height="{total_h - lane_top - LANE_HDR_H}" fill="{bg}" opacity="0.4"/>'
        )
        # Header box
        svg.append(
            f'<rect x="{lx}" y="{lane_top}" width="{LANE_W}" height="{LANE_HDR_H}" '
            f'fill="{COLORS["lane_hd"]}" rx="0"/>'
        )
        safe_name = lane_name.replace('&','&amp;').replace('<','&lt;')
        svg.append(
            f'<text x="{lx + LANE_W//2}" y="{lane_top + LANE_HDR_H//2 + 5}" '
            f'text-anchor="middle" font-size="12" font-weight="bold" '
            f'fill="{COLORS["lane_hd_fg"]}">{safe_name}</text>'
        )
        # Vertical divider
        if i > 0:
            svg.append(
                f'<line x1="{lx}" y1="{lane_top}" x2="{lx}" y2="{total_h}" '
                f'stroke="#CBD5E0" stroke-width="1" stroke-dasharray="4,3"/>'
            )

    # Outer border
    svg.append(
        f'<rect x="{SL_MARGIN_X}" y="{lane_top}" width="{len(lanes)*LANE_W}" '
        f'height="{total_h - lane_top}" fill="none" stroke="#CBD5E0" stroke-width="1.5" rx="4"/>'
    )

    draw_edges(svg, nodes, edges, pos)
    draw_nodes(svg, nodes, pos)
    svg.append('</svg>')
    return '\n'.join(svg)


# ── Dispatcher ────────────────────────────────────────────────────────────────

def build_svg(title, lanes, nodes, edges):
    if lanes:
        return build_svg_swimlane(title, lanes, nodes, edges)
    return build_svg_single(title, nodes, edges)


# ── HTML wrapper ──────────────────────────────────────────────────────────────

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

def build_html(title, svg):
    return HTML_TEMPLATE.replace('{title}', title or 'Activity Diagram').replace('{svg_content}', svg)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 activity_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path = sys.argv[1]
    base_output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = list(re.finditer(r'```activity\s*(.*?)```', content, re.DOTALL))
    if not blocks:
        print("No ```activity block found. Check your syntax."); sys.exit(1)

    base_stem = os.path.splitext(base_output or input_path)[0]
    if base_stem.endswith('-activity'):
        base_stem = base_stem[:-len('-activity')]

    generated = 0
    for idx, match in enumerate(blocks):
        result = parse_activity(match.group(1))
        title = result[0] or ""

        if len(blocks) == 1:
            out_stem = base_stem
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') if title else str(idx+1)
            out_stem = base_stem + f'-{slug}'

        output_path = out_stem + '-activity.html'
        svg_path    = out_stem + '-activity.svg'

        svg = build_svg(*result)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(build_html(title, svg))
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg)

        mode = 'swim lane' if result[1] else 'single-column'
        print(f"Generated: {output_path} ({mode}, {len(result[2])} nodes)")
        print(f"Generated: {svg_path} (static, for PDF embedding)")
        generated += 1

    if generated > 1:
        print(f"\nTotal: {generated} diagrams from {os.path.basename(input_path)}")


if __name__ == '__main__':
    main()
