#!/usr/bin/env python3
"""component_to_html.py — Component diagram → Interactive HTML + Static SVG

Supports package grouping (recommended for projects with 5+ components):

```component
title: Frontend Architecture

package "Presentation" {
  component "DashboardPage" as Dashboard {
    provides: KPI cards, chart widgets
    requires: API Client, RealtimeProvider
  }
  component "ReportsPage" as Reports {
    provides: Period selector, chart suite
    requires: API Client
  }
  component "AlarmCenterPage" as Alarm {
    provides: Alarm list, detail panel
    requires: API Client, RealtimeProvider
  }
}

package "Application" {
  component "RealtimeProvider" as RT {
    provides: Socket.IO typed events
    requires: Backend Socket.IO
  }
  component "PreferencesProvider" as Pref {
    provides: theme, language, KPI layout
    requires: localStorage
  }
}

package "Infrastructure" {
  component "API Client" as API {
    provides: HTTP methods, error handling
    requires: Backend REST API
  }
}

Dashboard --> API
Dashboard --> RT
Reports   --> API
Alarm     --> API
Alarm     --> RT
```

Rules:
  - Only draw REAL compile-time/import dependencies (not router navigation)
  - Pages should depend on services/providers, not other pages
  - Use packages to group components by layer (Presentation/Application/Infrastructure)
  - Keep provides/requires brief — 2-4 items max, no internal method names
  - One direction only: A --> B means A depends on B (never draw B --> A as well unless truly mutual)
"""
import sys, os, re, math

COLORS = {
    'bg':        '#F8FAFC',
    'card_bg':   '#FFFFFF',
    'card_bd':   '#CBD5E0',
    'head_bg':   '#2D3748',
    'head_fg':   '#FFFFFF',
    'prov_fg':   '#276749',
    'req_fg':    '#C53030',
    'sec_fg':    '#718096',
    'arrow':     '#4A5568',
    'label_fg':  '#718096',
    'title_fg':  '#1A365D',
    'pkg_bd':    '#90CDF4',
    'pkg_label': '#2B6CB0',
}

PKG_BG = [
    '#EBF8FF',  # blue
    '#F0FFF4',  # green
    '#FFFAF0',  # orange
    '#FAF5FF',  # purple
    '#FFF5F7',  # pink
    '#E6FFFA',  # teal
]

CARD_W   = 200
HEAD_H   = 36
IFACE_H  = 18
MARGIN   = 40
H_GAP    = 28   # gap between cards
V_GAP    = 28   # gap between rows
PKG_PAD  = 20   # padding inside package
PKG_HEAD = 28   # package header height


def wrap_text(text, max_chars=22):
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


def card_height(comp):
    prov_lines = sum(len(wrap_text(p, max_chars=22)) for p in comp.get('provides', []))
    req_lines  = sum(len(wrap_text(r, max_chars=22)) for r in comp.get('requires', []))
    sections = (1 if comp.get('provides') else 0) + (1 if comp.get('requires') else 0)
    return HEAD_H + (prov_lines + req_lines + sections) * IFACE_H + 8


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_component(content):
    if '```component' in content:
        m = re.search(r'```component\s*(.*?)```', content, re.DOTALL)
        raw = m.group(1) if m else content
    else:
        raw = content

    title      = ""
    packages   = {}    # pkg_name -> [alias, ...]
    components = {}    # alias -> {label, provides, requires, package}
    relations  = []    # {src, dst, label}

    lines = raw.splitlines()
    i = 0
    current_pkg = None

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1; continue
        if line.lower().startswith('title:'):
            title = line[6:].strip(); i += 1; continue

        # package "Name" {
        pm = re.match(r'^package\s+"([^"]+)"\s*\{?', line)
        if pm:
            current_pkg = pm.group(1)
            if current_pkg not in packages:
                packages[current_pkg] = []
            i += 1; continue

        # closing brace (could be package or component)
        if line == '}':
            # Heuristic: if we're in a component context inside a line scan, skip
            # This is handled below in component parsing
            i += 1; continue

        # component "Label" as ALIAS { ... }
        cm = re.match(r'^component\s+"([^"]+)"\s+as\s+(\w+)\s*\{?', line)
        if cm:
            label, alias = cm.group(1), cm.group(2)
            comp = {'label': label, 'provides': [], 'requires': [], 'package': current_pkg}
            if '{' in line:
                i += 1
                while i < len(lines):
                    inner = lines[i].strip()
                    if inner == '}':
                        i += 1; break
                    if inner.lower().startswith('provides:'):
                        items = [x.strip() for x in inner[9:].split(',') if x.strip()]
                        comp['provides'].extend(items)
                    elif inner.lower().startswith('requires:'):
                        items = [x.strip() for x in inner[9:].split(',') if x.strip()]
                        comp['requires'].extend(items)
                    i += 1
            else:
                i += 1
            components[alias] = comp
            if current_pkg:
                packages[current_pkg].append(alias)
            continue

        # A --> B : label  or  A --> B
        rm = re.match(r'^(\w+)\s*-->\s*(\w+)(?:\s*:\s*(.*))?$', line)
        if rm:
            relations.append({'src': rm.group(1), 'dst': rm.group(2),
                               'label': (rm.group(3) or '').strip()})
            i += 1; continue

        i += 1

    return title, packages, components, relations


