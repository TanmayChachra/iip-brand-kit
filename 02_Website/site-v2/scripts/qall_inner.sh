#!/bin/bash
# taste gate over one page of each inner type, on the dist-inner build: scripts/qall_inner.sh
export DIST=dist-inner
for p in ${PAGES:-location faq contact plot-maps blog/how-to-choose-an-industrial-plot 404.html industrial-plots privacy blog amenities}; do
  echo "=== $p"; scripts/q.sh "$p" | grep -v "tel:\|wa.me"
done
