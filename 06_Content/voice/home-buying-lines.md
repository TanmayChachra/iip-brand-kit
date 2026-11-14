# Proposed replacement for the buying steps in src/pages/index.astro (lines 37 to 43), for the lead to apply

Drop the DRAFT comment on line 43 only when the owner confirms. Five steps become four (the "Payments through us" step is removed by owner decision 2026-11-14). If the home grid needs five, keep it at four.

```js
const steps = [
  ['First meeting', 'We show you what is for sale today and walk you through the park and the papers.'],
  ['Approvals and answers', 'See the approvals we hold. Every objection and cross question gets a straight answer.'],
  ['Payment plan', 'An industry standard plan, about three months on average. If you ever need to sell, we help you sell your land.'],
  ['Registry day', 'After about three months of payments we fix the registry day to suit both sides.'],
];
```

Line 41 replacement (old "Payments through us" step): removed. Its job is done by step 3 and step 4 above.

Also line 45 (home FAQ) is fine as is. Check any other "through us" in index.astro: none found beyond line 41.