# ── Layout ────────────────────────────────────────────────────────────────────

def compute_layout(packages, components):
    """
    If packages are defined: lay out packages in a vertical stack,
    components within each package arranged horizontally.
    If no packages: arrange components in a grid.
    """
    pos = {}   # alias -> {x, y}
    pkg_rects = {}  # pkg_name -> {x, y, w, h}

    if packages:
        # Stack packages vertically, components side by side within each package
        y = MARGIN + 40
        pkg_names = list(packages.keys())

        for pi, pkg_name in enumerate(pkg_names):
            aliases = packages[pkg_name]
            if not aliases:
                continue

            # Compute row height (max card height in this package)
            max_h = max((card_height(components[a]) for a in aliases if a in components), default=100)

            pkg_w = len(aliases) * (CARD_W + H_GAP) - H_GAP + PKG_PAD * 2
            pkg_h = max_h + PKG_HEAD + PKG_PAD * 2

            pkg_x = MARGIN
            pkg_rects[pkg_name] = {'x': pkg_x, 'y': y, 'w': pkg_w, 'h': pkg_h, 'idx': pi}

            # Position cards inside package
            cx = pkg_x + PKG_PAD
            for alias in aliases:
                if alias in components:
                    pos[alias] = {'x': cx, 'y': y + PKG_HEAD + PKG_PAD}
                    cx += CARD_W + H_GAP

            y += pkg_h + V_GAP * 2

        # Handle unpackaged components
        unpackaged = [a for a in components if not components[a].get('package')]
        if unpackaged:
            cx = MARGIN
            for alias in unpackaged:
                pos[alias] = {'x': cx, 'y': y}
                cx += CARD_W + H_GAP
            pkg_h = max((card_height(components[a]) for a in unpackaged), default=100)
            y += pkg_h + V_GAP

        total_w = max(
            (r['x'] + r['w'] for r in pkg_rects.values()),
            default=MARGIN + 300
        ) + MARGIN
        total_h = y + MARGIN

    else:
        # No packages: grid layout
        aliases = list(components.keys())
        cols = min(3, max(1, math.ceil(math.sqrt(len(aliases)))))
        max_h = max((card_height(components[a]) for a in aliases), default=100)

        for i, alias in enumerate(aliases):
            col = i % cols
            row = i // cols
            x = MARGIN + col * (CARD_W + H_GAP)
            y = MARGIN + 40 + row * (max_h + V_GAP * 2)
            pos[alias] = {'x': x, 'y': y}

        total_w = MARGIN + cols * (CARD_W + H_GAP) + MARGIN
        total_h = MARGIN + 40 + (math.ceil(len(aliases) / cols)) * (max_h + V_GAP * 2) + MARGIN

    return pos, pkg_rects, int(total_w), int(total_h)


# ── SVG builder ───────────────────────────────────────────────────────────────

