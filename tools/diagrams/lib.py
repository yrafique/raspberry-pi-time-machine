"""A tiny SVG design system for the guide's diagrams.

Look: dark glass panels, gradient icon tiles, tight system typography, soft glows.
Motion: connectors flow gently; everything stops under prefers-reduced-motion.
Every diagram is a self-contained SVG, so it reads the same in GitHub's light and dark themes.
"""
import html
import math
import re

FONT = "-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"

# name: (light, deep) gradient stops, plus a solid accent
PAL = {
    "blue":   ("#4FB3FF", "#0A6CFF"),
    "teal":   ("#7CE0FF", "#1FA6E0"),
    "green":  ("#5BE584", "#1FA54A"),
    "orange": ("#FFC24B", "#FF8A00"),
    "red":    ("#FF7A70", "#E0281F"),
    "purple": ("#D58BFF", "#8F3FD0"),
    "pink":   ("#FF8FB8", "#E03A7C"),
    "gray":   ("#A9ADB8", "#5F6572"),
    "indigo": ("#8B8CFF", "#4B4DE0"),
}
ACCENT = {k: v[0] for k, v in PAL.items()}

INK = "#F5F5F7"      # primary text
INK2 = "#A7ADBB"     # secondary text
INK3 = "#6E7587"     # tertiary text

ICONS = {
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="2"/><path d="M2 19.5h20"/>',
    "pi": '<rect x="3" y="6" width="18" height="12" rx="2.5"/><rect x="6" y="9.5" width="5" height="5" rx="1"/><path d="M14 9.5h4M14 12h4M14 14.5h4"/>',
    "drive": '<rect x="4" y="3.5" width="16" height="17" rx="3.5"/><circle cx="12" cy="10.5" r="3.2"/><path d="M8 17h3"/><circle cx="16.5" cy="17" r=".7" fill="#fff"/>',
    "wifi": '<path d="M3.5 9.5a12 12 0 0 1 17 0"/><path d="M6.7 12.7a7.5 7.5 0 0 1 10.6 0"/><path d="M9.9 15.9a3 3 0 0 1 4.2 0"/><circle cx="12" cy="19" r="1" fill="#fff"/>',
    "router": '<rect x="3" y="13" width="18" height="6.5" rx="2.5"/><path d="M7.5 16.2h.01M11 16.2h.01"/><path d="M8 9.5a5.5 5.5 0 0 1 8 0"/><path d="M5.5 7a9 9 0 0 1 13 0"/>',
    "folder": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "shield": '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l8.5-8.5M16 7l3 3M14 9l2 2"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L20.5 20.5"/>',
    "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 5v6h-6"/>',
    "warn": '<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.3" r=".8" fill="#fff"/>',
    "terminal": '<rect x="3" y="4.5" width="18" height="15" rx="3"/><path d="M7 10l3 2.5-3 2.5M12.5 15.5h4.5"/>',
    "user": '<circle cx="12" cy="8" r="3.8"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>',
    "heart": '<path d="M20.5 8.8c0 5-8.5 11-8.5 11s-8.5-6-8.5-11a4.6 4.6 0 0 1 8.5-2.3 4.6 4.6 0 0 1 8.5 2.3z"/><path d="M6.5 12h3l1.5-3 2 6 1.5-3h3"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
    "trash": '<path d="M4 7h16M9.5 7V4.5h5V7M6.5 7l1 13h9l1-13"/>',
    "download": '<path d="M12 4v11M7.5 11l4.5 4.5 4.5-4.5M5 20h14"/>',
    "gauge": '<path d="M4.5 17a8.5 8.5 0 1 1 15 0"/><path d="M12 13l4-4"/>',
    "sd": '<path d="M7 3h7.5L19 7.5V21H7z"/><path d="M10 6v3M12.5 6v3M15 8v1"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    "power": '<path d="M12 3v8M7 6.5a7.5 7.5 0 1 0 10 0"/>',
    "server": '<rect x="3.5" y="4" width="17" height="7" rx="2"/><rect x="3.5" y="13" width="17" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>',
    "broadcast": '<circle cx="12" cy="12" r="2"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 7.8a6 6 0 0 1 0 8.4M4.9 4.9a10 10 0 0 0 0 14.2M19.1 4.9a10 10 0 0 1 0 14.2"/>',
    "usb": '<circle cx="12" cy="18.5" r="2"/><path d="M12 16.5V4M12 4l-2.5 2.5M12 4l2.5 2.5M12 11l-4-2v-1.5M12 13l4-2.5"/>',
    "ethernet": '<rect x="6" y="3" width="12" height="9" rx="1.5"/><path d="M9 12v3h6v-3M12 15v5"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3.5 17.5a1.8 1.8 0 0 0 2.5 2.5l5.8-5.8a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.2-.6-.6-2.2z"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "list": '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8L3.5 9.7l5.9-.8z"/>',
    "tm": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.2 2"/><path d="M5.2 6.2L3.2 4.5M5.2 6.2L7.3 4.5"/>',
}


