#!/usr/bin/env bash
# Shared helpers, sourced by the other scripts. Not meant to be run directly.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${CONFIG_FILE:-$REPO_ROOT/config.env}"

log()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!!\033[0m  %s\n' "$*" >&2; }
die()  { printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2; exit 1; }

need_root() {
  [[ $EUID -eq 0 ]] || die "Run this script with sudo."
}

# Reads config.env and checks the values we depend on.
load_config() {
  [[ -f "$CONFIG_FILE" ]] || die "Missing $CONFIG_FILE. Copy config.env.example to config.env and edit it."
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
  : "${DISK:?DISK is not set in config.env}"
  : "${LABEL:=TimeMachine}"
  : "${MOUNT_POINT:=/srv/timemachine}"
  : "${USERS:?USERS is not set in config.env}"
  : "${SMART_DEVICE_TYPE:=sat}"
  local u
  for u in $USERS; do
    [[ $u =~ ^[a-z][a-z0-9_-]{0,30}$ ]] || die "Invalid user name '$u'. Use lowercase letters, digits, '-' or '_', starting with a letter."
  done
}

# The Samba share name for a user, e.g. alice -> TimeMachine-Alice
share_name() { printf 'TimeMachine-%s' "${1^}"; }

SMB_CONF="${SMB_CONF:-/etc/samba/smb.conf}"
AVAHI_FILE="${AVAHI_FILE:-/etc/avahi/services/timemachine.service}"
