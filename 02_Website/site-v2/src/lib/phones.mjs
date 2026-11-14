// THE ONE PLACE FOR PHONE NUMBERS. Swap here and every page, link, schema and WhatsApp link follows.
// Owner decision 2026-11-12 (final): the only public number is 98377 64222, also the WhatsApp number.
// 98370 57800 is retired everywhere. 92195 49800 is allowed ONLY for renting (owner, 2026-11-14): see RENT_PHONE.
export const PHONES = [
  { display: '98377 64222', tel: '+919837764222' },
];
// RENT_PHONE: call number for the rent and lease section and the rent page only. Never in PHONES, header, footer, sticky bar or schema. WhatsApp stays WHATSAPP everywhere.
export const RENT_PHONE = { display: '92195 49800', tel: '+919219549800' };
export const WHATSAPP = '919837764222'; // WhatsApp is 98377 64222
export const HOURS_TEXT = 'Open 8 am to 8 pm every day except Tuesday.';
export const fill = (s) => typeof s !== 'string' ? s : s
  .replaceAll('{{phone1}}', PHONES[0].display).replaceAll('{{phone1_tel}}', PHONES[0].tel)
  .replaceAll('{{rent_phone}}', RENT_PHONE.display).replaceAll('{{rent_phone_tel}}', RENT_PHONE.tel).replaceAll('{{wa}}', WHATSAPP).replaceAll('{{hours}}', HOURS_TEXT);
export const fillDeep = (v) => Array.isArray(v) ? v.map(fillDeep) : v && typeof v === 'object' && !(v instanceof Date) ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, fillDeep(x)])) : fill(v);
