# Shipping and freight from Isapur Industrial Park (IIP): Dadri, DFC, ICDs

Research date: 2026-11-13. Research only, no website edits, nothing committed.

Origin: park centroid 28.7826 N, 77.6560 E (same as `connectivity.md`). Say "from the park", never "from the gate".

Labels: **verified** (read at the source or computed, dated), **reported** (trade press or aggregator, not checked at a primary source), **guess**.

OSRM method: public demo `router.project-osrm.org/route/v1/driving`, run 2026-11-13, free-flow speeds, no traffic. Destination pins are geocoded (Nominatim/OSM) or taken from the BIC registry, so a different pin inside the same site shifts a figure by 1 to 5 km. Minutes are free-flow only.

## 0. Corrections to what the owner believes

1. There is no "Adani Logistics Park Dadri" that I could find. Adani Logistics' container terminals on the Western DFC are in Gujarat (Tumb, Vapi, bought 2022). In the Delhi region Adani Ports publishes tariffs for **ICD Loni, Ghaziabad** (reported). Adani Ports was one of three bidders for a new 174 acre park in Greater Noida (July 2025 report, winner unverified). So "Adani at Dadri" is not proven. Do not say it.
2. The Dadri container depot is real: **CONCOR, ICD Dadri**, now branded **MMLP Dadri** in 2026 CONCOR press. It is a rail terminal, not a port.
3. "Shipping" means a container goes by truck to the Dadri terminal, by train to a seaport (JNPT, Mundra, Pipavav), then by ship. The park is not on the corridor. The nearest road-to-rail point on this route is Dadri, 46 km by road.
4. A big finding for the nearby side: **New Pilkhuwa station is 3.7 km from the park** (OSRM), but it is a passenger line station. No goods yard was found there. Do not claim it as freight.

## 1. Table

