# Connectivity fact-check for Isapur Industrial Park (IIP)

Research date: 2026-11-13. Research only, no website edits.

Origin: centroid of the Phase 1 to 3 plots, 28.7826 N, 77.6560 E (`01_Brand/Plot-Maps/data/phase-boundaries.geojson`). The gate position is not known, so every distance is from this centroid. Say "from the park" on the site, never "from the gate".

Labels: verified (computed or read at the source, dated), reported (third party, not checked at a primary source), guess.

## 1. Driving distances (OSRM)

Method: public OSRM demo server, `router.project-osrm.org/route/v1/driving`, free, run 2026-11-13. Label: **verified (computed)**. Traffic is NOT included, the demo server uses free-flow speeds, so real minutes at peak hours will be longer. Destination points are my own approximations of each place (centre or station, geocoded with Nominatim/OSM on 2026-11-13); another pin inside the same town shifts a figure by 1 to 3 km. Distances already on V3-HOME (4.7 / 11.4 / 13.4 km, Bhojpur exit about 4.3 km) were not changed; the figures here agree within pin differences.

| Place | Driving km | Minutes (no traffic) | Source | Label |
|---|---|---|---|---|
| Delhi-Meerut Expressway (NE3) entry, via MDR148W, at Bhojpur | 4.2 | about 5 (guess from speed, route to Bhojpur town is 22.8 km / 18 min with 8.6 km on the expressway) | OSRM, step list shows 4.2 km on MDR148W then the "Delhi - Meerut Expressway NE3" | verified, 2026-11-13 |
| Bhojpur town (on the expressway) | 22.8 | 18 | OSRM (route goes via the expressway) | verified |
| Modinagar centre | 10.7 | 14 | OSRM | verified |
| Modinagar North station | 11.3 | 13 | OSRM | verified |
| Muradnagar | 21.4 | 24 | OSRM | verified |
| Hapur centre | 13.6 | 15 | OSRM | verified |
| Hapur Junction station | 15.0 | 18 | OSRM | verified |
| Meerut centre (Ghanta Ghar area) | 29.9 | 29 | OSRM, via expressway then NH34/NH334 | verified |
| Meerut City Junction station | 31.4 | 29 | OSRM | verified |
| Ghaziabad Junction station (city) | 33.5 | 30 | OSRM, via expressway then NH9 | verified |
| Anand Vihar Terminal, Delhi | 46.0 | 40 | OSRM, via expressway and NH24 | verified |
| India Gate, Delhi | 54.9 | 42 | OSRM | verified |
| Noida Sector 18 | 47.9 | 38 | OSRM | verified |
| Hindon Airport (Ghaziabad) | 42.7 | 39 | OSRM | verified |
| Dadri town (Dadri station area, proxy for the WDFC start and Dadri ICD, see note) | 44.2 | 40 | OSRM | verified for the pin, proxy for the terminal |
| Noida International Airport, Jewar | 101.4 | 83 | OSRM, via EPE then Yamuna Expressway | verified |
| DME and EPE junction (Kallu Garhi area, OSRM enters EPE here) | about 17.8 | about 15 | OSRM step list (4.2 + 13.6 km) | verified |
| Dasna, NH9 (EPE and expressway area) | 22.2 | 19 | OSRM | verified |
| Duhai, NH34 (EPE area) | 25.2 | 20 | OSRM | verified |
| EPE north end, Kundli | 74.8 | 56 | OSRM, 10.4 km of the route stays on EPE after the Kallu Garhi entry, then Haryana roads (OSRM names EPE as "NE-2") | verified (distance), the road mix is reported by OSRM only |
| EPE south end, Palwal (Dholagarh area approx) | 103.8 | 71 | OSRM, 75.1 km on EPE then NH334D, NH71B | verified for an approximate pin |

Notes and gaps:
- Dadri ICD and the WDFC terminal: I could not geocode the ICD (CONCOR lists it near Tilapatta village, Dadri, Greater Noida). The Dadri row uses Dadri station area. The true ICD or new Dadri DFC station pin could be 3 to 8 km different. Re-run with the exact pin before any number goes live. Until then the site should say "about 45 km" only if worded as "to Dadri".
- Nearest railway goods or freight station: not determined. No source found for a goods yard at Hapur, Modinagar or Muradnagar. Do not put one on the site. Label: open gap.
- Owner guesses checked: expressway "under 5 km" holds (4.2 km to the entry, verified). Dadri "about 50 km" is a little high, OSRM says about 44 km to Dadri town. Delhi "about 55 km" holds for India Gate (54.9 km) and is about 46 km to Anand Vihar.
- Air distances were not computed. The site rule says say straight-line or driving, so use only these driving numbers.

