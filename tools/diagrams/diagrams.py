"""Every diagram in the guide, one function each. Run build.py to write the SVGs."""
from lib import Canvas, ACCENT, PAL, INK, INK2, INK3, text_w


# ---------------------------------------------------------------------------
def banner():
    c = Canvas(1280, 440, "Time Machine on a Raspberry Pi",
               "A Raspberry Pi connected to a USB hard drive, backing up two MacBooks over the network.",
               glows=("teal", "indigo", "green"), radius=36)
    # soft grid of light
    c.add('<g opacity="0.07" stroke="#fff" stroke-width="1">' + "".join(
        f'<path d="M{x} 0V440"/>' for x in range(0, 1281, 64)) + "".join(
        f'<path d="M0 {y}H1280"/>' for y in range(0, 441, 64)) + '</g>')

    c.eyebrow(84, 132, "Backup server guide", "teal")
    c.add(f'<text x="80" y="214" style="font-size:78px;font-weight:760;letter-spacing:-0.035em" fill="{INK}">Time Machine</text>')
    c.add('<text x="80" y="296" style="font-size:78px;font-weight:760;letter-spacing:-0.035em" fill="url(#ttlgrad)">on a Raspberry Pi</text>')
    c.add('<defs><linearGradient id="ttlgrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7CE0FF"/><stop offset="0.55" stop-color="#8B8CFF"/><stop offset="1" stop-color="#D58BFF"/></linearGradient></defs>')
    c.add(f'<text x="84" y="346" style="font-size:26px;font-weight:450;letter-spacing:-0.005em" fill="{INK2}">Give a spare USB drive a second life as a backup server.</text>')
    x = 84
    for label, col in (("Samba", "teal"), ("Avahi", "purple"), ("ext4", "orange"), ("macOS 26", "green")):
        w = text_w(label, 17, 650) + 36
        c.pill(x + w / 2, 392, label, col, size=17, pad=18)
        x += w + 12

    # --- illustration -------------------------------------------------------
    def mac(cx, cy, s=1.0, glow="blue"):
        w, h = 190 * s, 120 * s
        x, y = cx - w / 2, cy - h / 2
        c.add(f'<g filter="url(#shadow)"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{12*s:.1f}" fill="#C9CEDA"/></g>')
        c.add(f'<rect x="{x+7*s:.1f}" y="{y+7*s:.1f}" width="{w-14*s:.1f}" height="{h-14*s:.1f}" rx="{7*s:.1f}" fill="#070B16"/>')
        c.add(f'<circle cx="{cx}" cy="{cy}" r="{46*s:.1f}" fill="url(#r-{glow})" opacity="0.9"/>')
        r = 22 * s
        c.add(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="url(#g-teal)" stroke-width="{4.5*s:.1f}"/>')
        c.add(f'<path d="M{cx} {cy-r*0.55:.1f} V{cy:.1f} L{cx+r*0.45:.1f} {cy+r*0.3:.1f}" fill="none" stroke="#fff" stroke-width="{4*s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        c.add(f'<path d="M{cx-r-7*s:.1f} {cy-4*s:.1f} l{7*s:.1f} {9*s:.1f} l{7*s:.1f} -{9*s:.1f}" fill="none" stroke="#fff" stroke-width="{3.2*s:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>')
        c.add(f'<rect x="{x-14*s:.1f}" y="{y+h-1:.1f}" width="{w+28*s:.1f}" height="{10*s:.1f}" rx="{5*s:.1f}" fill="#AEB4C2"/>')
        c.add(f'<rect x="{cx-22*s:.1f}" y="{y+h-1:.1f}" width="{44*s:.1f}" height="{4*s:.1f}" rx="{2*s:.1f}" fill="#8C93A3"/>')

    mac(900, 120, 1.0, "blue")
    mac(1130, 120, 1.0, "purple")
    # Pi board
    px, py, pw, ph = 880, 272, 250, 130
    c.add(f'<g filter="url(#shadow)"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="url(#g-green)"/></g>')
    c.add(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="url(#tilehl)" opacity="0.7"/>')
    c.add(f'<rect x="{px+0.5}" y="{py+0.5}" width="{pw-1}" height="{ph-1}" rx="16" fill="none" stroke="#fff" stroke-opacity="0.35"/>')
    c.add(f'<rect x="{px+24}" y="{py+28}" width="66" height="66" rx="8" fill="#0A1020"/>')
    c.add(f'<text x="{px+57}" y="{py+68}" text-anchor="middle" style="font-size:13px;font-weight:700;letter-spacing:0.08em" fill="#7CE0FF">BCM</text>')
    for i in range(3):
        c.add(f'<rect x="{px+108}" y="{py+22+i*30}" width="44" height="22" rx="4" fill="#E5E9F0" opacity="0.92"/>')
    c.add(f'<rect x="{px+168}" y="{py+22}" width="62" height="34" rx="5" fill="#9AA3B5"/>')
    c.add(f'<rect x="{px+168}" y="{py+66}" width="62" height="34" rx="5" fill="#2F7BFF"/>')
    c.add(f'<circle class="pulse" cx="{px+26}" cy="{py+ph-18}" r="4.5" fill="#FFD60A"/>')
    c.add(f'<text x="{px+pw-20}" y="{py+ph-14}" text-anchor="end" style="font-size:14px;font-weight:700;letter-spacing:0.02em" fill="#06310F">Raspberry Pi 4</text>')
    # drive
    dx, dy = 1196, 360
    c.add(f'<g filter="url(#shadow)"><rect x="{dx-58}" y="{dy-50}" width="116" height="100" rx="16" fill="#C2C8D4"/></g>')
    c.add(f'<rect x="{dx-58}" y="{dy-50}" width="116" height="100" rx="16" fill="url(#tilehl)" opacity="0.8"/>')
    c.add(f'<circle cx="{dx}" cy="{dy-6}" r="30" fill="#1B2233"/>')
    c.add(f'<circle cx="{dx}" cy="{dy-6}" r="9" fill="#8E96AA"/>')
    c.add(f'<path d="M{dx} {dy-6} L{dx+24} {dy-26}" stroke="#E6E9F0" stroke-width="4" stroke-linecap="round"/>')
    c.add(f'<text x="{dx}" y="{dy+40}" text-anchor="middle" style="font-size:14px;font-weight:800" fill="#2B3246">2 TB</text>')
    # links
    c.link(900, 190, 960, 270, "teal", vertical=True)
    c.link(1130, 190, 1050, 270, "purple", vertical=True)
    c.link(1130, 340, 1138, 340, "blue", flow=False, head=False)
    c.add('<path d="M1130 337 H1138" stroke="#2F7BFF" stroke-width="6" stroke-linecap="round"/>')
    return c


# ---------------------------------------------------------------------------
def architecture():
    c = Canvas(1200, 470, "How the pieces fit together",
               "Two Macs reach a router over Wi-Fi or Ethernet. The router connects by gigabit Ethernet to a Raspberry Pi running Samba and Avahi, and the Pi connects by USB 3.0 to a 2 TB disk holding one folder per Mac.",
               glows=("blue", "green"))
    c.eyebrow(56, 62, "The big picture", "teal")
    c.card(125, 168, 190, 150, "laptop", "blue", "MacBook", "personal")
    c.card(125, 336, 190, 150, "laptop", "purple", "MacBook", "work")
    c.card(410, 252, 150, 150, "router", "gray", "Router", "your network")
    c.glass(580, 96, 290, 336, r=26, tint="green")
    c.tile("pi", 630, 142, "green", 52)
    c.text(668, 140, "Raspberry Pi 4", "tl", anchor="start")
    c.text(668, 164, "Debian 13", "s", anchor="start")
    c.card(725, 262, 250, 86, "server", "teal", "Samba", "serves the share", layout="row")
    c.card(725, 366, 250, 86, "broadcast", "purple", "Avahi", "announces it", layout="row")
    c.glass(950, 96, 214, 336, r=26, tint="orange")
    c.tile("drive", 997, 142, "orange", 52)
    c.text(1032, 140, "USB disk", "tl", anchor="start")
    c.text(1032, 164, "2 TB \u00b7 ext4", "s", anchor="start")
    c.card(1057, 262, 178, 82, "folder", "blue", "personal/", "Mac 1", layout="row", tint=False, tcls="tl")
    c.card(1057, 366, 178, 82, "folder", "purple", "work/", "Mac 2", layout="row", tint=False, tcls="tl")
    c.link(220, 168, 335, 238, "blue", both=True)
    c.link(220, 336, 335, 268, "purple", both=True)
    c.link_label(293, 253, "Wi-Fi or Ethernet", "teal", 14)
    c.link(485, 252, 580, 252, "green", both=True)
    c.link_label(532, 216, "Gigabit", "green", 14)
    c.link(870, 262, 950, 262, "orange", both=True)
    c.link_label(910, 226, "USB 3.0", "orange", 14)
    return c


# ---------------------------------------------------------------------------
def route():
    c = Canvas(1200, 330, "The route",
               "Five steps: prepare the Pi, prepare the drive, install the server, connect your Macs, then make it solid.",
               glows=("blue", "green"))
    c.eyebrow(56, 56, "The route", "teal")
    steps = [
        ("pi", "green", "Prepare the Pi", "Flash, SSH,\nfixed address", "Chapter 2", None),
        ("drive", "red", "Prepare the drive", "Erase, format,\nmount at boot", "Chapter 3", "erases it"),
        ("server", "teal", "Install the server", "Samba, Bonjour,\nusers and shares", "Chapter 4", None),
        ("laptop", "blue", "Connect your Macs", "Add the disk in\nTime Machine", "Chapter 5", None),
        ("shield", "purple", "Make it solid", "Boot order, health,\nreboot test", "Chapter 6", None),
    ]
    n = len(steps)
    cw, gap = 196, 36
    total = n * cw + (n - 1) * gap
    x0 = (1200 - total) / 2 + cw / 2
    cy = 186
    for i, (ic, col, t, s, ch, warn) in enumerate(steps):
        cx = x0 + i * (cw + gap)
        c.glass(cx - cw / 2, cy - 100, cw, 224, tint=col)
        c.tile(ic, cx, cy - 46, col, 54)
        c.badge_num(cx - cw / 2 + 24, cy - 100 + 24, i + 1, col, 13)
        c.text(cx, cy + 22, t, "tl")
        for j, line in enumerate(s.split("\n")):
            c.text(cx, cy + 50 + j * 22, line, "s")
        c.pill(cx, cy + 100, ch + (" \u00b7 " + warn if warn else ""), "red" if warn else "teal", size=13)
        if i < n - 1:
            c.link(cx + cw / 2 + 6, cy, cx + cw / 2 + gap - 6, cy, "teal")
    return c
