<p align="center"><sub><a href="06-persistence-and-hardening.md">← Previous</a> &nbsp;·&nbsp; 🏠 <a href="../README.md">Home</a> &nbsp;·&nbsp; <b>Chapter 7 of 9</b> &nbsp;·&nbsp; ▰▰▰▰▰▰▰▱▱ &nbsp;·&nbsp; <a href="08-troubleshooting.md">Next: Troubleshooting →</a></sub></p>

# 🚀 7. Speed

Three things limit speed: the **disk**, the **Pi's network port**, and your **Mac's connection** (Wi-Fi or wired).

## 🏁 7.1 Where the bottleneck is

Data from the Mac passes through four links. The slowest one sets the speed.

```mermaid
flowchart LR
    mac["💻 Mac"] -->|"📶 Wi-Fi<br/>about 15 to 60 MB/s"| router(["📡 Router"])
    router -->|"🔌 Gigabit Ethernet<br/>about 110 MB/s"| pi["🍓 Pi"]
    pi -->|"🔗 USB 3.0<br/>about 400 MB/s"| disk[("💾 Disk<br/>about 145 MB/s")]

    classDef slow fill:#fee2e2,stroke:#dc2626,color:#7f1d1d
    classDef mid fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef fast fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef n fill:#f1f5f9,stroke:#64748b,color:#1e293b
    class mac,router,pi n
    class disk mid
    linkStyle 0 stroke:#dc2626,stroke-width:4px
    linkStyle 1 stroke:#d97706,stroke-width:3px
    linkStyle 2 stroke:#16a34a,stroke-width:2px
```

On Wi-Fi, **the Wi-Fi is the bottleneck**. On Ethernet, the Pi's gigabit port (about 110 MB/s) is just below the disk's speed, so the **network is still the limit, not the disk**.

## 📏 7.2 What we measured

On a Raspberry Pi 4 with a USB 3.0 WD Red 2 TB (5400 RPM) on the blue USB port:

```mermaid
%%{init: {"xyChart": {"showDataLabel": true}, "themeVariables": {"xyChart": {"plotColorPalette": "#60a5fa, #f59e0b"}}}}%%
xychart-beta
    title "Speed in MB/s (higher is faster)"
    x-axis ["Disk write", "Disk read", "Gigabit best case", "Wi-Fi measured"]
    y-axis "MB per second" 0 --> 160
    bar [144, 145, 110, 15]
```

| | Test | Result |
|---|---|---|
| 💾 | Disk, sequential write | **144 MB/s** |
| 💾 | Disk, sequential read | **145 MB/s** |
| 🔌 | Gigabit Ethernet, best case | about 110 MB/s (a hardware limit, not measured) |
| 📶 | A real first backup over Wi-Fi (30-second sample) | **about 15 MB/s** |

The disk tests were run with `scripts/benchmark.sh`, which uses `dd` with direct I/O and a 2 GB file. The Wi-Fi figure was one short sample during the first backup and will vary a lot.

> [!NOTE]
> These are estimates for planning, not guarantees, apart from the measurements above. Time Machine is slower than a plain file copy because it sends many small files and has the sparsebundle overhead on top.

| Connection from the Mac | Best case | Typical Time Machine |
|---|---|---|
| 🔌 Wired gigabit | about 100 MB/s | roughly 30 to 60 MB/s |
| 📶 Wi-Fi | about 25 to 60 MB/s | often 10 to 30 MB/s |

## ⏳ 7.3 How long a first backup takes

```mermaid
%%{init: {"xyChart": {"showDataLabel": true}, "themeVariables": {"xyChart": {"plotColorPalette": "#60a5fa, #f59e0b"}}}}%%
xychart-beta
    title "First backup time in hours (lower is better)"
    x-axis ["100 GB", "500 GB", "1 TB"]
    y-axis "Hours" 0 --> 20
    bar [1.9, 9.3, 18.5]
    line [0.7, 3.5, 7]
```

The bars are for 15 MB/s (slow Wi-Fi). The line is for 40 MB/s (a good wired connection).

| Data on the Mac | At 15 MB/s | At 40 MB/s |
|---|---|---|
| 100 GB | 1.9 hours | 42 minutes |
| 500 GB | 9.3 hours | 3.5 hours |
| 1 TB | 18.5 hours | 7 hours |

Later backups are incremental and usually take a minute or two.

## 🔬 7.4 Measure yours

**The disk:**

```bash
sudo ./scripts/benchmark.sh
```

**The network between a Mac and the Pi:**

```bash
# on the Pi
sudo apt-get install -y iperf3
iperf3 -s

# on the Mac (install with: brew install iperf3)
iperf3 -c <pi-address>
```

`iperf3` reports the link speed in Mbit/s. Divide by 8 for MB/s. About 940 Mbit/s is the best a gigabit link does.

**The backup itself, while it runs:**

```bash
a=$(sudo du -sb /srv/timemachine/personal | cut -f1); sleep 30
b=$(sudo du -sb /srv/timemachine/personal | cut -f1)
echo "$(( (b-a)/30/1048576 )) MB/s"
```

## 🏎️ 7.5 Making it faster

```mermaid
flowchart TD
    start{"Backups slower<br/>than you'd like?"} --> w{"Is the Mac on<br/>Wi-Fi?"}
    w -- "yes" --> eth["🔌 Use Ethernet for the first backup<br/><b>The biggest single improvement</b>"]
    w -- "no" --> usb{"Does lsusb -t show<br/>5000M for the disk?"}
    usb -- "no, 480M" --> port["🟦 Move the disk to a blue USB 3.0 port<br/>and use a USB 3.0 cable"]
    usb -- "yes" --> link{"Does eth0 speed<br/>say 1000?"}
    link -- "no, 100" --> cable["🔧 Replace the Ethernet cable"]
    link -- "yes" --> ok["✅ You're at the hardware limit<br/>of a Pi 4 on gigabit"]

    classDef good fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef fix fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef q fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
    class eth,port,cable fix
    class ok good
    class start,w,usb,link q
```

1. **Use Ethernet on the Mac** for the first backup. It is the biggest single improvement.
2. **Check the disk is on a USB 3.0 port** with `lsusb -t`. `5000M` is right. `480M` is USB 2.0 and would cap you at about 35 MB/s.
3. **Check the Pi's link speed:** `cat /sys/class/net/eth0/speed` should print `1000`. A value of `100` points to a bad cable.
4. **Keep the Mac close to the router** if you must use Wi-Fi, and prefer the 5 GHz band.
5. **A Raspberry Pi 5**, or any faster computer, won't help much on gigabit Ethernet. It only matters if you also add a faster network.

---

<p align="center"><sub><a href="06-persistence-and-hardening.md">← Previous</a> &nbsp;·&nbsp; 🏠 <a href="../README.md">Home</a> &nbsp;·&nbsp; <b>Chapter 7 of 9</b> &nbsp;·&nbsp; <a href="08-troubleshooting.md">Next: Troubleshooting →</a></sub></p>
