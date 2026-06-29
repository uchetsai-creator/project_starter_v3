#!/usr/bin/env python3
"""sequence_to_html.py — sequence diagram markdown → Interactive HTML + Static SVG

Input format (inside a markdown file):
```sequence
title: Create Order Flow

Client -> API Gateway: POST /orders [auth token]
API Gateway -> Order Service: create(input)
Order Service -> PostgreSQL: INSERT order
PostgreSQL --> Order Service: order record
Order Service -> Message Queue: publish OrderCreated
Message Queue --> Order Service: ack
Order Service --> API Gateway: 201 Created
API Gateway --> Client: 201 {orderId}
```

Syntax rules:
  A -> B: message        synchronous call (solid arrow →)
  A --> B: message       return / async response (dashed arrow ⇢)
  A -x B: message        failed call (solid arrow with X)
  # comment              ignored
  title: <text>          optional diagram title

Outputs:
  <name>.html  — interactive (hover to highlight, pan/zoom)
  <name>.svg   — static (for PDF embedding)

Usage:
  python3 sequence_to_html.py <input.md> [-o output.html]
"""
import sys, os, re, math, json

# ── Parser ──────────────────────────────────────────────────────────────────

def parse_sequence(content):
    # Accept either a full markdown file or a raw block string
    if '```sequence' in content:
        _m = re.search(r'```sequence\s*(.*?)```', content, re.DOTALL)
        raw = _m.group(1) if _m else content
    else:
        raw = content

    title = ""
    participants = []
    seen = {}
    messages = []

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.lower().startswith('title:'):
            title = line[6:].strip()
            continue

        # A -> B: msg  |  A --> B: msg  |  A -x B: msg
        m = re.match(r'^(.+?)\s*(-->|-x|->)\s*(.+?):\s*(.*)$', line)
        if m:
            src, arrow, dst, msg = m.group(1).strip(), m.group(2), m.group(3).strip(), m.group(4).strip()
            for p in (src, dst):
                if p not in seen:
                    seen[p] = len(participants)
                    participants.append(p)
            kind = 'return' if arrow == '-->' else ('fail' if arrow == '-x' else 'call')
            messages.append({'src': src, 'dst': dst, 'msg': msg, 'kind': kind})

    return title, participants, messages


# ── SVG builder ─────────────────────────────────────────────────────────────

COLORS = {
    'head_bg':   '#1A365D',
    'head_fg':   '#FFFFFF',
    'life_line': '#CBD5E0',
    'call':      '#3182CE',
    'return':    '#718096',
    'fail':      '#E53E3E',
    'box_bg':    '#EBF8FF',
    'box_bd':    '#BEE3F8',
    'bg':        '#F7FAFC',
    'msg_fg':    '#2D3748',
    'self_bg':   '#FEF3C7',
}

BOX_W, BOX_H = 120, 32
H_GAP = 60   # horizontal gap between participant centres
V_START = 70  # y where lifelines start
MSG_H = 44   # vertical space per message
MARGIN = 40


