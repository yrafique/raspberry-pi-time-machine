#!/usr/bin/env bash
# Remove a Mac's share and login. Its backup folder is KEPT unless you pass --delete-data.
# Usage: sudo ./scripts/remove-mac.sh <name> [--delete-data]
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root
[[ $# -ge 1 ]] || die "Usage: sudo $0 <name> [--delete-data]"
OLD="$1"
DELETE_DATA="${2:-}"
load_config

found=0; keep=()
for u in $USERS; do
  if [[ $u == "$OLD" ]]; then found=1; else keep+=("$u"); fi
done
[[ $found -eq 1 ]] || die "'$OLD' is not in USERS in $CONFIG_FILE."
[[ ${#keep[@]} -gt 0 ]] || die "That is the last user. Remove the whole setup by hand instead."

sed -i -E "s/^USERS=.*/USERS=\"${keep[*]}\"/" "$CONFIG_FILE"
pdbedit -x -u "$OLD" 2>/dev/null || true
userdel "$OLD" 2>/dev/null || true

"$(dirname "$0")/03-configure-shares.sh"

if [[ $DELETE_DATA == "--delete-data" ]]; then
  log "Deleting $MOUNT_POINT/$OLD"
  rm -rf "${MOUNT_POINT:?}/$OLD"
else
  log "Backups kept in $MOUNT_POINT/$OLD (owned by a now-deleted user). Delete the folder to reclaim the space."
fi
