"""Diagrams for chapters 4 to 6."""
from lib import Canvas, ACCENT, INK, INK2, INK3, text_w

ALL = ["script_flow", "journey", "share_missing", "restore", "boot_order"]


def script_flow():
    c = Canvas(1200, 500, "What the share script builds",
               "config.env feeds 03-configure-shares.sh, which creates Linux users, folders, the Samba share configuration and the Bonjour service file, then restarts the services and sets passwords, leaving shares the Macs can find and use.",
               glows=("orange", "blue"))
    c.eyebrow(56, 58, "What the script builds", "teal")
    c.card(150, 250, 220, 130, "doc", "orange", "config.env", None, tcls="tl", sub_lines=["USERS=“personal work”"])
    c.card(450, 250, 250, 150, "terminal", "blue", "Share script", None, tcls="tl", sub_lines=["03-configure-shares.sh"])
    outs = [("user", "teal", "Linux users", "no login shell"),
            ("folder", "blue", "Folders", "one per Mac, mode 700"),
            ("server", "green", "smb.conf", "one share per user"),
            ("broadcast", "purple", "Avahi service", "Bonjour announcement")]
    ys = [106, 206, 306, 406]
    for y, (ic, col, t, s) in zip(ys, outs):
        c.card(770, y, 290, 84, ic, col, t, s, layout="row", tcls="tl")
        c.link(578, 250, 625, y, "teal")
        c.link(915, y, 985, 250, "green", flow=True)
    c.card(1085, 250, 170, 170, "check", "green", "Ready", None, tcls="tl", sub_lines=["Macs can find", "and use it"])
    c.link(264, 250, 322, 250, "orange")
    c.pill(600, 478, "Then it restarts smbd and avahi, and asks for each password", "gray", size=14)
    return c


def journey():
    c = Canvas(1200, 400, "Connecting a Mac",
               "Three phases: set up in a few minutes, the first backup which takes hours, and then hourly backups every day.",
               glows=("blue", "green"))
    c.eyebrow(56, 56, "Connecting a Mac", "teal")
    phases = [
        (29, 430, "blue", "1", "Set up", "a few minutes", ["Open Time Machine settings", "Pick the share", "Sign in with that share's login", "Choose encryption"]),
        (495, 320, "orange", "2", "First backup", "hours", ["The Mac prepares the backup", "Copies everything to the Pi"]),
        (851, 320, "green", "3", "Every day", "minutes", ["Hourly incremental backups", "Restore a file when needed"]),
    ]
    for x, w, col, n, title, dur, rows in phases:
        c.glass(x, 90, w, 270, r=26, tint=col)
        c.badge_num(x + 36, 130, n, col, 16)
        c.text(x + 64, 137, title, "t", anchor="start")
        pw = text_w(dur, 14, 650) + 28
        c.pill(x + w - 20 - pw / 2, 130, dur, col, size=14)
        for i, r in enumerate(rows):
            yy = 192 + i * 40
            c.add(f'<circle cx="{x+36}" cy="{yy}" r="5" fill="{ACCENT[col]}"/>')
            if i < len(rows) - 1:
                c.add(f'<path d="M{x+36} {yy+9} V{yy+31}" stroke="{ACCENT[col]}" stroke-opacity="0.45" stroke-width="2" stroke-linecap="round"/>')
            c.text(x + 58, yy + 6, r, "s", anchor="start", fill=INK)
    c.link(463, 225, 491, 225, "teal", width=2)
    c.link(819, 225, 847, 225, "teal", width=2)
    return c


def share_missing():
    c = Canvas(1200, 330, "The share is missing from the list",
               "Connect by hand with Finder's Connect to Server. If it connects, only Bonjour is the problem, so restart Avahi. If not, go to troubleshooting.",
               glows=("orange", "green"))
    c.eyebrow(56, 56, "The share isn't listed", "teal")
    c.card(140, 190, 200, 150, "search", "orange", "Share missing", "in Time Machine", tcls="tl")
    c.card(440, 190, 250, 150, "globe", "blue", "Connect by hand", "Finder → Go → Connect to Server", tcls="tl")
    c.decision(740, 190, 220, 150, ["Does it connect", "and ask to log in?"], "orange")
    c.card(1010, 118, 300, 96, "check", "green", "The share is fine", "restart avahi-daemon", layout="row", tcls="tl")
    c.card(1010, 262, 300, 96, "warn", "red", "Troubleshooting", "see chapter 8", layout="row", tcls="tl")
    c.link(246, 190, 264, 190, "orange", width=2)
    c.link(596, 190, 626, 190, "blue", width=2)
    c.link(795, 140, 860, 118, "green")
    c.link(795, 240, 860, 262, "red")
    c.link_label(826, 114, "yes", "green", 13)
    c.link_label(826, 266, "no", "red", 13)
    return c