def build_svg(title, packages, components, relations):
    pos, pkg_rects, total_w, total_h = compute_layout(packages, components)
    title_h = 32 if title else 0
    total_h += title_h

    for p in pos.values():
        p['y'] += title_h
    for r in pkg_rects.values():
        r['y'] += title_h

    svg = [
        f'<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="Segoe UI, Arial, sans-serif">',
        f'<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{COLORS["arrow"]}"/></marker></defs>',
        f'<rect width="{total_w}" height="{total_h}" fill="{COLORS["bg"]}"/>',
    ]

    if title:
        svg.append(
            f'<text x="{total_w//2}" y="24" text-anchor="middle" font-size="15" '
            f'font-weight="bold" fill="{COLORS["title_fg"]}">{title}</text>'
        )

    # ── Package backgrounds ───────────────────────────────────────────────────
    for pkg_name, r in pkg_rects.items():
        bg = PKG_BG[r['idx'] % len(PKG_BG)]
        svg.append(
            f'<rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" '
            f'rx="10" fill="{bg}" stroke="{COLORS["pkg_bd"]}" stroke-width="1.5"/>'
        )
        safe_pkg = pkg_name.replace('&', '&amp;').replace('<', '&lt;')
        svg.append(
            f'<text x="{r["x"]+12}" y="{r["y"]+18}" font-size="11" font-weight="bold" '
            f'font-style="italic" fill="{COLORS["pkg_label"]}">{safe_pkg}</text>'
        )

    # ── Relations ─────────────────────────────────────────────────────────────
    for rel in relations:
        src, dst = rel['src'], rel['dst']
        if src not in pos or dst not in pos:
            continue
        p1, p2 = pos[src], pos[dst]
        h1 = card_height(components[src])
        h2 = card_height(components[dst])

        # Source: bottom-centre of card
        x1 = p1['x'] + CARD_W // 2
        y1 = p1['y'] + h1

        # Destination: top-centre of card (or closest edge)
        x2 = p2['x'] + CARD_W // 2
        y2 = p2['y']

        # If on same vertical level, use side anchors
        if abs(p1['y'] - p2['y']) < 30:
            if p1['x'] < p2['x']:
                x1 = p1['x'] + CARD_W; y1 = p1['y'] + h1 // 2
                x2 = p2['x'];           y2 = p2['y'] + h2 // 2
            else:
                x1 = p1['x'];           y1 = p1['y'] + h1 // 2
                x2 = p2['x'] + CARD_W; y2 = p2['y'] + h2 // 2

        if abs(x1 - x2) > 20 and abs(y1 - y2) > 20:
            mid_y = (y1 + y2) / 2
            path = f'M {x1},{y1} L {x1},{mid_y} L {x2},{mid_y} L {x2},{y2}'
            svg.append(
                f'<path d="{path}" stroke="{COLORS["arrow"]}" stroke-width="1.4" '
                f'fill="none" stroke-dasharray="6,3" marker-end="url(#arr)"/>'
            )
        else:
            svg.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{COLORS["arrow"]}" stroke-width="1.4" '
                f'stroke-dasharray="6,3" marker-end="url(#arr)"/>'
            )

        if rel.get('label'):
            mx, my = (x1+x2)/2 + 6, (y1+y2)/2
            safe_lbl = rel['label'].replace('&', '&amp;').replace('<', '&lt;')
            svg.append(
                f'<text x="{mx}" y="{my}" font-size="9" fill="{COLORS["label_fg"]}">{safe_lbl}</text>'
            )

    # ── Component cards ───────────────────────────────────────────────────────
    for alias, comp in components.items():
        if alias not in pos:
            continue
        p = pos[alias]
        x, y = p['x'], p['y']
        h = card_height(comp)

        # Card border
        svg.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{h}" rx="6" '
            f'fill="{COLORS["card_bg"]}" stroke="{COLORS["card_bd"]}" stroke-width="1.2"/>'
        )
        # Header
        svg.append(
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{HEAD_H}" rx="6" '
            f'fill="{COLORS["head_bg"]}"/>'
        )
        svg.append(
            f'<rect x="{x}" y="{y+HEAD_H-6}" width="{CARD_W}" height="6" fill="{COLORS["head_bg"]}"/>'
        )
        # Component icon (⊞) + label
        safe_label = comp['label'].replace('&', '&amp;').replace('<', '&lt;')
        svg.append(
            f'<text x="{x+CARD_W//2}" y="{y+HEAD_H//2+5}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="{COLORS["head_fg"]}">⊞ {safe_label}</text>'
        )

        cy = y + HEAD_H + 4
        if comp.get('provides'):
            svg.append(
                f'<text x="{x+6}" y="{cy+IFACE_H//2+4}" font-size="8.5" '
                f'fill="{COLORS["sec_fg"]}" font-style="italic">provides</text>'
            )
            cy += IFACE_H
            for prov in comp['provides']:
                prov_lines = wrap_text(prov, max_chars=22)
                for li, pl in enumerate(prov_lines):
                    safe_pl = pl.replace('&', '&amp;').replace('<', '&lt;')
                    prefix = '▸ ' if li == 0 else '  '
                    svg.append(
                        f'<text x="{x+12}" y="{cy+IFACE_H//2+4+li*11}" font-size="10" '
                        f'fill="{COLORS["prov_fg"]}">{prefix}{safe_pl}</text>'
                    )
                cy += IFACE_H + (len(prov_lines)-1)*11

        if comp.get('requires'):
            svg.append(
                f'<text x="{x+6}" y="{cy+IFACE_H//2+4}" font-size="8.5" '
                f'fill="{COLORS["sec_fg"]}" font-style="italic">requires</text>'
            )
            cy += IFACE_H
            for req in comp['requires']:
                req_lines = wrap_text(req, max_chars=22)
                for li, rl in enumerate(req_lines):
                    safe_rl = rl.replace('&', '&amp;').replace('<', '&lt;')
                    prefix = '◂ ' if li == 0 else '  '
                    svg.append(
                        f'<text x="{x+12}" y="{cy+IFACE_H//2+4+li*11}" font-size="10" '
                        f'fill="{COLORS["req_fg"]}">{prefix}{safe_rl}</text>'
                    )
                cy += IFACE_H + (len(req_lines)-1)*11

    svg.append('</svg>')
    return '\n'.join(svg)


