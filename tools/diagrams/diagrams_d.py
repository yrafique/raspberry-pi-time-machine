"""Diagrams for chapters 7 to 9 (speed, troubleshooting, maintenance)."""
from lib import Canvas, ACCENT, INK, INK2, INK3, text_w

ALL = ["bottleneck", "speed_chart", "backup_time", "speed_decision",
       "troubleshoot_map", "blocked_laptop", "disk_boot", "maintenance", "replace_disk"]


def bar(c, x1, x2, cy, h, color, opacity=0.95):
    c.add(f'<rect x="{x1}" y="{cy-h/2}" width="{x2-x1}" height="{h}" rx="{h/2}" fill="url(#g-{color})" opacity="{opacity}"/>')
    c.add(f'<path d="M{x1+10} {cy} H{x2-10}" stroke="#fff" stroke-opacity="0.8" stroke-width="{min(3, h/3):.1f}" class="flow" fill="none"/>')


def bottleneck():
    c = Canvas(1200, 410, "Where the bottleneck is",
               "Data passes through Wi-Fi at about 15 to 60 MB/s, gigabit Ethernet at about 110 MB/s, and USB 3.0 at about 400 MB/s to a disk that does about 145 MB/s. The slowest link sets the speed.",
               glows=("red", "green"))
    c.eyebrow(56, 58, "Where the time goes", "teal")
    cy = 170
    nodes = [(105, "laptop", "blue", "Mac", "on Wi-Fi"), (435, "router", "gray", "Router", None),
             (765, "pi", "green", "Raspberry Pi", None), (1095, "drive", "orange", "Disk", "145 MB/s")]
    for x, ic, col, t, s in nodes:
        c.card(x, cy, 150, 150, ic, col, t, s, tcls="tl", tile=50)
    links = [(190, 350, 10, "red", "Wi-Fi", "15 to 60 MB/s"),
             (520, 680, 20, "orange", "Gigabit Ethernet", "about 110 MB/s"),
             (850, 1010, 32, "green", "USB 3.0", "about 400 MB/s")]
    for x1, x2, h, col, name, spd in links:
        bar(c, x1, x2, cy, h, col)
        mid = (x1 + x2) / 2
        c.text(mid, cy - 54, name, "tl")
        c.text(mid, cy + 62, spd, "s", fill=ACCENT[col])
    c.pill(270, 270, "the bottleneck on Wi-Fi", "red", size=14)
    c.glass(56, 296, 1088, 86, r=24, tint="blue")
    c.tile("gauge", 112, 339, "blue", 50)
    c.text(156, 331, "The slowest link sets the speed", "t", anchor="start")
    c.text(156, 360, "On Ethernet, the Pi's gigabit port is just below the disk's speed, so the network is still the limit.", "s", anchor="start")
    return c


def speed_chart():
    c = Canvas(1200, 450, "Measured and best-case speeds",
               "Disk write 144 MB/s, disk read 145 MB/s, gigabit Ethernet best case about 110 MB/s, and a real first backup over Wi-Fi about 15 MB/s.",
               glows=("blue", "orange"))
    c.eyebrow(56, 58, "Speed in MB per second, higher is faster", "teal")
    rows = [("Disk write", "measured with dd", 144, "blue", True),
            ("Disk read", "measured with dd", 145, "blue", True),
            ("Gigabit Ethernet", "hardware limit, best case", 110, "orange", False),
            ("Real backup on Wi-Fi", "a 30-second sample", 15, "red", True)]
    x0, scale = 350, 4.9
    for i, (lab, sub, v, col, measured) in enumerate(rows):
        cy = 130 + i * 76
        c.text(320, cy - 2, lab, "tl", anchor="end")
        c.text(320, cy + 22, sub, "s", anchor="end", fill=INK3)
        w = v * scale
        c.add(f'<rect x="{x0}" y="{cy-22}" width="{800}" height="44" rx="22" fill="#fff" opacity="0.05"/>')
        if measured:
            c.add(f'<rect x="{x0}" y="{cy-22}" width="{w}" height="44" rx="22" fill="url(#g-{col})"/>')
            c.add(f'<rect x="{x0}" y="{cy-22}" width="{w}" height="44" rx="22" fill="url(#tilehl)"/>')
        else:
            c.add(f'<rect x="{x0}" y="{cy-22}" width="{w}" height="44" rx="22" fill="{ACCENT[col]}" fill-opacity="0.22" stroke="{ACCENT[col]}" stroke-width="2" stroke-dasharray="6 6"/>')
        c.text(x0 + w + 16, cy + 8, str(v), "big", anchor="start", extra='style="font-size:28px"')
    c.add(f'<rect x="{x0}" y="404" width="26" height="14" rx="7" fill="url(#g-blue)"/>')
    c.text(x0 + 36, 416, "measured", "s", anchor="start")
    c.add(f'<rect x="{x0+150}" y="404" width="26" height="14" rx="7" fill="none" stroke="{ACCENT["orange"]}" stroke-width="2" stroke-dasharray="4 4"/>')
    c.text(x0 + 186, 416, "hardware limit, not measured", "s", anchor="start")
    return c