## 2. Web facts

| Fact | Source and date | Label |
|---|---|---|
| Delhi-Meerut Expressway (NE3): Wikipedia gives 96 km (Nizamuddin to Partapur near Meerut), 6 lanes on the Dasna to Meerut greenfield section, 8 lanes Dasna to Hapur, up to 14 lanes in Delhi to Dasna section. Opened in stages 2018 to 1 April 2021. | https://en.wikipedia.org/wiki/Delhi%E2%80%93Meerut_Expressway , read 2026-11-13 | reported |
| The length is disputed in sources (82 km vs 96 km, depends what is counted). Do not quote a length on the site. | Search 2026-11-13, e.g. https://themetrorailguy.com/nhai-delhi-meerut-expressway-information-route-status/ | reported |
| A Bhojpur access point exists on the expressway (listed among entry/exit points, and a toll plaza at Bhojpur on the Dasna to Meerut section, 2019 source). | https://themetrorailguy.com/nhai-delhi-meerut-expressway-information-route-status/ ; OSRM route confirms the park to Bhojpur path uses the expressway | reported; the 4.2 km figure is verified as a driven path |
| No Modinagar exit on the expressway was found. Do not say "Modinagar exit". | search 2026-11-13 | gap |
| Eastern Peripheral Expressway (EPE, also KMP): 135 km, Kundli (NH44) to Dholagarh, Palwal (NH44), inaugurated 27 May 2018. Interchanges listed: NH709B Baghpat, NH34 Duhai, NE3 Kallu Garhi, NH9 Dasna, NH34/NH334C Kot, NH334D Sihol. It crosses the Delhi-Meerut Expressway. | https://en.wikipedia.org/wiki/Eastern_Peripheral_Expressway , read 2026-11-13 | reported (no NHAI list found, other sites disagree on names) |
| Nearest EPE junction for IIP: the Kallu Garhi junction of NE3 with EPE, about 17.8 km driving (OSRM path). Dasna on NH9 is the next one, 22.2 km. | OSRM, 2026-11-13 | verified (distance), junction names reported |
| Western DFC: Dadri (UP) to JNPT (Navi Mumbai), about 1,506 km. Dadri to Rewari section (127 km) operational since 2023. Final sections dedicated 8 Sep 2026 per trade press, completing the full Dadri to JNPT route. | https://en.wikipedia.org/wiki/Western_Dedicated_Freight_Corridor ; https://www.maritimegateway.com/pm-modi-dedicates-final-western-dedicated-freight-corridor-sections-completing-full-jnpt-dadri-route/ ; JICA https://www.jica.go.jp/english/overseas/india/information/press/2026/1585189_70871.html (2026) | reported (no PIB release for 2026 found) |
| Dadri is the WDFC end point, close to where the Western and Eastern DFCs meet (Khurja to Dadri branch, 46 km per Wikipedia). CONCOR runs the Dadri ICD (near Tilapatta, Dadri, Greater Noida), double-stack trains from the ICD to Mundra port since April 2023, and a new multimodal logistics park at Dadri (105 ha, connected to both DFCs). | https://www.maritimegateway.com/concor-announces-double-stack-container-trains-from-icd-dadri-to-mundra-port-on-western-dfc/ ; https://www.jnport.gov.in/page/inland-container-depot/RnZtOXM1a1RYaytXOGdkQVRTcEY5UT09 | reported |
| No WDFC interchange, siding or terminal near Ghaziabad or Hapur was found. The only WDFC contact for IIP is Dadri, by road. Do not say "on the freight corridor" or "next to the DFC". | Wikipedia and search 2026-11-13 | gap (absence of evidence) |
| Ganga Expressway: 594 km, Meerut (Bijauli, Kharkhauda) to Prayagraj, inaugurated 29 April 2026, passes Hapur district; Wikipedia lists a connection to the Delhi-Meerut Expressway. | https://en.wikipedia.org/wiki/Ganga_Expressway ; https://newsonair.gov.in/pm-modi-inaugurates-594-km-long-ganga-expressway-connecting-meerut-to-prayagraj/ (29 Apr 2026, state broadcaster) | reported (All India Radio is government, but the connection detail is Wikipedia only) |
| Namo Bharat (Delhi-Ghaziabad-Meerut RRTS): 82 km, full corridor opened 22 Feb 2026, 55 minutes end to end, stations include Duhai, Muradnagar, Modinagar South and North. It carries passengers, so only relevant for workers, not goods. | https://www.freepressjournal.in/amp/india/pm-modi-launches-meerut-metro-dedicates-full-delhimeerut-namo-bharat-corridor-video (Feb 2026); https://indianinfrastructure.com/?p=266185 | reported |
| Cluster news: GDA board approved a 251 ha industrial township and multimodal logistics park at Modinagar (Sep 2025, aggregator report); about 100 ha taken for a UPSIDA hub at Niwari, Modinagar area; a proposed Hapur corridor (Atola, Sikheda, Sadarpur, Pooth) is from aggregator news. | https://swarajyamag.com/amp/story/news-brief/world-class-industrial-township-multi-modal-logistics-hub-to-come-up-in-uttar-pradeshs-modinagar ; https://www.ghar.tv/blog/article_ghaziabad-industrial-hub-gains-100-hectares-as-state-secures-land_6886.html | reported, not for the site |

