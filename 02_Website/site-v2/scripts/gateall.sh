#!/bin/bash
for p in ${PAGES}; do echo "=== $p"; scripts/gate1.sh "$p"; done
