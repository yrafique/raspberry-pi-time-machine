#!/usr/bin/env bash
# Runs steps 1 to 4 and the verification in order. Step 2 erases the disk (it asks first).
# Usage: sudo ./scripts/setup-all.sh
set -euo pipefail
cd "$(dirname "$0")"

./01-install-packages.sh
./02-prepare-drive.sh
./03-configure-shares.sh
./04-harden.sh
./verify.sh
