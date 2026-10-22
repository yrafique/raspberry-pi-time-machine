#!/usr/bin/env bash
# Step 4: make the setup survive reboots and watch the disk's health.
#  - Samba waits for the drive to be mounted before it starts
#  - Samba, Avahi and SMART monitoring start at boot
#  - the mount can't hang the boot if the drive is missing
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root
load_config

log "Making smbd wait for $MOUNT_POINT"
mkdir -p /etc/systemd/system/smbd.service.d
cat > /etc/systemd/system/smbd.service.d/wait-for-drive.conf <<EOF
[Unit]
RequiresMountsFor=$MOUNT_POINT
EOF

log "Checking /etc/fstab options"
if grep -qE "[[:space:]]${MOUNT_POINT}[[:space:]]" /etc/fstab; then
  grep -E "[[:space:]]${MOUNT_POINT}[[:space:]]" /etc/fstab | grep -q 'nofail' || warn "fstab line for $MOUNT_POINT has no 'nofail'. A missing drive could block boot."
  grep -E "[[:space:]]${MOUNT_POINT}[[:space:]]" /etc/fstab | grep -q 'x-systemd.device-timeout' \
    || sed -i -E "\|[[:space:]]${MOUNT_POINT}[[:space:]]|s/nofail/nofail,x-systemd.device-timeout=30/" /etc/fstab
else
  warn "No fstab entry for $MOUNT_POINT. Run step 2 first."
fi
findmnt --verify 2>&1 | tail -2

log "Configuring SMART monitoring for $DISK (device type: $SMART_DEVICE_TYPE)"
[[ -f /etc/smartd.conf.orig ]] || cp /etc/smartd.conf /etc/smartd.conf.orig
# Short self-test daily at 03:00, long self-test Sundays at 04:00. 'standby' skips a sleeping drive.
echo "$DISK -d $SMART_DEVICE_TYPE -a -n standby,q -s (S/../.././03|L/../../7/04)" > /etc/smartd.conf

systemctl daemon-reload
systemctl enable smbd avahi-daemon smartmontools >/dev/null 2>&1
systemctl restart smartmontools
systemctl is-active --quiet smartmontools || warn "smartmontools did not start. Check: journalctl -u smartmontools"

log "Done. A reboot test is described in docs/06-persistence-and-hardening.md."