def backup_time():
    c = Canvas(1200, 480, "How long the first backup takes",
               "At 15 MB/s a first backup takes about 1.9 hours for 100 GB, 9.3 hours for 500 GB and 18.5 hours for 1 TB. At 40 MB/s it takes 0.7, 3.5 and 7 hours.",
               glows=("orange", "green"))
    c.eyebrow(56, 58, "The first backup, in hours", "teal")
    base, k = 410, 13.0
    for h in (0, 5, 10, 15, 20):
        y = base - h * k
        c.add(f'<path d="M110 {y} H1140" stroke="#fff" stroke-opacity="{0.28 if h==0 else 0.09}" stroke-width="1.5"/>')
        c.text(96, y + 6, str(h), "s", anchor="end", fill=INK3)
    data = [("100 GB", 1.9, 0.7), ("500 GB", 9.3, 3.5), ("1 TB", 18.5, 7.0)]
    for i, (lab, slow, fast) in enumerate(data):
        cx = 300 + i * 340
        for dx, v, col, who in ((-62, slow, "orange", "15"), (62, fast, "green", "40")):
            h = v * k
            c.add(f'<rect x="{cx+dx-52}" y="{base-h}" width="104" height="{h}" rx="14" fill="url(#g-{col})"/>')
            c.add(f'<rect x="{cx+dx-52}" y="{base-h}" width="104" height="{h}" rx="14" fill="url(#tilehl)" opacity="0.7"/>')
            c.text(cx + dx, base - h - 12, f"{v:g} h", "tl")
        c.text(cx, base + 34, lab, "t")
    c.pill(730, 70, "15 MB/s: slow Wi-Fi", "orange", size=15)
    c.pill(962, 70, "40 MB/s: good wired", "green", size=15)
    return c


def speed_decision():
    c = Canvas(1200, 500, "How to speed things up",
               "Check whether the Mac is on Wi-Fi, whether the disk is on a 5000M USB 3.0 port, and whether the Ethernet link says 1000. Each failed check has a fix; if all pass, you are at the hardware limit.",
               glows=("green", "blue"))
    c.eyebrow(56, 58, "Slower than you'd like?", "teal")
    qs = [(150, ["Is the Mac", "on Wi-Fi?"], "no"), (450, ["Does lsusb -t", "say 5000M?"], "yes"), (750, ["Does eth0", "say 1000?"], "yes")]
    cy = 170
    for x, lines, _ in qs:
        c.decision(x, cy, 250, 150, lines, "blue")
    c.card(1060, cy, 240, 150, "check", "green", "Hardware limit", None, tcls="tl", sub_lines=["of a Pi 4 on gigabit"])
    c.link(275, cy, 325, cy, "teal"); c.link_label(300, cy - 22, "no", "teal", 13)
    c.link(575, cy, 625, cy, "teal"); c.link_label(600, cy - 22, "yes", "teal", 13)
    c.link(875, cy, 940, cy, "green"); c.link_label(908, cy - 22, "yes", "green", 13)
    fixes = [(150, "ethernet", "orange", "Use Ethernet", ["First backup, wired.", "The biggest gain."], "yes"),
             (450, "usb", "orange", "Use a blue port", ["And a USB 3.0 cable.", "480M means USB 2.0."], "no"),
             (750, "wrench", "orange", "Replace the cable", ["The link says 100,", "not 1000."], "no")]
    for x, ic, col, t, subs, lab in fixes:
        c.link(x, cy + 76, x, 340, "orange", vertical=True, straight=True)
        c.link_label(x + 34, 266, lab, "orange", 13)
        c.card(x, 410, 262, 130, ic, col, t, None, layout="row", tcls="tl", sub_lines=subs)
    return c


