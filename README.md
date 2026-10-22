<p align="center">
  <img src="docs/images/banner.svg" alt="Time Machine on a Raspberry Pi: a spare USB drive becomes a backup server for your Macs" width="100%">
</p>

<p align="center">
  <img alt="Raspberry Pi 4" src="https://img.shields.io/badge/Raspberry%20Pi-4-C51A4A?logo=raspberrypi&logoColor=white">
  <img alt="Debian 13" src="https://img.shields.io/badge/Debian-13%20trixie-A81D33?logo=debian&logoColor=white">
  <img alt="Samba 4.22" src="https://img.shields.io/badge/Samba-4.22.11-1F6FB2">
  <img alt="macOS 26" src="https://img.shields.io/badge/macOS-26%20Tahoe-000000?logo=apple&logoColor=white">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-2EA44F">
</p>

<h1 align="center">Time Machine on a Raspberry Pi</h1>

<p align="center"><b>Turn an old USB hard drive and a Raspberry Pi into a Time Machine backup server for your Macs.<br>No new hardware, and no old drive left on the shelf.</b></p>

This guide was built and tested on a Raspberry Pi 4 with a 2 TB WD Red drive that had been retired from an old NAS. Everything here is either a command you can paste or a script you can run, and every step says why it is there.

> [!CAUTION]
> Step 2 **erases the disk**. Copy anything you want to keep before you start.

## ✨ What you end up with

| | |
|---|---|
| 🔄 **Automatic backups** | Your Mac backs up every hour, on Wi-Fi or Ethernet, to a drive that sits quietly in a corner. |
| 👥 **One share per Mac** | Each Mac gets its own login, so a work laptop and a personal laptop can't read each other's backups. |
| 💾 **The whole disk** | All the space is shared. Each Mac prunes its own old backups, so there are no quotas to manage. |
| 🛡️ **It survives power cuts** | The server restarts by itself, waits for the disk, and watches the disk's health. |
| ⏱️ **About an hour of work** | Most of it is waiting for the first backup. |

```mermaid
flowchart LR
    m1["💻 MacBook<br/>personal"] <-->|"Wi-Fi or Ethernet"| router(["📡 Router"])
    m2["💻 MacBook<br/>work"] <-->|"Wi-Fi or Ethernet"| router
    router <-->|"Gigabit Ethernet"| pi["🍓 <b>Raspberry Pi</b><br/>Samba serves the share<br/>Avahi announces it"]
    pi <-->|"USB 3.0"| disk[("💾 USB disk<br/>2 TB, ext4")]

    classDef mac fill:#dbeafe,stroke:#2563eb,color:#1e293b
    classDef net fill:#f1f5f9,stroke:#64748b,color:#1e293b
    classDef svc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef store fill:#fef3c7,stroke:#d97706,color:#78350f
    class m1,m2 mac
    class router net
    class pi svc
    class disk store
```

## 🧰 What you need

| | Item | Notes |
|---|---|---|
| 🍓 | **A Raspberry Pi** | Tested on a Pi 4 Model B. A Pi 3 works but is slower; a Pi 5 is faster. |
| 💾 | **A USB hard drive** | Any size. A 2.5" drive can run from the Pi's USB power; a 3.5" drive needs its own power supply. |
| 🔌 | **An Ethernet cable** | Wired is strongly recommended for the Pi. The first backup is large. |
| 💳 | **A microSD card** | For Raspberry Pi OS. Debian 13 "trixie" was tested. |
| 💻 | **A Mac on macOS 11 (Big Sur) or later** | Tested with macOS 26 (Tahoe). |

## 🗺️ The route

```mermaid
flowchart LR
    a["🍓 <b>1. Prepare the Pi</b><br/>flash, SSH,<br/>fixed address"] --> b["💾 <b>2. Prepare the drive</b><br/>erase, format,<br/>mount at boot"]
    b --> c["⚙️ <b>3. Install the server</b><br/>Samba, Bonjour,<br/>users and shares"]
    c --> d["💻 <b>4. Connect your Macs</b><br/>add the disk in<br/>Time Machine"]
    d --> e["🛡️ <b>5. Make it solid</b><br/>boot order,<br/>health, reboot test"]

    classDef step fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
    classDef danger fill:#fee2e2,stroke:#dc2626,color:#7f1d1d
    classDef done fill:#dcfce7,stroke:#16a34a,color:#14532d
    class a,c,d step
    class b danger
    class e done
```

