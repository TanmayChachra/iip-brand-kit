#!/bin/bash
# gate one built page in its own project folder (own waivers, own rounds): scripts/gate1.sh <slug>   (home: /)
S="$HOME/.claude/skills/taste-skill/scripts/gate.mjs"
ROOT="$(pwd)"; slug="$1"; name="$(echo "$slug" | tr '/.' '__')"; [ "$slug" = "/" ] && name=home
page="$ROOT/dist/$slug/index.html"; [ "$slug" = "/" ] && page="$ROOT/dist/index.html"; [ -f "$ROOT/dist/$slug" ] && page="$ROOT/dist/$slug"
mkdir -p "gates/$name/.taste-skill"; cd "gates/$name"
[ -f .taste-skill/waivers.json ] || cp "$ROOT/scripts/waivers.default.json" .taste-skill/waivers.json
[ -f .taste-skill/build.json ] || [ -f .taste-skill/gate.json ] || node "$S" --start "$page" --root "$ROOT/dist" --kind place --category "industrial plots" --primary "Book a site visit" --profile .taste-skill > /dev/null 2>&1
node "$S" "$page" --root "$ROOT/dist" --profile .taste-skill > result.txt 2>&1
grep -E "FAIL|GATE|WAIVED" -A2 result.txt | cut -c1-320