def troubleshoot_map():
    c = Canvas(1200, 790, "Find your problem",
               "Five kinds of problem: the Mac can't see the share, can't connect, fails after an update, a backup stopped or is slow, or the disk or boot misbehaves. Each has a first move.",
               glows=("orange", "red", "blue"))
    c.eyebrow(56, 58, "Find your problem", "teal")
    c.card(600, 130, 320, 90, "search", "blue", "What's happening?", None, layout="row", tcls="tl")
    cats = [(152, "search", "orange", "Can't see the share", ["Check ping, smbd,", "avahi, then connect", "by hand"]),
            (376, "lock", "red", "Can't connect", ["Run tcpdump on the", "Pi while the Mac", "tries to connect"]),
            (600, "refresh", "purple", "Fails after update", ["Samba must be", "4.22.6 or newer"]),
            (824, "clock", "blue", "Stopped or slow", ["Mac asleep? Samba", "restarted? Or a", "slow first backup"]),
            (1048, "drive", "teal", "Disk or boot", ["Check lsblk,", "lsusb -t and the", "fstab line"])]
    for x, ic, col, t, lines in cats:
        c.link(600, 176, x, 252, col, vertical=True)
        c.card(x, 320, 208, 148, ic, col, t, None, tcls="tl", tile=46)
        c.link(x, 394, x, 442, col, vertical=True, straight=True, width=2)
        c.glass(x - 104, 446, 208, 112, r=20)
        c.eyebrow(x, 470, "first move", col, anchor="middle")
        for i, s in enumerate(lines):
            c.text(x, 498 + i * 21, s, "s", fill=INK)
    # tcpdump branch under column 2
    c.link(376, 558, 376, 590, "red", vertical=True, straight=True, width=2)
    c.card(262, 676, 214, 150, "check", "green", "Packets arrive", None, tcls="tl", tile=44, sub_lines=["Look on the Pi:", "password, logs"])
    c.card(490, 676, 214, 150, "x", "red", "Nothing at all", None, tcls="tl", tile=44, sub_lines=["A security client on", "the Mac blocks it"])
    c.link(376, 590, 262, 601, "green", vertical=True, straight=False, head=False, flow=False, width=2)
    c.link(376, 590, 490, 601, "red", vertical=True, straight=False, head=False, flow=False, width=2)
    c.glass(640, 608, 508, 136, r=24, tint="green")
    c.tile("check", 704, 676, "green", 56)
    c.text(752, 664, "Not sure? Start here", "t", anchor="start")
    c.text(752, 696, "sudo ./scripts/verify.sh", "m", anchor="start", fill="#5BE584")
    c.text(752, 722, "checks disk, services, Samba and shares", "s", anchor="start")
    return c


def blocked_laptop():
    c = Canvas(1200, 470, "A Mac that can't reach the Pi",
               "A normal Mac sends SMB on port 445 straight to the Pi. A Mac with a security client has its SMB traffic intercepted before it leaves, so the Pi sees no packets at all.",
               glows=("green", "red"))
    c.eyebrow(56, 56, "A normal Mac", "green")
    c.card(190, 140, 260, 96, "laptop", "blue", "Mac", "no security client", layout="row", tcls="tl")
    c.card(1010, 140, 280, 96, "pi", "green", "Raspberry Pi", "packets arrive", layout="row", tcls="tl")
    c.link(322, 140, 868, 140, "green", straight=True)
    c.link_label(595, 112, "SMB, port 445", "green", 14)
    c.add('<path d="M56 224 H1144" stroke="#fff" stroke-opacity="0.1"/>')
    c.eyebrow(56, 272, "A Mac with a security client", "red")
    c.card(190, 356, 260, 96, "laptop", "blue", "Mac", "managed laptop", layout="row", tcls="tl")
    c.card(600, 356, 290, 110, "shield", "red", "Security client", "intercepts SMB", layout="row", tcls="tl")
    c.card(1010, 356, 280, 96, "pi", "gray", "Raspberry Pi", "sees 0 packets", layout="row", tcls="tl", tint=False)
    c.link(322, 356, 452, 356, "red", straight=True)
    c.link(752, 356, 868, 356, "red", dashed=True, straight=True, head=False)
    c.add(f'<circle cx="810" cy="356" r="17" fill="#0C1224" stroke="{ACCENT["red"]}" stroke-width="1.6"/>')
    c.icon("x", 810, 356, 18, stroke=ACCENT["red"], sw=2.6)
    c.pill(810, 428, "never leaves the Mac", "red", size=13)
    return c