| Place | What it is | Operator | Road km from park | Free-flow hours | Source | Label | Date |
|---|---|---|---|---|---|---|---|
| ICD Dadri / MMLP Dadri (pin 28.5312 N, 77.5401 E, Tilpata Road, Dadri, Greater Noida 201311) | Rail container terminal, 105 ha, 10 lakh TEU a year capacity, 5 container freight stations (JV partners Star Track, Transworld, CMA-CGM Logistics Park, AllCargo), reefer park. Indian Railways approved private freight terminal. Handles export, import, domestic | CONCOR (Container Corporation of India) | 46.3 (via NE3 17.5, NH9 5.5, NH34 and NH334C about 10, MDR148W 4.2) | about 0.75 (45 min) | OSRM; pin https://www.bic-code.org/facility-codes/indriuifu/ ; facts https://www.maritimegateway.com/concor-engages-trade-partners-at-concor-connect-2026-dadri/ ; https://www.maritimegateway.com/concor-announces-double-stack-container-trains-from-icd-dadri-to-mundra-port-on-western-dfc/ | distance verified for that pin; terminal facts reported | 2026-11-13 |
| Dadri station area (proxy used in `connectivity.md`) | Town railway station | Indian Railways | 44.2 | 0.67 (40 min) | OSRM | verified | 2026-11-13 |
| Customs status of ICD Dadri | "Dadri, Greater Noida" is in the customs ICD list for unloading imports and loading exports (Notification 57/2003-Cus (N.T.), 25 July 2003). A Noida Customs Commissionerate office sits in the CONCOR building on Tilpata Road and its Commissioner attended CONCOR Connect on 29 July 2026 | Customs, Noida Commissionerate | same site | n/a | https://taxmanagementindia.com/visitor/detail_notification.asp?ID=2198 (via search summary, page itself not read, it redirects) ; maritimegateway link above | reported (not read at gazette; no later amendment found) | 2026-11-13 |
| Greater Noida MMLP, Sector Kappa-II, next to ICD Dadri | 174 acre new multimodal logistics park, tender stage, 3 bidders including Adani Ports, winner not verified | Greater Noida Authority (tender) | about 46 (same area as ICD Dadri) | n/a | https://indiaseatradenews.com/adani-ports-among-3-cos-vying-for-land-to-build-logistics-park/ (headline only readable) ; https://knnindia.co.in/news/newsdetails/state/uttar-pradesh/greater-noida-to-develop-174-acre-multi-modal-logistics-park-in-dadri-integrating-air-rail-road-cargo | reported, not built | 2026-11-13 |
| NICDC Multi Modal Logistics Hub, Dadri | 825 to 849 acre hub, "near intersection of Eastern and Western DFC", New Dadri DFC junction listed 5 km away, PPP, under "nearing completion". DFCCIL building its external rail link | NICDC (state of delivery unclear) | about 46 (Dadri area) | n/a | https://nicdc.in/projects/4-projects-nearing-completion/multi-modal-logistics-and-transport-hub-dadri-greater-noida-up (updated 2025-08-05) | reported (area figures inconsistent on the page) | 2026-11-13 |
| Dadri DFC junction (Western meets Eastern branch) | WDFC northern end. Eastern DFC branch Dadri to Khurja, 46 km, reported opened Oct 2022 | DFCCIL | about 46 (Dadri area, exact pin not found) | n/a | https://en.wikipedia.org/wiki/Western_Dedicated_Freight_Corridor ; https://www.wikiwand.com/en/Eastern_Dedicated_Freight_Corridor | reported | 2026-11-13 |
| ICD Loni, Ghaziabad (Banthala, near Noli station) | Customs notified ICD (added to list by Notification 11/2007-Cus (N.T.), ICEGATE code INLON6), 27.5 acre bonded area. Operator unclear: older source says Worlds Window Infrastructure with CWC, Adani Ports publishes Loni tariffs | CWC or Adani Logistics (unverified) | 53.9 (to Noli station pin, proxy) | 0.77 (46 min) | OSRM; https://www.seair.co.in/custom-notifications/notification-no-112007-dated-15-feb-2007-64236.aspx ; https://www.adaniports.com/-/media/Project/Ports/Logistics/tariff/Loni/Public-Tariff-for-Terminal-Charges_ICD-Loni.pdf | distance verified for proxy pin; status reported | 2026-11-13 |
| ICD Tughlakabad, Delhi (station pin 28.5025 N, 77.2994 E) | CONCOR ICD, Delhi to Kolkata assured-transit pilot train (since 1 Oct 2025, 120 hours guaranteed, Wed and Sat) per press | CONCOR | 64.1 | 0.85 (51 min) | OSRM; https://indianinfrastructure.com/?p=254383 | distance verified for proxy pin; service reported | 2026-11-13 |
| Garhi Harsaru, Gurugram (station pin) | CONCOR ICD area | CONCOR | 96.0 | 1.4 (83 min) | OSRM | distance verified for proxy pin; ICD status not checked | 2026-11-13 |
| Dasna (station, NH9) | Road junction area, not a container depot. No ICD found | n/a | 22.2 | 0.3 (19 min) | OSRM | verified for pin | 2026-11-13 |
| Hapur Junction station | Passenger and mainline station. No goods or container depot found | Indian Railways | 15.0 | 0.3 (18 min) | OSRM | verified distance; no freight facility found | 2026-11-13 |
| New Pilkhuwa station | Passenger station on Hapur-Ghaziabad line. No goods yard found | Indian Railways | 3.7 | 0.1 (6 min) | OSRM | verified distance; no freight use found | 2026-11-13 |
| Meerut Cantt station | Mainline station. No container depot found | Indian Railways | 36.7 | 0.55 (33 min) | OSRM | verified distance | 2026-11-13 |
| Ghaziabad Junction station | Mainline station | Indian Railways | 33.5 | 0.5 (30 min) | OSRM (also in `connectivity.md`) | verified | 2026-11-13 |
| Khurja Junction station | Eastern DFC branch town, no container depot found | Indian Railways | 77.1 | 1.1 (67 min) | OSRM | verified distance | 2026-11-13 |
| Moradabad Junction station | Mainline station, no depot found | Indian Railways | 119.1 | 1.65 (99 min) | OSRM | verified distance | 2026-11-13 |
| Panipat Junction station | Mainline station, ICD not checked | Indian Railways | 125.0 | 1.5 (88 min) | OSRM | verified distance | 2026-11-13 |
| Noida International Airport, Jewar (cargo) | Commercial flights from 15 June 2026. First cargo flight 17 June 2026 (domestic freighter, AISATS hub). International cargo expected within about six months, not confirmed | NIAL, AISATS | 101.4 (`connectivity.md`) | 1.4 | https://www.newkerala.com/news/a/cargo-operations-commence-noida-international-airport-inaugural-flight-239.htm ; https://www.businesstoday.in/amp/india/story/inaugural-flight-from-lucknow-lands-at-jewar-airport-indigo-kickstarts-ops-akasa-air-to-begin-soon-536804-2026-06-15 | reported | 2026-11-13 |
| Hindon Airport, Ghaziabad | Small airport, no cargo role found | AAI | 42.7 (`connectivity.md`) | 0.65 | OSRM | verified distance only | 2026-11-13 |

