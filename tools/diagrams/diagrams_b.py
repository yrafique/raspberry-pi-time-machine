"""Diagrams for chapters 1 to 3 and the README."""
from lib import Canvas, ACCENT, INK, INK2, INK3, text_w

ALL = ["features", "backup_flow", "isolation", "retention", "setup_steps", "ports", "disk_before_after", "wipe_guard"]


def features():
    c = Canvas(1200, 292, "What you end up with",
               "Five benefits: automatic hourly backups, one share per Mac, the whole disk shared, it survives power cuts, and about an hour of work.",
               glows=("indigo", "teal"))
    items = [
        ("refresh", "blue", "Automatic", "Hourly backups over\nWi-Fi or Ethernet"),
        ("lock", "purple", "One share per Mac", "Each Mac has its own\nprivate login"),
        ("drive", "orange", "The whole disk", "All the space, no\nquotas to manage"),
        ("shield", "green", "Survives power cuts", "Restarts by itself and\nwatches disk health"),
        ("clock", "teal", "About an hour", "Most of it is waiting\nfor the first backup"),
    ]
    cw, gap = 204, 22
    total = len(items) * cw + (len(items) - 1) * gap
    x0 = (1200 - total) / 2 + cw / 2
    for i, (ic, col, t, s) in enumerate(items):
        cx = x0 + i * (cw + gap)
        c.glass(cx - cw / 2, 36, cw, 220, tint=col)
        c.tile(ic, cx, 36 + 52, col, 56)
        c.text(cx, 36 + 128, t, "tl")
        for j, line in enumerate(s.split("\n")):
            c.text(cx, 36 + 158 + j * 22, line, "s")
    return c


def backup_flow():
    c = Canvas(1200, 620, "What happens during a backup",
               "The Pi's Avahi announces the share, the Mac connects to Samba with its login, creates a backup file, and then sends only what changed every hour; Samba writes it to the disk.",
               glows=("blue", "purple"))
    c.eyebrow(56, 62, "What happens during a backup", "teal")
    lanes = [(170, "laptop", "blue", "Mac", "Time Machine"),
             (450, "broadcast", "purple", "Avahi", "on the Pi"),
             (730, "server", "teal", "Samba", "on the Pi"),
             (1030, "drive", "orange", "Disk", "ext4")]
    for x, ic, col, t, s in lanes:
        c.card(x, 138, 220, 84, ic, col, t, s, layout="row", tcls="tl")
        c.add(f'<path d="M{x} 182 V500" stroke="{ACCENT[col]}" stroke-opacity="0.35" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>')
    mac, avahi, samba, disk = 170, 450, 730, 1030
    y = 240
    steps = [
        (avahi, mac, "teal", "Announces \u201ca backup disk is here\u201d"),
        (mac, samba, "blue", "Connects with SMB 3 as \u201cpersonal\u201d"),
        (samba, mac, "green", "Checks the password, logs in"),
        (mac, samba, "blue", "Creates the backup file"),
        (samba, disk, "orange", "Writes MyMac.sparsebundle"),
    ]
    for i, (a, bb, col, lab) in enumerate(steps):
        yy = y + i * 56
        sgn = 1 if bb > a else -1
        c.link(a + sgn * 34, yy, bb - sgn * 6, yy, col, straight=True)
        c.badge_num(a, yy, i + 1, col, 14)
        c.text((a + bb) / 2 + sgn * 14, yy - 13, lab, "s", fill=INK)
    # loop band
    c.glass(86, 508, 1030, 76, r=22, tint="blue")
    c.tile("refresh", 140, 546, "blue", 44)
    c.text(186, 540, "Then, every hour while the Mac is awake", "tl", anchor="start")
    c.text(186, 566, "The Mac sends only what changed, and Samba writes it to the disk.", "s", anchor="start")
    return c


