#!/bin/bash
# one at a time over every inner page, DIST=dist-q
export DIST=dist-q
for p in ${PAGES:-faq contact neighbours blog/how-to-choose-an-industrial-plot 404.html blog location industrial-plots amenities about privacy location/industrial-plots-in-hapur location/industrial-plots-in-ghaziabad location/industrial-plots-near-delhi-meerut-expressway location/industrial-plots-in-bhojpur location/industrial-plots-in-modinagar blog/industrial-plot-buying-checklist}; do
  echo "=== $p"; scripts/q.sh "$p" | grep -v "tel:\|wa.me"
done