Route note (OSRM, ICD Dadri): the free-flow route is the Delhi-Meerut Expressway (NE3) about 17.5 km, NH9, then NH34 and NH334C into Greater Noida. Real time is longer with trucks and traffic. A loaded truck is limited to about 60 to 70 km/h in practice (guess): plan 1.5 to 2 hours, not 45 minutes.

## 2. Freight corridors and transit times (status 2026-11-13)

| Fact | Source | Label |
|---|---|---|
| Western DFC: Dadri (UP) to JNPT, 1,506 km. DFCCIL declared it complete 31 March 2026. Final three sections (about 326 route km, over 20,700 crore rupees) dedicated by the PM, reported 9 Sep 2026 | https://en.wikipedia.org/wiki/Western_Dedicated_Freight_Corridor ; https://cargoconnect.co.in/railways/pm-modi-flags-off-freight-trains-as-indias-2843-km-dedicated-freight-corridor-network-goes-fully-operational | reported |
| Eastern DFC: Ludhiana to Sonnagar, 1,337 km, reported fully operational. The Dadri to Khurja branch (46 km) reported open Oct 2022, Ludhiana to Khurja (365 km) reported Aug 2023. One undated trade item says the Ludhiana to Khurja to Dadri single-track segment still needed a year, contradicting this. Dadri is where the Western DFC and the Eastern DFC branch meet | https://en.wikipedia.org/wiki/Eastern_Dedicated_Freight_Corridor ; https://www.wikiwand.com/en/Eastern_Dedicated_Freight_Corridor | reported, conflicting. Check DFCCIL |
| Both corridors together: about 443 freight trains a day on average | cargoconnect link above | reported |
| Dadri to Mundra by double-stack train, 1,158 km, under 30 hours (earlier average about 70 hours). Flagged off 20 April 2023 | https://www.maritimegateway.com/concor-announces-double-stack-container-trains-from-icd-dadri-to-mundra-port-on-western-dfc/ | reported (CONCOR announcement) |
| Dadri to JNPT: DFCCIL says freight time fell from about 66 to about 58 hours. A different 26 May 2026 trade article says about 72 hours cut by half to about 36 hours, no source. The two conflict | cargoconnect link above ; https://www.cargoconnect.co.in/railways/dadrijnpa-corridor-redefines-freight-movement-cuts-transit-time-by-50 | reported, conflicting. Use none on the site |
| First double-stack train Dadri to JNPT flagged off 29 June 2026, up to 180 TEU a train (a competing report says 360 TEU, conflict). Daily service reported | https://indiashippingnews.com/ports/concor-operates-first-double-stack-container-train-from-mmlp-dadri-to-jnpt-boosting-indias-exim-logistics/ | reported |
| Dadri to Pipavav: planned long-haul and double-stack service, no transit time found | maritimegateway Apr 2023 link above | reported plan |
| Dadri to Kolkata or Haldia: no Dadri service or transit time found. The only Kolkata item is Tughlakabad to Kolkata, 120 hour guaranteed, since 1 Oct 2025 | https://indianinfrastructure.com/?p=254383 | reported |
| No DFC siding, interchange or terminal at Ghaziabad, Hapur or Modinagar found. Only contact with the DFC from the park is a road haul to Dadri | search 2026-11-13, absence of evidence | gap |
| E-way bill and GST check posts: e-way bill is an online system with no required physical point; I found no park-specific facility | not researched in depth | gap |
| Truck terminals, trucker rest facilities, nearest customs office other than Noida Customs at Dadri and ICD Loni: not verified | n/a | gap |

## 3. How a container from the park reaches a port by rail from Dadri (plain language)

1. The factory packs the goods into a container at the park, or a truck carries loose cargo to a container freight station inside the Dadri terminal, where it is packed.
2. A truck hauls the container about 46 km to ICD Dadri (CONCOR, Dadri, Greater Noida). The route is the Delhi-Meerut Expressway, then NH9, then local highway. Plan about 1.5 to 2 hours loaded.
3. At the terminal, customs checks and seals the export container (Customs has an office there). Shipping lines and agents work in the terminal.
4. The container is loaded onto a train. Trains run on the Western Dedicated Freight Corridor, a separate railway built only for goods, from Dadri to JNPT (Nhava Sheva, Mumbai). Some trains carry containers stacked two high (double-stack). Dadri to Mundra is reported under 30 hours. Dadri to JNPT is reported at about 58 hours, with other reports disagreeing.
5. At the port, the container is moved to the ship. Imports run the same way in reverse: ship, train to Dadri, truck to the park.