# ── HTML wrapper ──────────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{title}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0;}}body{{font-family:'Segoe UI',Arial,sans-serif;background:#F8FAFC;overflow:hidden;}}#wrap{{position:fixed;inset:0;overflow:hidden;cursor:grab;}}#wrap:active{{cursor:grabbing;}}#stage{{position:absolute;transform-origin:0 0;padding:24px;}}#hint{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:#2D3748;color:#90CDF4;font-size:11px;padding:5px 14px;border-radius:20px;pointer-events:none;z-index:999;}}</style>
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
    return HTML_TEMPLATE.replace('{title}', title or 'Component Diagram').replace('{svg_content}', svg)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 component_to_html.py <input.md> [-o output.html]"); sys.exit(1)
    input_path  = sys.argv[1]
    base_output = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '-o' else None

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}"); sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = list(re.finditer(r'```component\s*(.*?)```', content, re.DOTALL))
    if not blocks:
        print("No ```component block found. Check your syntax."); sys.exit(1)

    base_stem = os.path.splitext(base_output or input_path)[0]
    if base_stem.endswith('-component'):
        base_stem = base_stem[:-len('-component')]

    generated = 0
    for idx, match in enumerate(blocks):
        result = parse_component(match.group(1))
        title  = result[0] or ""

        if len(blocks) == 1:
            out_stem = base_stem
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') if title else str(idx+1)
            out_stem = base_stem + f'-{slug}'

        output_path = out_stem + '-component.html'
        svg_path    = out_stem + '-component.svg'

        svg = build_svg(*result)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(build_html(title, svg))
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg)

        _, pkgs, comps, _ = result
        mode = f'{len(pkgs)} packages, ' if pkgs else ''
        print(f"Generated: {output_path} ({mode}{len(comps)} components)")
        print(f"Generated: {svg_path} (static, for PDF embedding)")
        generated += 1

    if generated > 1:
        print(f"\nTotal: {generated} diagrams from {os.path.basename(input_path)}")


if __name__ == '__main__':
    main()