### Safe for the website, and not safe

Safe (verified, state as "by road from the park", not from the gate, no traffic):
- 4.2 km to the Delhi-Meerut Expressway entry (say "about 4 km by road"; this agrees with the existing 4.3 and 4.7 figures, pick one number and one pin sitewide).
- Modinagar about 11 km, Hapur about 14 km, Muradnagar about 21 km, Meerut about 30 km, Ghaziabad about 34 km, Delhi (Anand Vihar about 46 km, India Gate about 55 km), Noida about 48 km, Hindon Airport about 43 km, Dadri about 44 km to Dadri town.
- The EPE meeting point at Kallu Garhi about 18 km by road, worded as "reach the Eastern Peripheral Expressway in about 18 km".
- Noida International Airport (Jewar) about 100 km: true, but low value, say it only as a distance, never as "near".

Not safe (no proof, or only reported):
- Any length, lane count or date of the expressways, EPE, Ganga Expressway or the DFC (reported only; if wanted, cite the official NHAI or PIB page first).
- "On" or "next to" the freight corridor, any DFC interchange near the park, or a goods station near the park.
- Travel times promised as a fact. Show them only as "free-flow minutes, traffic not included".
- Hapur and Modinagar cluster plans (proposals, aggregator sources).
- Any schema markup for these claims.

## 3. Five strongest selling points, ranked for a factory owner

1. **Expressway in about 4 km.** Delhi-Meerut Expressway entry (4.2 km) turns Delhi, Noida and Meerut into a one-road trip, no town traffic (Modinagar is bypassed). Fully verified, the strongest claim.
2. **Reach to the Delhi region markets.** Anand Vihar about 46 km, Ghaziabad about 34 km, Noida about 48 km. A factory owner cares about next-day delivery to the big buyers.
3. **Eastern Peripheral Expressway in about 18 km.** Lets trucks avoid Delhi entirely and reach Kundli (about 75 km) and Palwal (about 104 km), the Haryana industrial belts, and the Yamuna Expressway towards Jewar. Strong for trucking, but name the junction only as "Kallu Garhi, reported".
4. **Dadri freight terminal about 44 km (to Dadri town).** WDFC and Dadri ICD for container movement to Mumbai and Mundra ports. Real and valuable for exporters, but it is a road haul to the terminal, never "access to the corridor". Needs the exact ICD pin before use.
5. **Labour and market towns close by.** Modinagar about 11 km, Hapur about 14 km, Muradnagar about 21 km, plus the Namo Bharat stops at Modinagar and Muradnagar for staff (reported). Labour supply is an unsourced claim, so state only the distances, not "labour availability".

Airport (Hindon about 43 km, Jewar about 100 km) ranks last: cargo owners barely care and Jewar is far.

## 4. Three UX ideas (plain words, no final design)

1. **Zoomed-out map with lanes.** The page already has a zoomed-out map. Zoom out one more level and draw three road lines out of the park: the expressway to Delhi, the EPE ring, and a dashed line to Dadri. Each line ends at a labelled place with its kilometres. Tapping a line shows the route and the "traffic not included" note.
2. **Distance ladder.** A simple vertical list, nearest at the top: expressway 4 km, Modinagar 11, Hapur 14, EPE 18, Meerut 30, Ghaziabad 34, Anand Vihar 46, Delhi 55. A bar grows beside each number as you scroll. One row can highlight "your buyers" if the owner picks a city.
3. **"Trucks leave at dawn" story.** In the scroll scene where the roller shutter lifts and trucks leave, add three captions as the truck moves: "On the expressway in 5 minutes", "Anand Vihar in about 40 minutes with a clear road", "Dadri terminal in about 40 minutes". Keep the words "clear road, traffic not included" visible so it stays honest.
