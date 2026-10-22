#!/usr/bin/env bash
# Measures raw sequential speed of the drive (not the network). Uses 2 GB of temporary space.
# Usage: sudo ./scripts/benchmark.sh
set -euo pipefail
source "$(dirname "$0")/lib.sh"
need_root
load_config

F="$MOUNT_POINT/.benchmark.tmp"
trap 'rm -f "$F"' EXIT

log "Write test (2 GB, direct I/O)"
dd if=/dev/zero of="$F" bs=1M count=2048 oflag=direct 2>&1 | tail -1
sync
echo 3 > /proc/sys/vm/drop_caches
log "Read test (2 GB, direct I/O)"
dd if="$F" of=/dev/null bs=1M iflag=direct 2>&1 | tail -1
log "For network speed, run 'iperf3 -s' on the Pi and 'iperf3 -c <pi-address>' on a Mac."
