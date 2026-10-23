# Next phase: an interactive storybook world

Approved direction: preserve prototype 0.9's colorful storybook art direction,
characters, scenery, warmth, and atmosphere. This phase is planned separately;
the current hotspot correction does not redesign or repaint the artwork.

## Requirements and acceptance criteria

1. **One live interface.** Remove baked-in money bubbles, season/day labels,
   navigation icons, buttons, prices, and other interface text from scene art.
   Render exactly one functional set. Every displayed balance, day, season,
   quantity, price, and goal must reflect the actual game state. No static
   illustrated copy of a control may remain behind its real counterpart.
2. **A real 5 × 5 garden.** The 25 plots belong to the illustrated game world,
   rather than transparent cells above a pre-planted background. Empty plots
   show empty soil. Planting places the correct crop in the chosen plot.
   Watering and each growth stage visibly update that crop. Harvest removes a
   one-time crop or resets a repeat crop to its appropriate regrowth stage;
   exhausted repeat crops leave empty soil. Artwork, labels, hit targets, and
   saved state must agree for every plot.
3. **Real illustrated garden tools.** The illustrated Water and End Day
   controls become the actual buttons. They have visible press/focus/disabled
   feedback and accessible labels. Remove duplicate controls below the scene.
4. **Interactive stores and market.** Merchandise, baskets, shelves, produce,
   scales, money, equipment, and customers become individually rendered,
   state-driven game objects. Whole-scene pictures with invisible clickable
   rectangles are a temporary bridge, not the final implementation. Adding
   merchandise, weighing, filling orders, buying equipment, and making change
   must visibly change the corresponding objects in the scene.
5. **Keep scenes visible.** Preserve shopkeepers and scenery while presenting
   compact contextual information; avoid large shopping menus or dialogs that
   cover the illustrated world. Maintain the educational gameplay, customer
   conversations, calculation of totals, and counting back change.
6. **Responsive and accessible.** Use a shared object coordinate system for
   drawing and interaction. Validate phone/tablet/desktop layouts, touch and
   keyboard input, labels, contrast, and suitable touch target sizes. Check
   actual Safari/iPhone behavior as well as Chromium.

## Proposed implementation order

Inventory and separate background/foreground/control art without overwriting
originals; establish scene/object components; build the state-driven garden and
its tools first; then migrate Seed & Feed, Dream Shop, Market Supplies, and the
market. Add visual regression and gameplay tests at each step. Keep source
prototypes and original assets as immutable references. Develop and approve on
the development branch; do not merge or deploy as part of this plan.
