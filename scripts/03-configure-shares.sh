#!/usr/bin/env bash
# Step 3: create one Linux/Samba user, one folder and one Time Machine share
# per name in USERS, write the Samba and Avahi configuration, and restart both.
# Safe to run again; it rebuilds the managed block each time.
#
# Set NO_RESTART=1 to skip the restart (a restart interrupts running backups).
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root
load_config

mountpoint -q "$MOUNT_POINT" || die "$MOUNT_POINT is not mounted. Run step 2 first."

BEGIN="# BEGIN timemachine (managed by scripts/03-configure-shares.sh; do not edit)"
END="# END timemachine"

log "Creating users and folders"
for u in $USERS; do
  id -u "$u" >/dev/null 2>&1 || useradd -M -s /usr/sbin/nologin "$u"
  install -d -o "$u" -g "$u" -m 700 "$MOUNT_POINT/$u"
done

log "Building $SMB_CONF"
[[ -f "$SMB_CONF.orig" ]] || cp "$SMB_CONF" "$SMB_CONF.orig"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

# 1) drop any previous managed block, 2) drop the distro's default [homes],
# [printers] and [print$] shares (a Time Machine server doesn't need them) and any
# hand-written copy of our own shares, 3) trim trailing blank lines so reruns give identical output.
mine="|"
for u in $USERS; do mine+="$(share_name "$u")|"; done
sed '/^# BEGIN timemachine/,/^# END timemachine$/d' "$SMB_CONF" | awk -v mine="$mine" '
  /^\[/ {
    name=$0; gsub(/^\[|\].*$/, "", name)
    skip = (name=="homes" || name=="printers" || name=="print$" || index(mine, "|" name "|") > 0)
  }
  !skip { print }
' | sed -e :a -e '/^[[:space:]]*$/{$d;N;ba' -e '}' > "$tmp"

{
  echo
  echo "$BEGIN"
  echo "[global]"
  echo "   fruit:aapl = yes"
  for u in $USERS; do
    cat <<EOF

[$(share_name "$u")]
   path = $MOUNT_POINT/$u
   valid users = $u
   read only = no
   vfs objects = catia fruit streams_xattr
   fruit:time machine = yes
   fruit:metadata = stream
   fruit:model = MacSamba
   fruit:posix_rename = yes
   fruit:veto_appledouble = no
   fruit:nfs_aces = no
   fruit:wipe_intentionally_left_blank_rfork = yes
   fruit:delete_empty_adfiles = yes
   create mask = 0600
   directory mask = 0700
EOF
  done
  echo "$END"
} >> "$tmp"

testparm -s "$tmp" >/dev/null 2>&1 || { testparm -s "$tmp" 2>&1 | tail -20; die "Generated Samba config is invalid. Nothing was installed."; }
install -m 644 "$tmp" "$SMB_CONF"

log "Writing the Bonjour advertisement $AVAHI_FILE"
{
  cat <<EOF
<?xml version="1.0" standalone="no"?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">%h</name>
  <service><type>_smb._tcp</type><port>445</port></service>
  <service>
    <type>_adisk._tcp</type>
    <txt-record>sys=waMa=0,adVF=0x100</txt-record>
EOF
  i=0
  for u in $USERS; do
    echo "    <txt-record>dk${i}=adVN=$(share_name "$u"),adVF=0x82</txt-record>"
    i=$((i + 1))
  done
  cat <<EOF
  </service>
  <service><type>_device-info._tcp</type><port>0</port><txt-record>model=TimeCapsule8,119</txt-record></service>
</service-group>
EOF
} > "$AVAHI_FILE"
xmllint --noout "$AVAHI_FILE"

if [[ "${NO_RESTART:-0}" == "1" ]]; then
  warn "Skipping restart (NO_RESTART=1). Run: sudo systemctl restart smbd avahi-daemon"
else
  log "Restarting smbd and avahi-daemon (this interrupts any running backup)"
  systemctl restart smbd avahi-daemon
fi

log "Samba passwords"
for u in $USERS; do
  if pdbedit -L 2>/dev/null | grep -q "^$u:"; then
    echo "  $u: password already set (change with: sudo smbpasswd $u)"
  elif [[ -t 0 ]]; then
    echo "  $u: choose a password for this Mac's backups"
    smbpasswd -a "$u"
  else
    warn "$u has no Samba password yet. Run: sudo smbpasswd -a $u"
  fi
done

log "Done. Shares:"
for u in $USERS; do echo "  $(share_name "$u")  (user: $u)"; done
