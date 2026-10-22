#!/usr/bin/env bash
# Read-only health check. Changes nothing. Exit code is the number of failed checks.
# Usage: sudo ./scripts/verify.sh
set -uo pipefail
source "$(dirname "$0")/lib.sh"
need_root
load_config

FAILS=0
ok()   { printf '  \033[32mPASS\033[0m  %s\n' "$*"; }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$*"; FAILS=$((FAILS + 1)); }
note() { printf '  \033[33mWARN\033[0m  %s\n' "$*"; }

echo "Drive"
mountpoint -q "$MOUNT_POINT" && ok "$MOUNT_POINT is mounted ($(df -h --output=size,avail "$MOUNT_POINT" | tail -1 | awk '{print $1" total, "$2" free"}'))" || bad "$MOUNT_POINT is not mounted"
grep -E "[[:space:]]${MOUNT_POINT}[[:space:]]" /etc/fstab | grep -q '^UUID=' && ok "fstab mounts by UUID" || bad "no UUID entry in /etc/fstab"
grep -E "[[:space:]]${MOUNT_POINT}[[:space:]]" /etc/fstab | grep -q nofail && ok "fstab has nofail" || bad "fstab entry lacks nofail"
if smartctl -d "$SMART_DEVICE_TYPE" -H "$DISK" 2>/dev/null | grep -q PASSED; then ok "SMART health: PASSED"; else bad "SMART health check did not pass for $DISK"; fi

echo "Services"
for s in smbd avahi-daemon smartmontools; do
  systemctl is-active --quiet "$s" && ok "$s is running" || bad "$s is not running"
  systemctl is-enabled --quiet "$s" && ok "$s starts at boot" || bad "$s is not enabled at boot"
done
[[ -f /etc/systemd/system/smbd.service.d/wait-for-drive.conf ]] && ok "smbd waits for the drive" || bad "smbd does not wait for the drive (run step 4)"

echo "Samba"
ver="$(smbd --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
case "$ver" in
  4.21.*|4.22.[0-5]) bad "Samba $ver has the macOS 26 Time Machine bug. Need 4.22.6 or newer." ;;
  "") bad "Could not read the Samba version" ;;
  *) ok "Samba $ver" ;;
esac
testparm -s >/dev/null 2>&1 && ok "smb.conf is valid" || bad "smb.conf has errors (run: testparm)"
for u in $USERS; do
  sh="$(share_name "$u")"
  testparm -s 2>/dev/null | grep -qi "^\[$sh\]" && ok "share $sh exists" || bad "share $sh is missing"
  pdbedit -L 2>/dev/null | grep -q "^$u:" && ok "Samba user $u exists" || bad "Samba user $u has no password (run: sudo smbpasswd -a $u)"
  [[ "$(stat -c '%U %a' "$MOUNT_POINT/$u" 2>/dev/null)" == "$u 700" ]] && ok "$MOUNT_POINT/$u is owned by $u, mode 700" || bad "$MOUNT_POINT/$u has wrong owner or mode"
done
testparm -s 2>/dev/null | grep -qiE '^\[(homes|printers|print\$)\]' && note "default shares [homes]/[printers]/[print\$] are still enabled (run step 3)" || ok "no unneeded default shares"

echo "Bonjour"
xmllint --noout "$AVAHI_FILE" 2>/dev/null && ok "$AVAHI_FILE is valid XML" || bad "$AVAHI_FILE is missing or invalid"
for u in $USERS; do grep -q "adVN=$(share_name "$u")," "$AVAHI_FILE" 2>/dev/null && ok "advertising $(share_name "$u")" || bad "$(share_name "$u") is not advertised"; done

echo "System"
[[ -e /var/run/reboot-required ]] && note "a reboot is pending" || ok "no reboot pending"
failed="$(systemctl --failed --no-legend | wc -l)"
[[ "$failed" -eq 0 ]] && ok "no failed systemd units" || bad "$failed failed systemd unit(s): $(systemctl --failed --no-legend | awk '{print $2}' | tr '\n' ' ')"

echo
[[ $FAILS -eq 0 ]] && log "All checks passed." || warn "$FAILS check(s) failed."
exit "$FAILS"
