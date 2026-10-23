# My Garden Grows 1.0 development

Development branch: `development/1.0`. Nothing has been pushed, merged, or deployed.

## Preview safely

For a Mac playtest without Terminal: download the ZIP of the `development/1.0`
branch from GitHub (green **Code → Download ZIP** on that branch), double-click
the ZIP in Finder, open `playtest`, and open `My-Garden-Grows-1.0.html` with Chrome
or Safari. The file embeds all scripts, styles, and artwork. Keep the same file
and browser for saved progress. The GitHub branch must be available remotely;
this does not require merging or enabling GitHub Pages.

For developers, `npm start` serves the repository on port 8000; open the
`/development/` path. `python3 scripts/build_playtest.py` regenerates the
self-contained playtest after source edits. Do not edit the generated HTML
manually. Chat sandbox download links have failed for this user; use GitHub's
ZIP download rather than the chat side-panel download icon.

The root `index.html` remains the original working prototype 0.6. `prototypes/` contains byte-for-byte copies of both supplied originals. The development game references extracted, unchanged 0.9 image assets. The first seven crops use 0.6 rules; tomato, lettuce, and radish retain 0.9 values, with finite repeat harvests for tomatoes.

## Source layout

- `development/src/game.js`: DOM-independent rules, validated saves, crop definitions, purchasing, planting/growth, orders, and money transactions.
- `development/src/catalog.js`: scene artwork mapping, dreams, customer names, and shop descriptions.
- `development/src/scenes.js`: illustrated scene rendering, dialogs, navigation, and browser persistence.
- `development/src/interactions.js`: UI actions connected to tested rules, planting plans, market display, and learning feedback.
- `development/src/styles.css`: extracted prototype styling with small focus/input improvements.
- `development/assets/`: original 0.9 artwork, extracted without conversion.

## Validation

Run `npm test` with Node.js 18+ (no npm dependencies required).

Run `python3 tests/browser_smoke.py` for the phone-sized end-to-end test. It starts and shuts down its own HTTP server. It requires Python Playwright and Chromium at `/usr/bin/chromium`, both provided in this cloud environment. On another machine install Playwright and adjust the browser executable path as necessary.

The browser test purchases corn, plans and plants it, waters and advances days, harvests, arranges the market, greets a customer, fills an order, enters a calculated total, collects payment, counts change, reloads progress, recovers a corrupt save from backup, and handles both saves being invalid.

## Save behavior

Development uses `mgg10` and `mgg10-backup`; prototype `mgg09` and `mgg_v06` are untouched. Saves are validated before rendering. Invalid primary data falls back to the backup; if neither is valid, a new playable farm starts. Interrupted orders are cancelled on reload without charging money or removing inventory. Purchases and completed sales persist. Starting a new farm replaces only development progress. Automatic migration from the prototypes is deliberately not implemented because their schemas and crop balances differ.

## Remaining work

This is the first development phase, not an App Store build. Original baked-in labels and imagery, large dialogs, and the three fixed decorative market hotspots remain. Produce quantities and purchased equipment do not yet alter the illustrated backgrounds. Bags and canopy effects/customer personalities need a later gameplay pass. Manual Safari/iPhone testing, accessibility work, asset-to-hotspot audits, and broader visual regression coverage remain. The browser automation verifies Chromium, not iOS Safari.

## Hotspot alignment validation

`python3 tests/browser_hotspots.py` clicks independently measured landmarks in
all 20 shop objects at 320, 390, 768, and 1440px viewport widths. It tests object
centers and interior edge points, verifies the matching dialog, and checks the
standalone playtest makes no external asset requests. Coordinates are centralized
in `SHOP_HOTSPOTS` in `catalog.js`, keyed by item ID rather than crop-array order.
The ten seed packets now match their illustrated positions and bottom-row order.
Original artwork remains unchanged; see `VISUAL-REDESIGN.md` for the approved
requirements for the next development phase.
