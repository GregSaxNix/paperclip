#!/usr/bin/env bash
# Sync the master GREG.md to all agent instruction directories.
# Run this after editing C:\Users\Administrator\.paperclip\instances\default\GREG.md
#
# Usage: bash scripts/sync-greg-md.sh

set -euo pipefail

INSTANCE_ROOT="$HOME/.paperclip/instances/default"
MASTER="$INSTANCE_ROOT/GREG.md"

if [ ! -f "$MASTER" ]; then
  echo "ERROR: Master GREG.md not found at $MASTER"
  exit 1
fi

# Life Admin company only (Shine merged and archived 2026-04-06)
LIFE_ADMIN_ID="505ab906-66b5-4400-b131-96b8aee91c5d"

COUNT=0
for AGENT_DIR in "$INSTANCE_ROOT/companies/$LIFE_ADMIN_ID/agents"/*/; do
  INSTR_DIR="$AGENT_DIR/instructions"
  if [ -d "$INSTR_DIR" ]; then
    cp "$MASTER" "$INSTR_DIR/GREG.md"
    COUNT=$((COUNT + 1))
  fi
done

echo "Synced GREG.md to $COUNT agent instruction directories (Life Admin only)."
