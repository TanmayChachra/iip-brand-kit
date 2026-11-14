// THE ONE PLACE FOR PHONE NUMBERS. Swap here and every page, link, schema and WhatsApp link follows.
// Owner decision 2026-11-12 (final): the only public number is 98377 64222, also the WhatsApp number.
// 98370 57800 is retired everywhere. 92195 49800 is HELD OFF the site until the owner says (about 2026-11-19).
export const PHONES = [
  { display: '98377 64222', tel: '+919837764222' },
];
// HELD: nothing imports or renders this. To publish it later, push it into PHONES (and review copy, schema, llms.txt).
export const HELD = { display: '92195 49800', tel: '+919219549800' };
export const WHATSAPP = '919837764222'; // WhatsApp is 98377 64222
export const HOURS_TEXT = 'Open 8 am to 8 pm every day except Tuesday.';
export const fill = (s) => typeof s !== 'string' ? s : s
  .replaceAll('{{phone1}}', PHONES[0].display).replaceAll('{{phone1_tel}}', PHONES[0].tel)
  .replaceAll('{{wa}}', WHATSAPP).replaceAll('{{hours}}', HOURS_TEXT);
export const fillDeep = (v) => Array.isArray(v) ? v.map(fillDeep) : v && typeof v === 'object' && !(v instanceof Date) ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, fillDeep(x)])) : fill(v);
