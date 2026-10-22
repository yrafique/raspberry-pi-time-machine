<p align="center"><sub><a href="04-install-the-server.md">← Previous</a> &nbsp;·&nbsp; 🏠 <a href="../README.md">Home</a> &nbsp;·&nbsp; <b>Chapter 5 of 9</b> &nbsp;·&nbsp; ▰▰▰▰▰▱▱▱▱ &nbsp;·&nbsp; <a href="06-persistence-and-hardening.md">Next: Make it survive reboots →</a></sub></p>

# 💻 5. Connect your Macs

```mermaid
flowchart LR
    subgraph s1["1️⃣ Set up · a few minutes"]
        direction TB
        a1["Open Time Machine<br/>settings"] --> a2["Pick the share"] --> a3["Sign in with that<br/>share's login"] --> a4["Choose<br/>encryption"]
    end
    subgraph s2["2️⃣ First backup · hours"]
        direction TB
        b1["The Mac prepares<br/>the backup"] --> b2["Copies everything<br/>to the Pi"]
    end
    subgraph s3["3️⃣ Every day · minutes"]
        direction TB
        c1["Hourly incremental<br/>backups"] --> c2["Restore a file<br/>when you need it"]
    end
    s1 --> s2 --> s3

    classDef a fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
    classDef b fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef c fill:#dcfce7,stroke:#16a34a,color:#14532d
    class a1,a2,a3,a4 a
    class b1,b2 b
    class c1,c2 c
```

## ➕ 5.1 Add the backup disk

On each Mac:

1. Open **System Settings → General → Time Machine**.
2. Click **Add Backup Disk** (the **+** button).
3. Choose your share, for example `TimeMachine-Personal`.
4. Click **Set Up Disk**.
5. Sign in with that share's **username** (`personal`) and the **password** you set with `smbpasswd`. Use the matching pair for each Mac. A Mac that tries another Mac's login is refused.
6. Decide on **encryption**.

> [!TIP]
> Turning on **Encrypt Backup** is a good idea if the Pi is in a shared space, because backups are readable on the Pi's disk otherwise. Keep the password somewhere safe: a lost password means the backup can't be read.

The Mac starts the first backup right away.

### 🔍 If the share doesn't appear in the list

Time Machine only lists shares that Bonjour announces. Try connecting directly first:

```mermaid
flowchart TD
    a["Share missing in<br/>Time Machine's list"] --> b["Finder → Go → Connect to Server<br/>smb://pi-address/TimeMachine-Personal"]
    b --> c{"Does it connect<br/>and ask for a login?"}
    c -- "yes" --> d["✅ The share is fine.<br/>Only Bonjour is the problem:<br/>sudo systemctl restart avahi-daemon"]
    c -- "no" --> e["🩺 Go to chapter 8,<br/>Troubleshooting"]

    classDef ok fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef bad fill:#fee2e2,stroke:#dc2626,color:#7f1d1d
    classDef n fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
    class d ok
    class e bad
    class a,b,c n
```

You can also add the disk from Terminal:

```bash
sudo tmutil setdestination -a "smb://personal@<pi-address>/TimeMachine-Personal"
```

It asks for the password.

## 🐢 5.2 The first backup

Expect it to take a long time. The first backup copies everything, and the network is the limit, not the disk. A rough guide from our tests (see [chapter 7](07-performance.md)):

| Connection | Roughly how long for 500 GB |
|---|---|
| 🔌 Wired gigabit | 3 to 5 hours |
| 📶 Wi-Fi | 9 hours or more |

Tips for the first run:

- 🔋 Plug the Mac in and keep it awake. A sleeping Mac pauses the backup. It resumes by itself when the Mac wakes, but the backup then takes longer overall.
- 🔌 Put the Mac on **wired Ethernet** for the first backup if you can. A USB-C Ethernet adapter is enough.
- 🚫 Don't restart the Pi or Samba during the first backup.

You can watch progress in System Settings → General → Time Machine, or from the Pi:

```bash
sudo du -sh /srv/timemachine/*          # the folder grows as data arrives
sudo smbstatus -b                       # who is connected right now
```

> [!NOTE]
> An empty folder for the first few minutes is normal. Time Machine spends that time "preparing" before it creates its backup file.

When it finishes, there is a file named like `<Your Mac's name>.sparsebundle` in the share's folder on the Pi.

## 🐇 5.3 Later backups

After the first backup, Time Machine runs hourly while the Mac is awake and on your network. These are quick because only the changes are copied.

If the Pi is off or unreachable, the Mac skips that backup and says the last one was a while ago. Nothing is lost.

This is what a working setup looks like in System Settings → General → Time Machine, after several days of backups to a 2 TB disk. It shows the share and server, the free space, the encryption, the date range of backups, and the hourly schedule:

![Time Machine settings showing the TimeMachine-Personal share on the Pi, 1.83 TB available, Encrypted, with backups from 2026-10-18 to today and the next backup set to Automatic (hourly)](images/time-machine-working.png)

## ♻️ 5.4 Restoring files

```mermaid
flowchart TD
    q{"What do you need<br/>to get back?"}
    q -->|"one file or folder"| one["📄 Open the folder in Finder<br/>⏰ menu bar → Browse Time Machine Backups<br/>pick a date, click Restore"]
    q -->|"a whole Mac<br/>(new or wiped)"| whole{"Is macOS still<br/>installed?"}
    whole -->|"yes, new Mac"| ma["🧳 Setup Assistant →<br/>Transfer from Time Machine backup"]
    whole -->|"no, wiped"| rec["🛟 Boot into macOS Recovery →<br/>Restore from Time Machine"]

    classDef n fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e
    classDef ok fill:#dcfce7,stroke:#16a34a,color:#14532d
    class q,whole n
    class one,ma,rec ok
```

- **A single file or folder:** open the folder in Finder, click the Time Machine icon in the menu bar, and choose **Browse Time Machine Backups**.
- **A new Mac:** in Setup Assistant choose **Transfer Information to This Mac → From a Mac, Time Machine backup, or Startup disk**, then pick the network backup.
- **A wiped Mac:** boot into macOS Recovery (hold the power button on Apple silicon, or ⌘R on Intel), choose **Restore from Time Machine**, and pick the network share.

> [!IMPORTANT]
> **Test a restore now**, while nothing is wrong. Open Time Machine, browse to a file, and restore a copy to your Desktop. A backup you have never restored from is only a hope.

---

<p align="center"><sub><a href="04-install-the-server.md">← Previous</a> &nbsp;·&nbsp; 🏠 <a href="../README.md">Home</a> &nbsp;·&nbsp; <b>Chapter 5 of 9</b> &nbsp;·&nbsp; <a href="06-persistence-and-hardening.md">Next: Make it survive reboots →</a></sub></p>
