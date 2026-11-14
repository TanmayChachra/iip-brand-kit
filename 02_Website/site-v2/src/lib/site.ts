import { PHONES, WHATSAPP, HOURS_TEXT } from './phones.mjs';
// One place for the facts every page shares. Source of truth: 00_ISAPUR_KNOWLEDGE.md and 05_Local-Presence/citations/nap.md
// ONE swap point for every Get directions link (hero, sticky bar, visit block, contact page, footer). Owner will supply the exact Google Maps place link; replace it here only.
export const DIRECTIONS_URL = 'https://www.google.com/maps/search/?api=1&query=Isapur+Industrial+Park+Hapur+Modinagar+Road+Ghaziabad';
export const SITE = {
  name: 'Isapur Industrial Park',
  short: 'IIP',
  tagline: 'A Modern Industrial Address.',
  address: 'Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, UP 201022',
  street: 'Hapur-Modinagar Road, Yusufpur Isapur',
  city: 'Ghaziabad',
  region: 'Uttar Pradesh',
  postal: '201022',
  phones: PHONES, // swap numbers in phones.mjs only
  // ponytail: WhatsApp number defaults to the first phone, owner to confirm in 04_Analytics / TODOS
  whatsapp: import.meta.env.PUBLIC_WHATSAPP || WHATSAPP,
  hours: HOURS_TEXT,
  geo: { lat: 28.7809, lon: 77.6559 }, // Maps pin for Phase 1, accuracy about 200 m (knowledge file section 2)
  mapsUrl: 'https://www.google.com/maps/place/Isapur+Industrial+Park+Phase+1/@28.7808965,77.6533041,17z',
  directionsUrl: DIRECTIONS_URL,
  waText: 'Hello, I want to know about industrial plots at Isapur Industrial Park.',
};
export const waLink = (text = SITE.waText) => `https://wa.me/${SITE.whatsapp}?text=${encodeURIComponent(text)}`;
export const mapSearch = 'https://www.openstreetmap.org/search?query=Hapur-Modinagar%20Road%20Yusufpur%20Isapur';
export const NAV = [
  { href: '/#visit', label: 'Visit' },
  { href: '/industrial-plots/', label: 'Plots' },
  { href: '/plot-maps/', label: 'Plot maps' },
  { href: '/industrial-shed-for-rent/', label: 'Rent a Factory' },
  { href: '/location/', label: 'Location' },
  { href: '/neighbours/', label: 'Around us' },
  { href: '/faq/', label: 'FAQ' },
];
