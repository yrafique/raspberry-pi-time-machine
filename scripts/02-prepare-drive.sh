#!/usr/bin/env bash
# Step 2: ERASE the disk named in config.env, create one ext4 partition,
# and mount it permanently at MOUNT_POINT. DESTRUCTIVE.
#
# To skip the interactive confirmation (automation only):
#   sudo CONFIRM_WIPE=/dev/sda ./scripts/02-prepare-drive.sh
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root
load_config

[[ -b "$DISK" ]] || die "$DISK is not a block device."

# Safety: never touch the disk the system is running from.
root_src="$(findmnt -no SOURCE / || true)"
root_disk="/dev/$(lsblk -no PKNAME "$root_src" 2>/dev/null | head -1)"
boot_src="$(findmnt -no SOURCE /boot/firmware 2>/dev/null || findmnt -no SOURCE /boot 2>/dev/null || true)"
boot_disk=""
[[ -n "$boot_src" ]] && boot_disk="/dev/$(lsblk -no PKNAME "$boot_src" 2>/dev/null | head -1)"
[[ "$DISK" != "$root_disk" && "$DISK" != "$boot_disk" ]] || die "$DISK is the disk the system boots from. Refusing."

log "About to ERASE this disk:"
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,LABEL,MOUNTPOINT "$DISK"
echo
if [[ "${CONFIRM_WIPE:-}" != "$DISK" ]]; then
  read -r -p "Type the device path ($DISK) to erase everything on it: " answer
  [[ "$answer" == "$DISK" ]] || die "Not confirmed. Nothing was changed."
fi

log "Unmounting and clearing old signatures"
for p in $(lsblk -nrpo NAME "$DISK" | tail -n +2); do
  umount "$p" 2>/dev/null || true
  swapoff "$p" 2>/dev/null || true
  wipefs -a "$p" >/dev/null 2>&1 || true
done
wipefs -a "$DISK" >/dev/null

log "Creating a GPT partition table and one partition"
parted -s "$DISK" mklabel gpt mkpart "$LABEL" ext4 1MiB 100%
partprobe "$DISK" || true
udevadm settle
sleep 1
PART="$(lsblk -nrpo NAME "$DISK" | sed -n 2p)"
[[ -b "$PART" ]] || die "Could not find the new partition on $DISK."

log "Formatting $PART as ext4 (label '$LABEL', no reserved blocks)"
mkfs.ext4 -F -L "$LABEL" -m 0 "$PART"
UUID="$(blkid -s UUID -o value "$PART")"
[[ -n "$UUID" ]] || die "Could not read the UUID of $PART."

log "Adding to /etc/fstab (UUID=$UUID -> $MOUNT_POINT)"
mkdir -p "$MOUNT_POINT"
sed -i "\|[[:space:]]${MOUNT_POINT}[[:space:]]|d" /etc/fstab
echo "UUID=$UUID $MOUNT_POINT ext4 defaults,noatime,nofail,x-systemd.device-timeout=30 0 2" >> /etc/fstab
systemctl daemon-reload
mount "$MOUNT_POINT"

log "Done:"
df -h "$MOUNT_POINT"
