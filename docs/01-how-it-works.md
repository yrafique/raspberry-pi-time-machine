# 1. How it works

[Home](../README.md) · Next: [Prepare the Pi →](02-prepare-the-pi.md)

## The idea

Time Machine can back up to a disk attached to a Mac, or to a **network share**. A network share is just a folder that your Mac reaches over your home network. The Raspberry Pi hosts that folder, and the USB drive gives it room to grow.

```
 MacBook ──┐                                     ┌────────────────────────────┐
           │  Wi-Fi or Ethernet     ┌──────────┐ │  USB 3.0                   │
 MacBook ──┼────── your router ─────┤ Raspberry├─┤  2 TB hard drive           │
           │                        │    Pi    │ │  /srv/timemachine          │
 (more) ───┘                        └──────────┘ │    ├─ personal/  ← Mac 1   │
                                      Samba      │    └─ work/      ← Mac 2   │
                                      Avahi      └────────────────────────────┘
```

## The three pieces

| Piece | What it does | Package |
|---|---|---|
| **Samba** | Shares folders using SMB, the protocol Macs use for file sharing. Its `vfs_fruit` module adds the Apple extensions that Time Machine requires. | `samba` |
| **Avahi** | Announces the share over Bonjour, so your Mac lists it in Time Machine without you typing an address. | `avahi-daemon` |
| **ext4 disk** | An ordinary Linux filesystem. Time Machine stores its data in a disk image (a *sparsebundle*), so the disk itself doesn't need an Apple format. | `parted`, `e2fsprogs` |

### Why SMB and Samba?

Apple removed the older AFP protocol, and Time Machine over SMB is now the supported route for network backups. Samba has supported it since version 4.8 through `fruit:time machine = yes`. Other options exist, such as a dedicated NAS operating system or a Docker image, but they hide the details. This guide uses plain Samba so that you can see and change every part.

### Why one share per Mac?

Each Mac creates its own backup file inside the share. Two Macs could safely share one folder, but a separate share and login for each gives you three things:

1. One Mac can't read or delete the other's backups.
2. A work laptop and a personal laptop stay separate. This matters if the work laptop's policy allows backups at all (see [chapter 8](08-troubleshooting.md#managed-work-laptops-and-vpn-clients)).
3. You can remove one Mac cleanly later.

### Why no quotas?

All Macs share the whole disk. Time Machine deletes a Mac's oldest backups when space runs low, so each Mac manages itself. The catch is that one Mac that backs up far more data can crowd out the others. If that worries you, set a limit per share with `fruit:time machine max size = 900G` in the share block.

## What to expect

- **First backup:** slow. It copies everything. Plan for hours (see [chapter 7](07-performance.md)).
- **After that:** hourly incremental backups, usually a minute or two.
- **Disk space:** a first backup is roughly the size of the data on your Mac. Time Machine then keeps hourly backups for 24 hours, daily for a month, and weekly after that, until the disk fills.
- **The Pi must be on** when your Mac wants to back up. If it is off, the Mac skips the backup and tries again later.

## Where this can go wrong

| Risk | How this guide handles it |
|---|---|
| The disk dies | The drive is monitored with SMART ([chapter 6](06-persistence-and-hardening.md)). A backup disk is a second copy, not the only copy; keep that in mind for irreplaceable files. |
| A Samba update breaks Time Machine | See the macOS 26 bug in [chapter 8](08-troubleshooting.md). `verify.sh` checks your version. |
| The Pi reboots before the disk is ready | Samba is told to wait for the disk to mount ([chapter 6](06-persistence-and-hardening.md)). |
| Someone on your network reads your backups | Each share needs its own username and password, and the folders are private to their user. Backups are not encrypted by default. Turn on encryption in Time Machine if the Pi is in a shared space ([chapter 5](05-connect-your-macs.md)). |

[Home](../README.md) · Next: [Prepare the Pi →](02-prepare-the-pi.md)
