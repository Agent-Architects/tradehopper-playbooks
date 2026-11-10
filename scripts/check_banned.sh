#!/usr/bin/env bash
# Fails if the repo contains social-post links, personal machine paths, internal tool names,
# em or en dashes, or emoji. Run from the repo root.
set -uo pipefail
export LC_ALL=C.UTF-8

status=0
check() {
  local label="$1" pattern="$2" rc
  git grep -nIP "$pattern" -- . ':!scripts/check_banned.sh'
  rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "FAIL: $label"
    status=1
  elif [ "$rc" -ne 1 ]; then
    echo "ERROR: grep failed for $label"
    status=1
  fi
}

check "social post links" '(instagram\.com|tiktok\.com|twitter\.com|x\.com/[^ ]*/status|youtube\.com/watch|youtu\.be/)'
check "personal paths" '(/Users/[a-z]|/home/[a-z]+/|~/Projects|~/\.claude/projects)'
check "internal tool names" '(?i)cortext'
check "em or en dashes" '[\x{2013}\x{2014}]'
check "emoji" '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]'

[ "$status" -eq 0 ] && echo "banned-terms check: OK"
exit "$status"
