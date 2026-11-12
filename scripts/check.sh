#!/bin/sh
# Gate: runs the same checks as the PR CI (.github/workflows/ci.yml, job "check").
# Usage: scripts/check.sh [--fast] [--part check]
# The only check is the offline static-site link check, so --fast runs the same thing.
set -eu
cd "$(dirname "$0")/.."

PART="all"
while [ $# -gt 0 ]; do
  case "$1" in
    --fast) ;;
    --part) shift; PART="${1:-}" ;;
    *) echo "Usage: $0 [--fast] [--part check]" >&2; exit 2 ;;
  esac
  shift
done
case "$PART" in all|check) ;; *) echo "Unknown part: $PART" >&2; exit 2 ;; esac

trap 'rc=$?; [ "$rc" -eq 0 ] || echo "GATE: FAIL"' EXIT

python3 scripts/check_site.py

echo "GATE: PASS"