def restore():
    c = Canvas(1200, 420, "How to get things back",
               "For one file, browse Time Machine from the menu bar. For a new Mac, use Setup Assistant. For a wiped Mac, boot into macOS Recovery.",
               glows=("green", "blue"))
    c.eyebrow(56, 58, "Getting things back", "teal")
    c.card(190, 230, 250, 170, "tm", "blue", "Need something back?", None, tcls="tl", sub_lines=["Pick the closest case"])
    opts = [
        ("doc", "green", "One file or folder", "Menu bar → Browse Time Machine Backups,\npick a date, click Restore"),
        ("laptop", "teal", "A new Mac", "Setup Assistant → Transfer from a\nTime Machine backup"),
        ("refresh", "orange", "A wiped Mac", "Boot into macOS Recovery →\nRestore from Time Machine"),
    ]
    for i, (ic, col, t, s) in enumerate(opts):
        y = 120 + i * 112
        c.card(800, y, 640, 96, ic, col, t, None, layout="row", tcls="tl", sub_lines=s.split("\n"))
        c.link(320, 230, 478, y, col)
    return c


def boot_order():
    c = Canvas(1200, 520, "What happens when the Pi boots",
               "Power on, Linux starts, the USB disk appears, and the system checks whether it mounted. If yes, Samba starts, then Avahi and SMART monitoring, and Macs can back up. If not, the boot carries on but Samba stays stopped so it never serves an empty folder.",
               glows=("green", "red"))
    c.eyebrow(56, 58, "The boot sequence", "teal")
    xs = [104, 270, 436, 602, 768, 934, 1100]
    cy = 190
    main = [
        ("bolt", "orange", "Power on", "the Pi starts"),
        ("terminal", "blue", "Linux starts", "systemd runs"),
        ("drive", "purple", "Disk appears", "waits up to 30 s"),
        (None, "orange", "Mounted?", "/srv/timemachine"),
        ("server", "teal", "Samba starts", "after the mount"),
        ("broadcast", "purple", "Avahi + SMART", "announce, watch"),
        ("check", "green", "Ready", "Macs back up"),
    ]
    for x, (ic, col, t, s) in zip(xs, main):
        if ic is None:
            c.decision(x, cy, 160, 160, ["Mounted?", ""], "orange")
            c.text(x, cy + 22, "/srv/timemachine", "s", fill=INK2, extra='style="font-size:13px"')
            continue
        c.card(x, cy, 148, 170, ic, col, t, s, tcls="tl", tile=50)
    for i in range(len(xs) - 1):
        a = xs[i] + (80 if i + 1 == 3 else 74) + 3
        b = xs[i + 1] - (80 if i + 1 == 3 else 74) - 3
        if i == 2:
            a = xs[i] + 74 + 3
        c.link(a, cy, b, cy, "green" if i >= 3 else "teal", width=2.4)
    c.link_label(685, cy - 36, "yes", "green", 13)
    # failure branch
    c.link(xs[3], cy + 80, xs[3], 340, "red", vertical=True, straight=True, dashed=True)
    c.link_label(xs[3] + 36, 305, "no", "red", 13)
    c.card(xs[3] + 22, 410, 330, 100, "warn", "orange", "Boot carries on anyway", "thanks to nofail", layout="row", tcls="tl")
    c.card(xs[3] + 22 + 360 + 24, 410, 330, 100, "x", "red", "Samba stays stopped", "never serves an empty folder", layout="row", tcls="tl")
    c.link(xs[3] + 22 + 165 + 2, 410, xs[3] + 22 + 360 + 24 - 165 - 2, 410, "red", width=2.2)
    c.text(56, 410, "If the disk is missing:", "s", anchor="start", fill=INK2)
    return c
