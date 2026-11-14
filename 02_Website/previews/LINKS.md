# Preview links (private, noindex, unlisted)

Deployed 2026-11-13 with `npx wrangler pages deploy` (account IsapurIndustrialPark). Start at the navigator.

| Variant | URL | This deployment | HTTP | X-Robots-Tag |
|---|---|---|---|---|
| Navigator | https://iipreview-nav.pages.dev/ | https://ee9bc3d5.iipreview-nav.pages.dev | 200 | noindex, nofollow, noarchive |
| Website v3 (current) | https://iipreview-v3.pages.dev/ | https://3641909f.iipreview-v3.pages.dev | 200 | noindex, nofollow, noarchive |
| Website v2 (earlier) | https://iipreview-v2.pages.dev/ | https://3d2c3626.iipreview-v2.pages.dev | 200 | noindex, nofollow, noarchive |
| Website v1 (rejected) | https://iipreview-v1.pages.dev/ | https://36b21026.iipreview-v1.pages.dev | 200 | noindex, nofollow, noarchive |
| Brand kit (new build) | https://iipreview-kit.pages.dev/ | https://45a08f84.iipreview-kit.pages.dev | 200 | noindex, nofollow, noarchive |

Each home returns exactly one h1. v3 /faq/ 200, /robots.txt 200 (Disallow: /), unknown path 404.
Kit package omits `ISAPUR-Brand-Book.pdf` (59 MB, over the 25 MB Pages file limit). v3 package omits `public/assets` (36 MB design toolkit, not used by the site).
v2 is the rebuild of commit 959f456 (old phones and claims, ribbon "Earlier version, preview only", public/assets kept because the site needs it).
