// Stand-in photographs (Unsplash licence, expressway: Wikimedia CC BY-SA 4.0; see public/img/photo/credits.json) and the OSM route map.
export const ALT = {
  'sheds-blue': 'Blue-roofed industrial sheds along a concrete road',
  'street-light': 'Street lights along a wide road',
  'verge-palms': 'Road edge lined with planted palm and trees',
  'expressway-a': 'Delhi-Meerut Expressway at Ghaziabad, lanes and street lights',
  'factory-yard': 'Industrial yard with sheds and a paved lane',
  'shed-dusk': 'Industrial shed at dusk',
  'sheds-aerial': 'Aerial view of industrial sheds',
  'road-green': 'Fresh black-top road between green slopes',
  'expressway-b': 'Multi-lane expressway with a service road in Ghaziabad',
  'road-india': 'Tree-lined city road with traffic under a blue sky',
  'jcb-lowbed': 'Excavator on a low-bed truck beside an open road and sheds',
};
export const POOL = ['factory-yard', 'verge-palms', 'sheds-blue', 'road-green', 'expressway-b', 'jcb-lowbed'];
const SIZES = '(min-width: 1024px) 588px, (min-width: 640px) 720px, 342px';
export const photoFig = (k, cls = '', moment = false) => `<figure class="pl-photo span-6 ${cls}"${moment ? ' data-moment="picture-develops"' : ''}><img src="/img/photo/${k}-43-800.webp" srcset="/img/photo/${k}-43-600.webp 600w, /img/photo/${k}-43-800.webp 800w, /img/photo/${k}-43-1350.webp 1350w" sizes="${SIZES}" width="1350" height="1013" alt="${ALT[k]}" loading="lazy" data-source="stand-in" data-subject="site and road"></figure>`;
export const mapFig = (cls = '') => `<figure class="pl-photo span-6 ${cls}"><a href="/location/"><img src="/img/map/map-park-sm.webp" srcset="/img/map/map-park-sm.webp 800w, /img/map/map-park.webp 1800w" sizes="${SIZES}" width="1800" height="1200" alt="Map of Hapur-Modinagar Road from the Delhi-Meerut Expressway on-ramp to Isapur Industrial Park, with Modinagar and Hapur marked" loading="lazy" style="object-position: 40% 50%" data-source="map" data-subject="route map"></a></figure>`;
// the photo for section i of a page: rotates through the pool, never the hero's, a different start per page
export const pick = (seed, i, hero) => { const p = POOL.filter((k) => k !== hero); let n = 0; for (const c of seed) n += c.charCodeAt(0); return p[(n + i) % p.length]; };