def isolation():
    c = Canvas(1200, 430, "One login per share",
               "Mac A's login opens only the TimeMachine-Personal share and its folder. Mac B's login opens only TimeMachine-Work. Each is refused on the other's share.",
               glows=("blue", "purple"))
    c.eyebrow(56, 60, "One login, one share, one private folder", "teal")
    rows = [(150, "blue", "personal", "TimeMachine-Personal", "/srv/timemachine/personal"),
            (330, "purple", "work", "TimeMachine-Work", "/srv/timemachine/work")]
    for y, col, user, share, path in rows:
        c.card(140, y, 220, 96, "laptop", col, "Mac", "login: " + user, layout="row", tcls="tl")
        c.card(610, y, 320, 96, "server", col, share, "valid users = " + user, layout="row", tcls="tl")
        c.card(1040, y, 270, 96, "folder", col, user + "/", "private, mode 700", layout="row", tcls="tl")
        c.link(254, y, 446, y, "green", straight=True)
        c.link_label(350, y - 26, "allowed", "green", 14)
        c.link(776, y, 899, y, "green", straight=True)
    # refused crossings
    c.link(262, 190, 438, 290, "red", dashed=True, straight=True, head=False)
    c.link(262, 290, 438, 190, "red", dashed=True, straight=True, head=False)
    c.link_label(350, 240, "refused", "red", 14)
    return c


def retention():
    c = Canvas(1200, 388, "What Time Machine keeps",
               "The first backup copies everything. After that, it keeps hourly backups for 24 hours, daily backups for a month, and weekly backups until the disk is full.",
               glows=("purple", "blue"))
    c.eyebrow(56, 60, "What Time Machine keeps", "teal")
    cols = [
        ("download", "purple", "First backup", "Copies everything", "hours to a day", 0),
        ("clock", "blue", "Last 24 hours", "Hourly backups", "24 snapshots", 24),
        ("calendar", "teal", "Last month", "Daily backups", "about 30 snapshots", 14),
        ("star", "orange", "Older", "Weekly backups", "until the disk is full", 6),
    ]
    cw, gap = 250, 30
    total = len(cols) * cw + (len(cols) - 1) * gap
    x0 = (1200 - total) / 2 + cw / 2
    for i, (ic, col, t, s, note, ticks) in enumerate(cols):
        cx = x0 + i * (cw + gap)
        c.glass(cx - cw / 2, 96, cw, 252, tint=col)
        c.tile(ic, cx, 96 + 50, col, 56)
        c.text(cx, 96 + 122, t, "tl")
        c.text(cx, 96 + 150, s, "s")
        # density ticks
        if ticks:
            span = cw - 70
            for k in range(ticks):
                tx = cx - span / 2 + (span * k / (ticks - 1))
                c.add(f'<rect x="{tx-1.5:.1f}" y="{96+172}" width="3" height="22" rx="1.5" fill="{ACCENT[col]}" opacity="0.9"/>')
        else:
            c.add(f'<rect x="{cx-(cw-70)/2}" y="{96+172}" width="{cw-70}" height="22" rx="8" fill="{ACCENT[col]}" opacity="0.85"/>')
        c.text(cx, 96 + 226, note, "s", fill=INK2)
        if i < len(cols) - 1:
            c.link(cx + cw / 2 + 4, 96 + 112, cx + cw / 2 + gap - 4, 96 + 112, "teal")
    return c


def setup_steps():
    c = Canvas(1200, 262, "Preparing the Pi in seven steps",
               "Flash the SD card, plug in power and Ethernet, SSH in from the Mac, reserve a fixed address, update everything, connect the USB drive, and clone this repository.",
               glows=("green", "blue"))
    items = [("sd", "green", "Flash the\nSD card"), ("plug", "orange", "Power and\nEthernet"), ("terminal", "blue", "SSH in from\nthe Mac"),
             ("globe", "teal", "Reserve a\nfixed address"), ("download", "purple", "Update\neverything"), ("drive", "pink", "Connect the\nUSB drive"),
             ("doc", "indigo", "Clone this\nrepository")]
    cw, gap = 138, 26
    total = len(items) * cw + (len(items) - 1) * gap
    x0 = (1200 - total) / 2 + cw / 2
    for i, (ic, col, t) in enumerate(items):
        cx = x0 + i * (cw + gap)
        c.glass(cx - cw / 2, 36, cw, 190, tint=col)
        c.badge_num(cx - cw / 2 + 22, 36 + 22, i + 1, col, 12)
        c.tile(ic, cx, 36 + 66, col, 54)
        for j, line in enumerate(t.split("\n")):
            c.text(cx, 36 + 134 + j * 24, line, "tl")
        if i < len(items) - 1:
            c.link(cx + cw / 2 + 3, 36 + 66, cx + cw / 2 + gap - 3, 36 + 66, "teal", width=2)
    return c


