#!/usr/bin/env bash
# Add another Mac: adds a user to config.env, creates its share, asks for a password.
# Usage: sudo ./scripts/add-mac.sh <name>
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root
[[ $# -eq 1 ]] || die "Usage: sudo $0 <name>   (e.g. 'laptop')"
NEW="$1"
[[ $NEW =~ ^[a-z][a-z0-9_-]{0,30}$ ]] || die "Invalid name '$NEW'."
load_config

for u in $USERS; do [[ $u != "$NEW" ]] || die "'$NEW' already exists in config.env."; done

sed -i -E "s/^USERS=\"(.*)\"/USERS=\"\1 $NEW\"/" "$CONFIG_FILE"
grep -q "^USERS=.*\b$NEW\b" "$CONFIG_FILE" || die "Could not update USERS in $CONFIG_FILE. Edit it by hand and run step 3."
log "Added '$NEW' to $CONFIG_FILE"

NO_RESTART="${NO_RESTART:-0}" "$(dirname "$0")/03-configure-shares.sh"
