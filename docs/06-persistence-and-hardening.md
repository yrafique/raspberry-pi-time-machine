# 6. Make it survive reboots

← Previous: [Connect your Macs](05-connect-your-macs.md) · [Home](../README.md) · Next: [Speed →](07-performance.md)

A backup server has to come back by itself after a power cut. This chapter covers what has to happen at boot, and how to prove that it does.

**The easy way:** `sudo ./scripts/04-harden.sh`. Below is what it does.

## 6.1 What must happen at boot

1. The disk is found and mounted at `/srv/timemachine`.
2. **Then** Samba starts, so it never shares an empty folder.
3. Avahi starts, so Macs can find the share.
4. SMART monitoring starts, so a failing disk gets noticed.

Items 3 and 4 are one `systemctl enable`. Items 1 and 2 need two small settings.

### Mount that can't block the boot

The `fstab` line from [chapter 3](03-prepare-the-drive.md) has two options for this:

```
UUID=<uuid> /srv/timemachine ext4 defaults,noatime,nofail,x-systemd.device-timeout=30 0 2
```

`nofail` means a missing or dead disk doesn't stop the Pi booting, and `x-systemd.device-timeout=30` limits the wait to 30 seconds. Without `nofail`, a disconnected USB cable could leave the Pi stuck in emergency mode, unreachable over SSH.

### Samba waits for the disk

A systemd drop-in adds one dependency to Samba:

```bash
sudo mkdir -p /etc/systemd/system/smbd.service.d
sudo tee /etc/systemd/system/smbd.service.d/wait-for-drive.conf <<'EOF'
[Unit]
RequiresMountsFor=/srv/timemachine
EOF
sudo systemctl daemon-reload
```

`RequiresMountsFor` makes Samba start only after `/srv/timemachine` is mounted. If the disk fails to mount, Samba stays stopped instead of serving an empty folder, which would make a Mac think its backup was gone and start a new one.

### Enable at boot

```bash
sudo systemctl enable smbd avahi-daemon smartmontools
```

## 6.2 Watch the disk's health

Hard drives usually warn before they fail. `smartd` reads the drive's own health counters and logs problems.

For a drive in a USB enclosure, `smartd` needs to be told how to talk to it, or it fails to start with `exit status 17`. Most USB-to-SATA bridges need `-d sat`. Replace the contents of `/etc/smartd.conf` with:

```
/dev/sda -d sat -a -n standby,q -s (S/../.././03|L/../../7/04)
```

| Part | Meaning |
|---|---|
| `-d sat` | Talk to the drive through a USB-to-SATA bridge. |
| `-a` | Monitor all health attributes. |
| `-n standby,q` | Don't wake a sleeping drive for a check, and stay quiet about it. |
| `-s (S/../.././03\|L/../../7/04)` | A short self-test every day at 03:00 and a long one every Sunday at 04:00. |

Keep the original: `sudo cp -n /etc/smartd.conf /etc/smartd.conf.orig`. Then:

```bash
sudo systemctl enable --now smartmontools
systemctl is-active smartmontools
```

### Read the numbers yourself

```bash
sudo smartctl -d sat -H /dev/sda                    # overall verdict: PASSED or FAILED
sudo smartctl -d sat -A /dev/sda | grep -E 'Reallocated_Sector|Current_Pending|Offline_Uncorrectable|Power_On_Hours|Temperature'
```

| Attribute | Good value | Why it matters |
|---|---|---|
| `Reallocated_Sector_Ct` | 0 | Sectors the drive had to give up on. Rising numbers mean a dying disk. |
| `Current_Pending_Sector` | 0 | Sectors waiting to be reallocated. |
| `Offline_Uncorrectable` | 0 | Sectors the drive could not read at all. |
| `Power_On_Hours` | information only | Our example disk had 41,250 (4.7 years) and was still healthy. |
| `Temperature_Celsius` | under about 45 | Ours ran at 34 °C. |

Replace the disk when any of the first three stop being zero.

## 6.3 Prove it: reboot test

Don't trust it until you've seen it. **Only do this when no backup is running**, since a reboot stops any running backup.

1. Check nothing is connected: `sudo smbstatus -b`
2. Reboot: `sudo reboot`
3. Wait a minute or two, SSH back in, and run:

```bash
sudo ./scripts/verify.sh
```

Every line should say `PASS`. In particular, check that `/srv/timemachine` is mounted, that `smbd` and `avahi-daemon` are running, and that no systemd unit has failed.

4. On a Mac, open Time Machine settings. The share should still be selectable, and the next backup should run on its own.

Then try the failure case once: **power the Pi off, unplug the USB drive, power it on.** It should boot, SSH should work, and `smbd` should be stopped. Plug the drive back in and run `sudo reboot` to restore normal service.

## 6.4 Updates

Install updates now and then, but not in the middle of a backup:

```bash
sudo apt-get update && sudo apt-get -y full-upgrade
sudo ./scripts/verify.sh
```

`verify.sh` checks the Samba version, so a Debian update that breaks Time Machine shows up straight away.

← Previous: [Connect your Macs](05-connect-your-macs.md) · [Home](../README.md) · Next: [Speed →](07-performance.md)