def build_svg(title, participants, messages):
    n = len(participants)
    centres = [MARGIN + BOX_W // 2 + i * (BOX_W + H_GAP) for i in range(n)]
    idx = {p: i for i, p in enumerate(participants)}

    total_w = centres[-1] + BOX_W // 2 + MARGIN if centres else 400
    total_h = V_START + (len(messages) + 1) * MSG_H + 40

    parts = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{total_w}" height="{total_h}" fill="{COLORS["bg"]}"/>',
    ]

    # Title
    if title:
        parts.append(
            f'<text x="{total_w//2}" y="22" text-anchor="middle" '
            f'font-size="14" font-weight="bold" fill="{COLORS["head_bg"]}">{title}</text>'
        )

    # Participant boxes
    for i, p in enumerate(participants):
        cx = centres[i]
        x = cx - BOX_W // 2
        parts.append(
            f'<rect x="{x}" y="{V_START - BOX_H}" width="{BOX_W}" height="{BOX_H}" '
            f'rx="6" fill="{COLORS["head_bg"]}"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{V_START - BOX_H//2 + 5}" text-anchor="middle" '
            f'fill="{COLORS["head_fg"]}" font-size="11" font-weight="bold">{p}</text>'
        )

    # Lifelines
    life_end = V_START + (len(messages) + 1) * MSG_H
    for cx in centres:
        parts.append(
            f'<line x1="{cx}" y1="{V_START}" x2="{cx}" y2="{life_end}" '
            f'stroke="{COLORS["life_line"]}" stroke-width="1.5" stroke-dasharray="4,3"/>'
        )

    # Messages
    for mi, msg in enumerate(messages):
        y = V_START + (mi + 1) * MSG_H
        si, di = idx[msg['src']], idx[msg['dst']]
        x1, x2 = centres[si], centres[di]
        color = COLORS[msg['kind']]
        dash = '6,3' if msg['kind'] == 'return' else ''
        label = msg['msg']

        if si == di:
            # Self-call loop
            lx = x1 + 12
            parts.append(
                f'<path d="M {x1},{y} Q {x1+50},{y} {x1+50},{y+15} Q {x1+50},{y+30} {x1},{y+30}" '
                f'stroke="{color}" stroke-width="1.8" fill="none"'
                + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
            )
            parts.append(
                f'<polygon points="{x1},{y+30} {x1-5},{y+22} {x1+5},{y+22}" fill="{color}"/>'
            )
            parts.append(
                f'<text x="{x1+54}" y="{y+16}" font-size="10" fill="{COLORS["msg_fg"]}">{label}</text>'
            )
        else:
            mx = (x1 + x2) / 2
            parts.append(
                f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
                f'stroke="{color}" stroke-width="1.8"'
                + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
            )
            # Arrowhead
            if msg['kind'] == 'fail':
                parts.append(f'<text x="{x2-8 if x2>x1 else x2+2}" y="{y+5}" font-size="13" fill="{color}">✕</text>')
            else:
                direction = 1 if x2 > x1 else -1
                ax = x2 - direction * 10
                parts.append(
                    f'<polygon points="{x2},{y} {ax},{y-5} {ax},{y+5}" fill="{color}"/>'
                )
            # Label
            parts.append(
                f'<rect x="{mx-50}" y="{y-16}" width="100" height="16" rx="3" '
                f'fill="{COLORS["box_bg"]}" stroke="{COLORS["box_bd"]}" stroke-width="0.8"/>'
            )
            parts.append(
                f'<text x="{mx}" y="{y-4}" text-anchor="middle" font-size="9.5" '
                f'fill="{COLORS["msg_fg"]}">{label}</text>'
            )

    parts.append('</svg>')
    return '\n'.join(parts)


# ── Interactive HTML ─────────────────────────────────────────────────────────

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
.msg-hit {{ cursor: pointer; }}
.msg-hit:hover rect {{ fill: #BEE3F8; }}
#tooltip {{
  position: fixed; background: #2D3748; color: #E2E8F0;
  font-size: 11px; padding: 6px 10px; border-radius: 6px;
  pointer-events: none; display: none; z-index: 999;
  border: 1px solid #4A5568; white-space: nowrap;
}}
#hint {{
  position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%);
  background: #2D3748; color: #90CDF4; font-size: 11px;
  padding: 5px 14px; border-radius: 20px; pointer-events: none;
  z-index: 999; border: 1px solid #4A5568;
}}
</style>
</head>
<body>
<div id="wrap">
  <div id="stage">
    {svg_content}
  </div>
</div>
<div id="tooltip"></div>
<div id="hint">Scroll to zoom · Drag to pan</div>
<script>
const wrap = document.getElementById('wrap');
let scale = 1, px = 0, py = 0;
let panning = false, lmx = 0, lmy = 0;

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
window.addEventListener('mouseup', () => {{ panning = false; }});
window.addEventListener('mousemove', e => {{
  if (panning) {{ px += e.clientX - lmx; py += e.clientY - lmy; lmx = e.clientX; lmy = e.clientY; applyT(); }}
}});

function applyT() {{
  document.getElementById('stage').style.transform = `translate(${{px}}px,${{py}}px) scale(${{scale}})`;
}}
</script>
</body>
</html>"""


def build_html(title, svg_content):
    return HTML_TEMPLATE.replace('{title}', title or 'Sequence Diagram').replace('{svg_content}', svg_content)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sequence_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path = sys.argv[1]
    base_output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find ALL ```sequence blocks in the file
    blocks = list(re.finditer(r'```sequence\s*(.*?)```', content, re.DOTALL))
    if not blocks:
        print("No ```sequence block found. Check your syntax."); sys.exit(1)

    # Strip existing suffix from base stem to avoid doubling (e.g. file-sequence-sequence.html)
    base_stem = os.path.splitext(base_output or input_path)[0]
    if base_stem.endswith('-sequence'):
        base_stem = base_stem[:-len('-sequence')]

    generated = 0

    for idx, match in enumerate(blocks):
        result = parse_sequence(match.group(1))
        title  = result[0] or ""

        # Single block → keep original naming; multiple → append title slug or index
        if len(blocks) == 1:
            out_stem = base_stem
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') if title else str(idx + 1)
            out_stem = base_stem + f'-{slug}'

        output_path = out_stem + '-sequence.html'
        svg_path    = out_stem + '-sequence.svg'

        svg        = build_svg(*result)
        html_title = title or 'Sequence Diagram'

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
