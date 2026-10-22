#!/usr/bin/env bash
# Step 1: install every package listed in requirements-apt.txt.
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root

REQ="$REPO_ROOT/requirements-apt.txt"
[[ -f "$REQ" ]] || die "Missing $REQ"

mapfile -t PKGS < <(sed -e 's/#.*//' -e 's/[[:space:]]*$//' "$REQ" | grep -v '^$')
log "Installing: ${PKGS[*]}"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y "${PKGS[@]}"

log "Installed Samba version: $(dpkg-query -W -f='${Version}' samba)"
log "Done. Samba must be 4.22.6 or newer (or 4.20 and older) for macOS 26 clients; see docs/08-troubleshooting.md."