## ⚡ The quick version

On the Pi, once the OS is installed and you can reach it over SSH:

```bash
sudo apt-get install -y git
git clone https://github.com/yrafique/raspberry-pi-time-machine.git timemachine-pi && cd timemachine-pi
cp config.env.example config.env && nano config.env     # choose your disk and one name per Mac
sudo ./scripts/setup-all.sh                              # installs, ERASES the disk, configures, checks
```

Then on each Mac: **System Settings → General → Time Machine → Add Backup Disk**. The details are in [chapter 5](docs/05-connect-your-macs.md).

## 📖 The book

Read it in order the first time. Each chapter ends with a link to the next.

| | Chapter | What it covers |
|---|---|---|
| 🧠 | [1. How it works](docs/01-how-it-works.md) | The pieces, why Samba, and what to expect |
| 🍓 | [2. Prepare the Pi](docs/02-prepare-the-pi.md) | The OS, SSH, a fixed address, updates |
| 💾 | [3. Prepare the drive](docs/03-prepare-the-drive.md) | Find, erase, format and mount the disk |
| ⚙️ | [4. Install the server](docs/04-install-the-server.md) | Packages, Samba, Bonjour, users and shares |
| 💻 | [5. Connect your Macs](docs/05-connect-your-macs.md) | Add the disk, the first backup, restoring |
| 🛡️ | [6. Make it survive reboots](docs/06-persistence-and-hardening.md) | Boot order, disk health, a reboot test |
| 🚀 | [7. Speed](docs/07-performance.md) | What we measured, and how to measure yours |
| 🩺 | [8. Troubleshooting](docs/08-troubleshooting.md) | The macOS 26 Samba bug, managed work laptops, every error we hit |
| 🧹 | [9. Maintenance](docs/09-maintenance.md) | Updates, adding or removing a Mac, health checks |

## 🗂️ What is in this repository

```
.
├── README.md                    this page
├── requirements-apt.txt         every package that gets installed, and why
├── config.env.example           your settings: disk, mount point, one name per Mac
├── scripts/
│   ├── setup-all.sh             runs steps 1 to 4, then verify
│   ├── 01-install-packages.sh   installs requirements-apt.txt
│   ├── 02-prepare-drive.sh      ERASES the disk, partitions, formats, mounts at boot
│   ├── 03-configure-shares.sh   users, folders, Samba shares, Bonjour
│   ├── 04-harden.sh             start order, boot at startup, SMART monitoring
│   ├── add-mac.sh               add another Mac later
│   ├── remove-mac.sh            remove a Mac's share
│   ├── verify.sh                read-only health check
│   └── benchmark.sh             measures the drive's raw speed
├── config/mac/nsmb.conf         optional Mac-side workaround, see chapter 8
└── docs/                        the chapters and their images
```

## ✅ What was tested

| | |
|---|---|
| 🍓 Hardware | Raspberry Pi 4 Model B, WD Red 2 TB (WD20EFRX) in a USB 3.0 enclosure, gigabit Ethernet |
| 🐧 OS | Debian GNU/Linux 13 (trixie), 64-bit, kernel 6.18 |
| 🗂️ Server | Samba 4.22.11 from the Debian repository |
| 💻 Client | macOS 26 (Tahoe) over SMB 3.1.1 |

The scripts were run against that system. Step 2 (erasing a disk) was done by hand with the same commands the script uses, so if you hit a problem in a script, please [open an issue](https://github.com/yrafique/raspberry-pi-time-machine/issues).

## 🤔 Why not just buy a NAS?

You can, and that is a fine answer. This is for when you already own a spare Pi and a drive, you want to keep them out of the landfill, and you don't mind learning a little along the way.

## 📄 License

[MIT](LICENSE). Use it, copy it, change it, share it.