def ports():
    c = Canvas(1200, 450, "Which port to use on a Raspberry Pi 4",
               "Plug the USB drive into a blue USB 3.0 port. A black USB 2.0 port is about ten times slower. Ethernet goes to the router and USB-C to the power supply.",
               glows=("green", "blue"))
    c.eyebrow(56, 60, "Which port to use", "teal")
    bx, by, bw, bh = 150, 92, 420, 290
    c.add(f'<g filter="url(#shadow)"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="url(#g-green)"/></g>')
    c.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="url(#tilehl)" opacity="0.6"/>')
    c.add(f'<rect x="{bx+0.5}" y="{by+0.5}" width="{bw-1}" height="{bh-1}" rx="26" fill="none" stroke="#fff" stroke-opacity="0.4"/>')
    # GPIO header
    for r in range(2):
        for k in range(20):
            c.add(f'<circle cx="{bx+70+k*13}" cy="{by+22+r*13}" r="3" fill="#0A1020" opacity="0.8"/>')
    c.add(f'<rect x="{bx+40}" y="{by+90}" width="96" height="96" rx="10" fill="#0A1020"/>')
    c.text(bx + 88, by + 146, "BCM2711", "s", fill="#7CE0FF", extra='style="font-size:14px;font-weight:700;letter-spacing:0.06em"')
    c.add(f'<rect x="{bx+160}" y="{by+110}" width="70" height="56" rx="8" fill="#0A1020" opacity="0.85"/>')
    c.text(bx + 195, by + 144, "RAM", "s", fill="#7CE0FF", extra='style="font-size:13px;font-weight:700"')
    c.add(f'<circle class="pulse" cx="{bx+40}" cy="{by+bh-28}" r="5" fill="#FFD60A"/>')
    # ports on right edge
    px = bx + bw
    c.add(f'<rect x="{px-6}" y="{by+34}" width="64" height="66" rx="6" fill="#DADFE8"/>')
    c.text(px + 26, by + 74, "ETH", "s", fill="#2B3246", extra='style="font-size:14px;font-weight:800"')
    for k, (col, lab) in enumerate((("#2F7BFF", "3.0"), ("#2F7BFF", "3.0"), ("#1B2233", "2.0"), ("#1B2233", "2.0"))):
        yy = by + 112 + k * 44
        c.add(f'<rect x="{px-6}" y="{yy}" width="64" height="36" rx="5" fill="{col}"/>')
        c.text(px + 26, yy + 24, lab, "s", fill="#fff", extra='style="font-size:14px;font-weight:800"')
    c.add(f'<rect x="{bx+60}" y="{by+bh-4}" width="44" height="22" rx="6" fill="#DADFE8"/>')
    c.text(bx + 82, by + bh + 36, "USB-C", "s", fill=INK2, extra='style="font-size:15px;font-weight:700"')
    # devices
    c.card(940, 126, 330, 76, "router", "gray", "Router", "Ethernet cable · 1 Gbps", layout="row", tcls="tl")
    c.card(940, 248, 330, 92, "drive", "orange", "USB drive", "blue port · 5 Gbps", layout="row", tcls="tl")
    c.card(940, 388, 330, 76, "plug", "blue", "Power supply", "5 V, 3 A", layout="row", tcls="tl")
    c.link(px + 58, by + 67, 775, 126, "gray", straight=False)
    c.link(px + 58, by + 130, 775, 236, "green", straight=False)
    c.link_label(690, 196, "use this one", "green", 14)
    c.link(px + 58, by + 218, 775, 262, "red", dashed=True, straight=False, head=False)
    c.link_label(690, 288, "10× slower", "red", 14)
    c.link(bx + 104, by + bh + 14, 775, 388, "blue", straight=True, head=False)
    return c


