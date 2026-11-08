// THE ONE PLACE FOR PHONE NUMBERS. Swap here and every page, link, schema and WhatsApp link follows.
// Owner decision 2026-11-08: the second number is 9837764222 for now; swap it to 9219549800 later.
export const PHONES = [
  { display: '98370 57800', tel: '+919837057800' },
  { display: '98377 64222', tel: '+919837764222' }, // SWAP LATER: { display: '92195 49800', tel: '+919219549800' }
];
// WhatsApp number (digits only, country code first). Owner to confirm which number is on WhatsApp.
export const WHATSAPP = '919837057800';
export const HOURS_TEXT = 'Open 8 am to 8 pm every day except Tuesday.';
export const fill = (s) => typeof s !== 'string' ? s : s
  .replaceAll('{{phone1}}', PHONES[0].display).replaceAll('{{phone1_tel}}', PHONES[0].tel)
  .replaceAll('{{phone2}}', PHONES[1].display).replaceAll('{{phone2_tel}}', PHONES[1].tel)
  .replaceAll('{{wa}}', WHATSAPP).replaceAll('{{hours}}', HOURS_TEXT);
export const fillDeep = (v) => Array.isArray(v) ? v.map(fillDeep) : v && typeof v === 'object' && !(v instanceof Date) ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, fillDeep(x)])) : fill(v);
