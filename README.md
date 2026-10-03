# TOD × UEFA Champions League – Campaign presentation

Creative Producer take-home test for TOD by beIN, by Abdelouahed Ayati.
Concept presentation only, not an official TOD page.

One page, two views:
- Default view: the test materials (promos and key visuals) on a TOD-style page.
- "Preview as customer" (corner button): the landing page a fan would reach from social media.

Direct link to the customer view: https://a-ayati.github.io/tod-uefa/#customer

Direct link to the campaign brief page: https://a-ayati.github.io/tod-uefa/#brief

## Files to add in `assets/`

| File | Content |
|---|---|
| `hero-textless.mp4` | 15-second film without text, used as the cover on the English site |
| `hero-ar.mp4` | 15-second film with a single Arabic line, used as the cover on the Arabic site |
| `promo-15s-ar.mp4`, `promo-15s-en.mp4` | 15-second promo, Arabic / English (shown by page language) |
| `promo-6s-ar.mp4`, `promo-6s-en.mp4` | 6-second promo, Arabic / English (shown by page language) |
| `kv-16x9.jpg` | Key visual 1920 × 1080 |
| `kv-1x1.jpg` | Key visual 1080 × 1080 |
| `kv-9x16.jpg` | Key visual 1080 × 1920 |
| `thumb-15s.jpg`, `thumb-15s-en.jpg` | Thumbnail for the 15s promo (a frame taken from the video) |
| `thumb-6s.jpg`, `thumb-6s-en.jpg` | Thumbnail for the 6s promo, 16:9 |
| `design-1.jpg`, `design-2.jpg`, `design-3.jpg` | The three designs shown in the "Campaign brief" page (any size, shown in a 4:5 frame) |
| `story-1.jpg`, `story-2.jpg`, `story-3.jpg` | The three story (9:16) versions, shown next to the 1:1 slider |
| `wide-1.jpg`, `wide-2.jpg`, `wide-3.jpg` | The three screen / TV (16:9) versions, shown below the 1:1 and story sliders |
| `customer-1.jpg`, `customer-2.jpg`, `customer-3.jpg` | The three 1:1 versions (without the watch button) shown in the customer view |
| `design-en-1..3.jpg`, `customer-en-1..3.jpg`, `story-en-1..3.jpg`, `wide-en-1..3.jpg` | English versions, shown when the page language is English (missing ones fall back to the Arabic file) |
| `character-sheet.webp` | Sample character sheet shown in the "Campaign brief" page |

## Club crests

The 36 club crests are already inside `index.html` (so the page works from a single file) and also
sit in `assets/crests/<CODE>.png` (128 px, transparent). Codes are listed in `assets/crests/README.txt`.
Club crests are trademarks of their owners; they come from football-logos.cc and are used here for
a non-commercial design test, not for promotion. For anything real, use the official TOD / UEFA assets.

## Live results

The "Champions League by the numbers" section refreshes itself every 2 minutes from ESPN's public
scoreboard and standings feeds (matches, results, table and top scorers). If the feed is unreachable
the built-in snapshot stays on screen. Assists are a manual snapshot in `index.html` (`ASSISTS`).
The ESPN feed is unofficial, so it can change without notice.

## Colours

Only the TOD colour system (TOD_Colour-Reference.pdf, v3.0) is used on the page:
TOD Yellow `#FFBC00`, TOD Black `#101010`, Deep Navy `#0C1423`, Royal Indigo `#262861`,
Royal Purple `#5B308E`, Cloud Grey `#D7D6D6`, Pure White `#FFFFFF`, and the "Happy" gradient accent `#E0298C` / `#FF6B5C`.
Secondary text, borders and glows are these colours at reduced opacity, never new hues.