def disk_before_after():
    c = Canvas(1200, 520, "Before and after erasing the disk",
               "An old NAS disk with eight partitions, including RAID members and swap, becomes a single ext4 partition labelled TimeMachine that fills the whole disk.",
               glows=("red", "green"))
    c.eyebrow(56, 56, "Before", "red")
    segs = [("sda1", "RAID", 100, "gray"), ("sda2", "RAID", 100, "gray"), ("sda3", "swap", 80, "gray"),
            ("sda4", "ext4, old data", 520, "red"), ("sda5–8", "leftovers", 240, "gray")]
    x = 80
    for name, kind, w, col in segs:
        c.add(f'<rect x="{x}" y="92" width="{w-6}" height="70" rx="14" fill="url(#g-{col})" opacity="{0.95 if col=="red" else 0.5}"/>')
        c.add(f'<rect x="{x}" y="92" width="{w-6}" height="70" rx="14" fill="url(#tilehl)"/>')
        c.text(x + (w - 6) / 2, 125, name, "tl", fill="#fff")
        c.text(x + (w - 6) / 2, 150, kind, "s", fill="#fff")
        x += w
    c.text(80, 192, "An old NAS disk: eight partitions, 1.7 TB of obsolete data", "s", anchor="start")
    # middle
    c.link(600, 204, 600, 224, "teal", vertical=True, straight=True, flow=False)
    c.link(600, 284, 600, 326, "teal", vertical=True, straight=True)
    c.glass(380, 226, 440, 56, r=28, tint="orange")
    c.icon("trash", 424, 254, 26)
    c.text(450, 261, "wipefs  ·  parted  ·  mkfs.ext4", "m", anchor="start", fill=INK)
    c.eyebrow(56, 340, "After", "green")
    c.add('<rect x="80" y="372" width="1034" height="78" rx="18" fill="url(#g-green)"/>')
    c.add('<rect x="80" y="372" width="1034" height="78" rx="18" fill="url(#tilehl)"/>')
    c.text(110, 408, "sda1  ·  ext4  ·  label “TimeMachine”", "t", anchor="start", fill="#fff")
    c.text(110, 435, "1.8 TiB, the whole disk, mounted at /srv/timemachine", "s", anchor="start", fill="#fff")
    c.icon("check", 1076, 411, 34)
    c.text(80, 486, "One partition, one purpose", "s", anchor="start")
    return c


def wipe_guard():
    c = Canvas(1200, 470, "How the erase script protects you",
               "The script checks that the target is a real disk, refuses the disk the Pi boots from, and makes you type the device path before it erases anything.",
               glows=("red", "blue"))
    c.eyebrow(56, 58, "The safety net", "teal")
    xs = [130, 365, 600, 835, 1070]
    items = [
        ("terminal", "blue", "Run the script", "02-prepare-drive.sh"),
        ("search", "teal", "Real disk?", "DISK is a block device"),
        ("shield", "orange", "Not the boot disk?", "refuses the SD card"),
        ("key", "purple", "You confirm", "type the device path"),
        ("trash", "red", "Erase and format", "then mount at boot"),
    ]
    for x, (ic, col, t, s) in zip(xs, items):
        c.card(x, 170, 196, 156, ic, col, t, s, tcls="tl", tile=52)
    for i in range(4):
        c.link(xs[i] + 98 + 4, 170, xs[i + 1] - 98 - 4, 170, "green")
        c.link_label((xs[i] + xs[i + 1]) / 2, 138, "yes" if i else "go", "green", 13)
    for x in xs[1:4]:
        c.link(x, 250, x, 336, "red", vertical=True, dashed=True, straight=True)
        c.card(x, 392, 222, 84, "x", "red", "Stop", "nothing erased", layout="row", tcls="tl")
    c.text(xs[4], 392, "Done", "t", fill="#5BE584")
    c.icon("check", xs[4], 352, 40, stroke="#5BE584", sw=2.4)
    c.text(xs[0], 386, "Each “no” stops the script", "s", extra="")
    c.text(xs[0], 410, "before anything is erased.", "s")
    return c
