# Event spec (contract file, read by the web agent)

Version 1, 2026-11-08. Bump the version line when anything changes.

GTM is the only third-party script on the site. The page pushes events to `window.dataLayer`; GTM turns them into GA4 events. Names follow GA4 recommended event names where one exists.

## Page-level data (pushed once per page load, before GTM)
```js
dataLayer.push({
  page_type: 'home|plots|amenities|location|brands|gallery|blog|faq|contact|landing',
  page_lang: 'en',
  location_slug: 'modinagar|hapur|ghaziabad|expressway|none',   // for location landing pages
  tagline_variant: 'A|B'                                       // which approved tagline the page shows (A/B test key)
});
```

## Events
| Event name | When | Parameters | Conversion |
|---|---|---|---|
| `click_call` | tap on any `tel:` link | `phone`, `cta_id`, `section`, `page_type` | yes |
| `click_whatsapp` | tap on any `wa.me` link | `cta_id`, `section`, `page_type`, `message_variant` | yes |
| `generate_lead` | enquiry form submitted successfully | `form_id`, `plot_size_interest`, `purpose` (own use / invest), `timeline`, `page_type` | yes |
| `click_directions` | tap on map or directions link | `cta_id`, `section` | yes |
| `file_download` | brochure or layout PDF download | `file_name`, `file_type` | secondary |
| `select_plot_size` | plot size chip or tab chosen | `plot_size` | no |
| `cta_click` | any other CTA button | `cta_id`, `cta_text`, `section` | no |
| `view_section` | key section 50 percent visible (IntersectionObserver, once per page) | `section` (hero, plots, amenities, location, brands, faq, contact) | no |
| `faq_expand` | FAQ item opened | `question_id` | no |
| `video_start` | site or park video played | `video_id` | no |
| `outbound_click` | link to another domain (GMB, social, UPSIDA) | `link_domain`, `link_url` | no |
| `scroll` | 25, 50, 75, 90 percent (GTM scroll trigger) | `percent_scrolled` | no |
| `page_404` | custom 404 shown | `requested_path` | no |
| `calculator_use` | later: cost or area calculator | `input_area`, `result` | later |

## Rules
- Every CTA element carries `data-cta-id`, `data-section` attributes. One delegated listener reads them (no inline script per button).
- IDs are stable lowercase slugs, for example `hero-call`, `sticky-whatsapp`, `plots-enquire`.
- No personal data in events. Phone numbers entered in forms are never pushed to the dataLayer.
- Form `generate_lead` fires only after the form backend confirms success.
- UTM scheme (also used for GBP, listings and social): `utm_source` (google, bing, justdial, indiamart, facebook, whatsapp, offline-qr), `utm_medium` (organic, cpc, listing, social, referral, qr), `utm_campaign` (gbp, directory, launch, brand-name), `utm_content` (ad or post id). Lowercase, hyphens.
- Consent: banner and consent mode to be decided with the owner (India DPDP Act 2023 awareness). Default plan: GA4 with IP anonymised, Clarity masked inputs, no ad pixels until ads start.