def disk_boot():
    c = Canvas(1200, 430, "Disk and boot problems",
               "Four symptoms and their fixes: a disk missing from lsblk, a disk that shows 480M, an empty mount, and emergency mode on boot.",
               glows=("orange", "green"))
    c.eyebrow(56, 56, "Disk and boot problems", "teal")
    cols = [(180, "usb", "Disk missing", "not in lsblk", ["Try another USB port", "and cable. A 3.5-inch", "disk needs its own power."]),
            (460, "gauge", "Shows 480M", "in lsusb -t", ["It's on USB 2.0.", "Use a blue port and a", "USB 3.0 cable."]),
            (740, "folder", "Mount is empty", "/srv/timemachine", ["The disk didn't mount.", "Run: sudo mount ...", "Samba stays stopped."]),
            (1020, "warn", "Emergency mode", "on boot", ["A bad /etc/fstab line.", "Make sure the disk", "line has nofail."])]
    for x, ic, t, s, lines in cols:
        c.card(x, 150, 250, 150, ic, "orange", t, s, tcls="tl", tile=46)
        c.link(x, 226, x, 274, "green", vertical=True, straight=True)
        c.glass(x - 125, 280, 250, 118, r=22, tint="green")
        c.eyebrow(x, 306, "the fix", "green", anchor="middle")
        for i, ln in enumerate(lines):
            c.text(x, 334 + i * 22, ln, "s", fill=INK)
    return c


def maintenance():
    c = Canvas(1200, 400, "A light maintenance routine",
               "Whenever you like, run verify.sh. Monthly, install updates and check disk health. Once, test a restore and a reboot. When things change, add or remove a Mac or replace a failing disk.",
               glows=("teal", "purple"))
    c.eyebrow(56, 56, "A light routine", "teal")
    cols = [(195, "eye", "blue", "Whenever", ["Run verify.sh", "Check free space", "See who is connected"]),
            (465, "calendar", "teal", "Monthly", ["Install updates", "Run verify.sh again", "Check disk health"]),
            (735, "check", "green", "Once", ["Restore one file", "Do a reboot test", ""]),
            (1005, "refresh", "orange", "When things change", ["add-mac.sh", "remove-mac.sh", "Replace a failing disk"])]
    for x, ic, col, t, lines in cols:
        c.glass(x - 125, 92, 250, 262, r=26, tint=col)
        c.tile(ic, x, 92 + 54, col, 54)
        c.text(x, 92 + 128, t, "tl")
        for i, ln in enumerate(lines):
            if ln:
                c.text(x, 92 + 168 + i * 28, ln, "s", fill=INK)
    return c


def replace_disk():
    c = Canvas(1200, 360, "Replacing the disk",
               "Connect the new disk, set DISK in config.env, run the prepare, shares and harden scripts, then re-add the backup disk on each Mac. Keep the old disk for a while.",
               glows=("orange", "red"))
    c.eyebrow(56, 56, "Replacing the disk", "teal")
    steps = [("drive", "orange", "Connect the", "new disk"), ("doc", "blue", "Set DISK in", "config.env"),
             ("trash", "red", "02-prepare-", "drive.sh"), ("server", "teal", "03-configure-", "shares.sh"),
             ("shield", "purple", "04-harden.sh", ""), ("laptop", "green", "Re-add the disk", "on each Mac")]
    cw, gap = 162, 30
    total = len(steps) * cw + (len(steps) - 1) * gap
    x0 = (1200 - total) / 2 + cw / 2
    for i, (ic, col, a, b) in enumerate(steps):
        cx = x0 + i * (cw + gap)
        c.glass(cx - cw / 2, 92, cw, 168, tint=col)
        c.badge_num(cx - cw / 2 + 22, 92 + 22, i + 1, col, 12)
        c.tile(ic, cx, 92 + 62, col, 52)
        c.text(cx, 92 + 128, a, "tl", extra='style="font-size:19px"')
        if b:
            c.text(cx, 92 + 152, b, "tl", extra='style="font-size:19px"')
        if i < len(steps) - 1:
            c.link(cx + cw / 2 + 3, 92 + 62, cx + cw / 2 + gap - 3, 92 + 62, "teal", width=2)
    c.pill(600, 306, "Keep the old disk for a while. It still holds your old backups.", "orange", size=15)
    return c
