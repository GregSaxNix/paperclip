#!/usr/bin/env bash
# Update Paperclip from upstream (paperclipai/paperclip)
# Usage: bash scripts/update-from-upstream.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

echo "=== Paperclip Upstream Update ==="
echo ""

# 1. Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[1/6] Stashing uncommitted changes..."
  git stash push -m "auto-stash before upstream update $(date +%Y-%m-%d_%H%M%S)"
  STASHED=true
else
  echo "[1/6] Working tree clean — no stash needed."
  STASHED=false
fi

# 2. Fetch upstream
echo "[2/6] Fetching upstream/master..."
git fetch upstream

# 3. Check if there are new commits
LOCAL_HEAD=$(git rev-parse HEAD)
UPSTREAM_HEAD=$(git rev-parse upstream/master)
MERGE_BASE=$(git merge-base HEAD upstream/master)

if [ "$LOCAL_HEAD" = "$UPSTREAM_HEAD" ]; then
  echo "[3/6] Already up to date with upstream."
  if [ "$STASHED" = true ]; then
    echo "Restoring stashed changes..."
    git stash pop
  fi
  echo ""
  echo "=== No updates available ==="
  exit 0
fi

# Show what's new
echo "[3/6] New commits from upstream:"
echo ""
git log --oneline "$MERGE_BASE".."$UPSTREAM_HEAD" | head -20
echo ""

# 4. Merge upstream
echo "[4/6] Merging upstream/master..."
if ! git merge upstream/master --no-edit; then
  echo ""
  echo "!!! MERGE CONFLICT detected !!!"
  echo "Aborting merge — please resolve conflicts manually."
  git merge --abort
  if [ "$STASHED" = true ]; then
    echo "Restoring stashed changes..."
    git stash pop
  fi
  exit 1
fi

# 5. Install dependencies (in case they changed)
echo "[5/6] Running pnpm install..."
pnpm install --frozen-lockfile 2>/dev/null || pnpm install

# 6. Check for new version tags
echo "[6/6] Checking for new version tags..."
LATEST_TAG=$(git tag --sort=-v:refname | head -1)
if [ -n "$LATEST_TAG" ]; then
  TAG_COMMIT=$(git rev-list -n 1 "$LATEST_TAG" 2>/dev/null || echo "")
  if [ -n "$TAG_COMMIT" ]; then
    IS_NEW=$(git log --oneline "$MERGE_BASE".."$UPSTREAM_HEAD" | grep -c "$TAG_COMMIT" || true)
    if [ "$IS_NEW" -gt 0 ]; then
      echo ""
      echo "*** New release: $LATEST_TAG ***"
      echo ""
      git tag -l -n1 "$LATEST_TAG"
    fi
  fi
fi

# Restore stash if needed
if [ "$STASHED" = true ]; then
  echo ""
  echo "Restoring stashed changes..."
  git stash pop
fi

echo ""
echo "=== Update complete ==="
echo "Restart the dev server to pick up changes (migrations run automatically)."
echo "  pnpm dev"
