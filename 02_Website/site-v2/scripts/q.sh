#!/bin/bash
# quick consistency on one built page: scripts/q.sh <slug-or-/> ; prints FAIL lines and the heights
S="$HOME/.claude/skills/taste-skill/scripts"
D=${DIST:-dist}; p="$D/$1/index.html"; [ "$1" = "/" ] && p="$D/index.html"; [ -f "$D/$1" ] && p="$D/$1"
out=".taste-skill/q-$(echo "$1" | tr '/' '_').txt"
node "$S/consistency.mjs" "$p" --root $D --quick --widths 1440,390 --page place --category "industrial plots" --primary "Book a site visit" --profile .taste-skill/chrome-q > "$out" 2>&1
grep -E "^\s*(FAIL|[0-9]+x[0-9]+ )|total" -A1 "$out" | grep -v "^--" | cut -c1-330