Short version: truck to Dadri, train to the port, ship overseas. The park gets none of this by itself. It is a truck trip at each end.

## 4. Road links from the park to Dadri

- Route: park to Bhojpur access (4.2 km, MDR148W), Delhi-Meerut Expressway (17.5 km), NH9 (5.5 km), NH34 and NH334C, then the Tilpata Road side of Dadri. Total 46.3 km to the ICD pin, 44.2 km to Dadri station. Label: verified for the pins, 2026-11-13, free-flow. OSRM names the expressway NE3.
- Alternative via the Eastern Peripheral Expressway (Kallu Garhi about 17.8 km) was not routed by OSRM as the fastest. Not claimed.
- Hours: 45 minutes free-flow, 1.5 to 2 hours loaded truck (guess).

## 5. Things a shipper cares about, and what can honestly be said

- Nearest container depot with customs: ICD Dadri, 46 km. Next nearest listed here: ICD Loni about 54 km (proxy pin), Tughlakabad about 64 km (proxy pin).
- No dry port, goods yard or container depot found closer than Dadri or Loni. Hapur, Modinagar, Meerut, Dasna have none confirmed.
- Jewar air cargo: 101 km, started June 2026, domestic first. Low value for the park.
- Not verified: e-way bill facility, truck terminal, nearest customs clearing point for road cargo, any Eastern DFC to Kolkata or Haldia container service from Dadri.

## 6. What can be said and what cannot

Safe (a measured driving distance, its source, "from the park", "by road", free-flow, no traffic):
- ICD Dadri, a CONCOR container terminal, is about 46 km by road.
- The Delhi-Meerut Expressway entry is about 4 km by road.

Safe only with a cited, named source and the word "reported" in the docs, not as the headline: Customs is present at the Dadri terminal, container trains run from Dadri to JNPT and Mundra.

Do not say:
- "On the freight corridor", "connected to the DFC", "next to the DFC", "rail connected".
- "Adani Logistics Park at Dadri".
- "Shipping to ports from our door" or "port connectivity" as if the park has it.
- Any transit time in hours to a port. The sources conflict (66 to 58 hours, or about 36 hours, or about 72 hours). Pick none until DFCCIL or CONCOR publishes a timetable.
- "Jewar cargo hub nearby."
- Any transit time or service to Kolkata or Haldia from Dadri.
- Schema markup for any of these claims.

## 7. Five safe website lines (owner's voice)

1. "About 46 km by road to ICD Dadri, the CONCOR container terminal." Source: OSRM 2026-11-13 plus https://www.bic-code.org/facility-codes/indriuifu/ . Verified distance, terminal reported. Footnote: "By road from the park, clear road, traffic not included."
2. "Your container goes by truck to Dadri and by train from there to the ports." Source: https://www.maritimegateway.com/concor-announces-double-stack-container-trains-from-icd-dadri-to-mundra-port-on-western-dfc/ , reported. Say only if the owner accepts a "reported" label on a how-it-works line.
3. "Delhi-Meerut Expressway about 4 km from the park, and Dadri about 46 km on it." Source: OSRM 2026-11-13, verified.
4. "Customs and container freight stations sit inside the Dadri terminal." Source: https://www.maritimegateway.com/concor-engages-trade-partners-at-concor-connect-2026-dadri/ (29 July 2026), reported.
5. "Hapur 15 km, Ghaziabad 34 km, Dadri 46 km, all by road from the park." Source: OSRM 2026-11-13, verified (pins noted in `connectivity.md`).

## 8. Still unverified

- Exact ICD Dadri and New Dadri DFC pins (BIC pin is a registry value, not a surveyed gate).
- Current customs status read from the gazette (2003 notice reported; a newer ICEGATE port code for Dadri not checked).
- Dadri to JNPT transit hours (conflicting sources). Dadri to Pipavav, Kolkata, Haldia: nothing found.
- Whether the Dadri to Khurja to Ludhiana Eastern DFC link is carrying trains in 2026 (conflicting).
- ICD Loni operator and status in 2026.
- Whether anyone else has a private depot near Dadri beyond the CONCOR JV partners.
- E-way bill, truck terminal and trucker facility points near the park.