def esc(s):
    return html.escape(str(s), quote=False)


def text_w(s, size, weight=500):
    """Rough text width, good enough to size pills and centre things."""
    k = 0.56 if weight < 650 else 0.6
    return len(s) * size * k


class Canvas:
    def __init__(self, w, h, title, desc, glows=("blue", "purple"), radius=34):
        self.w, self.h = w, h
        self.title, self.desc = title, desc
        self.glows = glows
        self.radius = radius
        self.parts = []
        self.uid = 0

    def nid(self, p="i"):
        self.uid += 1
        return f"{p}{self.uid}"

    def add(self, s):
        self.parts.append(s)

    # ------------------------------------------------------------------ defs
    def _defs(self):
        d = []
        for name, (lo, hi) in PAL.items():
            d.append(f'<linearGradient id="g-{name}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lo}"/><stop offset="1" stop-color="{hi}"/></linearGradient>')
            d.append(f'<radialGradient id="r-{name}" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{hi}" stop-opacity="0.55"/><stop offset="1" stop-color="{hi}" stop-opacity="0"/></radialGradient>')
            d.append(f'<marker id="a-{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1.2L8.6 5 1 8.8z" fill="{lo}" stroke="{lo}" stroke-width="1" stroke-linejoin="round"/></marker>')
        d.append('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0E1B"/><stop offset="1" stop-color="#131A30"/></linearGradient>')
        d.append('<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.11"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.045"/></linearGradient>')
        d.append('<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.08"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.04"/></linearGradient>')
        d.append('<linearGradient id="tilehl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.45"/><stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
        d.append('<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity="0.45"/></filter>')
        d.append('<filter id="tileshadow" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/></filter>')
        d.append('<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>')
        d.append(f'<clipPath id="panel"><rect width="{self.w}" height="{self.h}" rx="{self.radius}"/></clipPath>')
        return "\n    ".join(d)

    def _style(self):
        return f"""
    text {{ font-family: {FONT}; }}
    .t  {{ font-size: 25px; font-weight: 650; fill: {INK}; letter-spacing: -0.012em; }}
    .tl {{ font-size: 21px; font-weight: 650; fill: {INK}; letter-spacing: -0.008em; }}
    .s  {{ font-size: 18px; font-weight: 450; fill: {INK2}; letter-spacing: 0.002em; }}
    .eyebrow {{ font-size: 15px; font-weight: 650; letter-spacing: 0.14em; text-transform: uppercase; }}
    .h1 {{ font-size: 40px; font-weight: 720; fill: {INK}; letter-spacing: -0.028em; }}
    .big {{ font-size: 46px; font-weight: 720; fill: {INK}; letter-spacing: -0.03em; }}
    .m  {{ font-family: {MONO}; font-size: 17px; font-weight: 500; fill: {INK2}; }}
    .flow {{ stroke-dasharray: 2 13; stroke-linecap: round; animation: flow 1.3s linear infinite; }}
    .flowr {{ stroke-dasharray: 2 13; stroke-linecap: round; animation: flowr 1.3s linear infinite; }}
    .pulse {{ animation: pulse 2.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    .float {{ animation: float 6s ease-in-out infinite; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -15; }} }}
    @keyframes flowr {{ to {{ stroke-dashoffset: 15; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 0.55; }} 50% {{ opacity: 1; }} }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .flow,.flowr,.pulse,.float {{ animation: none; }} }}
"""

    # ---------------------------------------------------------------- render
    def render(self):
        glow_parts = []
        pos = [(0.12, 0.0), (0.92, 1.0), (0.55, 0.5)]
        for i, g in enumerate(self.glows):
            gx, gy = pos[i % len(pos)]
            r = max(self.w, self.h) * 0.55
            glow_parts.append(f'<circle cx="{self.w*gx:.0f}" cy="{self.h*gy:.0f}" r="{r:.0f}" fill="url(#r-{g})" opacity="0.5"/>')
        body = "\n".join(self.parts)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img" aria-labelledby="ttl dsc">
  <title id="ttl">{esc(self.title)}</title>
  <desc id="dsc">{esc(self.desc)}</desc>
  <defs>
    {self._defs()}
    <style>{self._style()}</style>
  </defs>
  <g clip-path="url(#panel)">
    <rect width="{self.w}" height="{self.h}" fill="url(#bg)"/>
    {''.join(glow_parts)}
    <g opacity="0.5"><rect width="{self.w}" height="{self.h}" fill="none"/></g>
  </g>
  {body}
  <rect x="0.5" y="0.5" width="{self.w-1}" height="{self.h-1}" rx="{self.radius}" fill="none" stroke="url(#edge)" stroke-width="1.2"/>
</svg>
"""

    # ------------------------------------------------------------ primitives
    def text(self, x, y, s, cls="s", anchor="middle", fill=None, extra=""):
        # CSS classes beat presentation attributes, so colour goes in an inline style, merged with any style in `extra`.
        m = re.search(r'style="([^"]*)"', extra)
        style = m.group(1).rstrip(";") if m else ""
        extra = re.sub(r'style="[^"]*"', "", extra)
        if fill:
            style = (style + ";" if style else "") + f"fill:{fill}"
        st = f' style="{style}"' if style else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{st} {extra}>{esc(s)}</text>')

    def lines(self, x, y, ss, cls="s", lh=24, anchor="middle", fill=None):
        for i, s in enumerate(ss):
            self.text(x, y + i * lh, s, cls, anchor, fill)

    def eyebrow(self, x, y, s, color="teal", anchor="start"):
        self.add(f'<text x="{x}" y="{y}" class="eyebrow" text-anchor="{anchor}" fill="{ACCENT[color]}">{esc(s)}</text>')

    def icon(self, name, cx, cy, size=26, stroke="#fff", sw=1.9):
        s = size / 24
        self.add(f'<g transform="translate({cx - size/2:.1f},{cy - size/2:.1f}) scale({s:.3f})" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')

    def tile(self, name, cx, cy, color="blue", size=56, glyph=None):
        r = size * 0.27
        x, y = cx - size / 2, cy - size / 2
        self.add(f'<g filter="url(#tileshadow)"><rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" rx="{r:.1f}" fill="url(#g-{color})"/></g>')
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" rx="{r:.1f}" fill="url(#tilehl)"/>')
        self.add(f'<rect x="{x+0.5:.1f}" y="{y+0.5:.1f}" width="{size-1}" height="{size-1}" rx="{r:.1f}" fill="none" stroke="#fff" stroke-opacity="0.28"/>')
        self.icon(name, cx, cy, glyph or size * 0.5)

    def glass(self, x, y, w, h, r=22, tint=None, shadow=True):
        sh = ' filter="url(#shadow)"' if shadow else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="url(#glass)"{sh}/>')
        if tint:
            self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{ACCENT[tint]}" opacity="0.10"/>')
        self.add(f'<rect x="{x+0.5:.1f}" y="{y+0.5:.1f}" width="{w-1:.1f}" height="{h-1:.1f}" rx="{r}" fill="none" stroke="url(#edge)" stroke-width="1.2"/>')

    def card(self, cx, cy, w, h, icon, color, title, sub=None, layout="col", tint=True, sub_lines=None, tcls="t", tile=56):
        """A glass card centred at (cx, cy) with a gradient icon tile."""
        x, y = cx - w / 2, cy - h / 2
        self.glass(x, y, w, h, tint=color if tint else None)
        subs = sub_lines or ([sub] if sub else [])
        if layout == "col":
            self.tile(icon, cx, y + 20 + tile / 2, color, tile)
            ty = y + 20 + tile + 32
            self.text(cx, ty, title, tcls)
            for i, s in enumerate(subs):
                self.text(cx, ty + 28 + i * 23, s, "s")
        else:  # row: icon left, text right
            self.tile(icon, x + 20 + 28, cy, color)
            tx = x + 20 + 56 + 18
            total = 1 + len(subs)
            top = cy - (total * 26) / 2 + 20
            self.text(tx, top, title, "tl", anchor="start")
            for i, s in enumerate(subs):
                self.text(tx, top + 26 + i * 22, s, "s", anchor="start")

    def pill(self, cx, cy, s, color="teal", size=15, solid=False, pad=14):
        w = text_w(s, size, 650) + pad * 2
        h = size + 14
        x, y = cx - w / 2, cy - h / 2
        if solid:
            self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="url(#g-{color})"/>')
            self.add(f'<text x="{cx}" y="{cy+size*0.36:.1f}" text-anchor="middle" style="font-size:{size}px;font-weight:650;letter-spacing:0.01em" fill="#fff">{esc(s)}</text>')
        else:
            self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{ACCENT[color]}" fill-opacity="0.16" stroke="{ACCENT[color]}" stroke-opacity="0.55"/>')
            self.add(f'<text x="{cx}" y="{cy+size*0.36:.1f}" text-anchor="middle" style="font-size:{size}px;font-weight:650;letter-spacing:0.01em" fill="{ACCENT[color]}">{esc(s)}</text>')
        return w

    def badge_num(self, cx, cy, n, color="blue", r=16):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#g-{color})"/>')
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r-0.5}" fill="none" stroke="#fff" stroke-opacity="0.3"/>')
        self.add(f'<text x="{cx}" y="{cy+6}" text-anchor="middle" style="font-size:{int(r*1.05)}px;font-weight:700" fill="#fff">{esc(n)}</text>')

    # ----------------------------------------------------------------- links
    def link(self, x1, y1, x2, y2, color="teal", label=None, vertical=False, both=False,
             dashed=False, flow=True, reverse=False, bend=0, lab_color=None, width=2.6, head=True, lab_dy=0, straight=False):
        if vertical:
            my = (y1 + y2) / 2
            d = f"M{x1},{y1} C{x1},{my} {x2},{my} {x2},{y2}" if abs(x2 - x1) > 1 else f"M{x1},{y1} L{x2},{y2}"
        else:
            mx = (x1 + x2) / 2
            d = f"M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" if abs(y2 - y1) > 1 else f"M{x1},{y1} L{x2},{y2}"
        if straight:
            d = f"M{x1},{y1} L{x2},{y2}"
        if bend:
            d = f"M{x1},{y1} Q{(x1+x2)/2},{(y1+y2)/2+bend} {x2},{y2}"
        mk = f' marker-end="url(#a-{color})"' if head else ""
        if both:
            mk += f' marker-start="url(#a-{color})"'
        dash = ' stroke-dasharray="3 9"' if dashed else ""
        self.add(f'<path d="{d}" fill="none" stroke="{ACCENT[color]}" stroke-opacity="0.42" stroke-width="{width}" stroke-linecap="round"{dash}{mk}/>')
        if flow and not dashed:
            cls = "flowr" if reverse else "flow"
            self.add(f'<path d="{d}" fill="none" stroke="{ACCENT[color]}" stroke-width="{width+0.6}" class="{cls}"/>')
        if label:
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 + (bend / 2 if bend else 0) + lab_dy
            self.link_label(lx, ly, label, lab_color or color)

    def link_label(self, cx, cy, s, color="teal", size=15):
        w = text_w(s, size, 600) + 22
        h = size + 14
        self.add(f'<rect x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="#0C1224" fill-opacity="0.92" stroke="{ACCENT[color]}" stroke-opacity="0.5"/>')
        self.add(f'<text x="{cx}" y="{cy+size*0.36:.1f}" text-anchor="middle" style="font-size:{size}px;font-weight:600;letter-spacing:0.005em" fill="{INK}">{esc(s)}</text>')

    def decision(self, cx, cy, w, h, s_lines, color="blue"):
        pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
        self.add(f'<polygon points="{pts}" fill="url(#glass)" filter="url(#shadow)"/>')
        self.add(f'<polygon points="{pts}" fill="{ACCENT[color]}" fill-opacity="0.12"/>')
        self.add(f'<polygon points="{pts}" fill="none" stroke="{ACCENT[color]}" stroke-opacity="0.7" stroke-width="1.4"/>')
        n = len(s_lines)
        for i, s in enumerate(s_lines):
            self.text(cx, cy + 6 - (n - 1) * 11 + i * 22, s, "s", fill=INK)

    def terminal_line(self, x, y, s, color=None, anchor="start"):
        self.add(f'<text x="{x}" y="{y}" class="m" text-anchor="{anchor}"' + (f' fill="{color}"' if color else "") + f'>{esc(s)}</text>')

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.render())
