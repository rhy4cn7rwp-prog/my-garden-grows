const { test } = require("node:test");
const assert = require("node:assert/strict");
const G = require("../development/src/game.js");
test("purchases debit once, bundle saves $1, insufficient funds are atomic", () => {
  let s = G.initial();
  s.cart = { bundle: 1 };
  assert.equal(
    Object.entries(G.bundle).reduce(
      (a, [id, n]) => a + G.crops.find((c) => c.id === id).seed * n,
      0,
    ),
    12,
  );
  assert.equal(G.purchase(s, "seeds"), 11);
  assert.equal(s.cash, 39);
  assert.equal(s.seeds.carrot, 3);
  assert.throws(() => G.purchase(s, "seeds"));
  s.cart = { strawberry: 100 };
  assert.throws(() => G.purchase(s, "seeds"));
  assert.equal(s.cash, 39);
});
test("supplies cannot be purchased twice or in duplicate quantities", () => {
  let s = G.initial();
  s.supcart = { scale: 1 };
  G.purchase(s, "supplies");
  s.supcart = { scale: 1 };
  assert.throws(() => G.purchase(s, "supplies"));
  assert.equal(s.cash, 45);
});
test("savings goals are validated and changing goals resets celebration", () => {
  let s = G.initial();
  s.won = true;
  G.chooseGoal(s, 0);
  assert.equal(s.goal, 0);
  assert.equal(s.won, false);
  assert.throws(() => G.chooseGoal(s, 99));
});
test("planting reserves seeds and commits a plan without overspending seeds", () => {
  let s = G.initial();
  s.seeds.carrot = 1;
  G.plan(s, 0, "carrot");
  assert.throws(() => G.plan(s, 1, "carrot"));
  assert.equal(s.seeds.carrot, 1);
  G.plantPlan(s);
  assert.equal(s.seeds.carrot, 0);
  assert.equal(s.plots[0].id, "carrot");
  assert.throws(() => G.plan(s, 0, "carrot"));
});
test("watered days grow crops; dry days reduce quality; premature harvest fails", () => {
  let s = G.initial();
  s.seeds.carrot = 1;
  G.plan(s, 0, "carrot");
  G.plantPlan(s);
  assert.throws(() => G.harvest(s, 0));
  G.endDay(s);
  assert.equal(s.plots[0].age, 1);
  G.endDay(s);
  assert.equal(s.plots[0].age, 1);
  assert.ok(s.plots[0].quality < 100);
  G.water(s);
  G.endDay(s);
  assert.equal(s.plots[0].age, 2);
});
test("repeat crops have exactly three harvests and truthful occupancy messages", () => {
  let s = G.initial();
  s.seeds.beans = 1;
  G.plan(s, 0, "beans");
  G.plantPlan(s);
  for (let n = 0; n < 3; n++) {
    s.plots[0].age = 3;
    let message = G.harvest(s, 0);
    assert.match(message, n < 2 ? /another harvest/ : /free to replant/);
    assert.equal(!!s.plots[0], n < 2);
  }
  assert.equal(s.inventory.beans, 3);
});
test("market cannot reopen until next farming day and seasons last 20 days", () => {
  let s = G.initial();
  s.display.carrot = 1;
  G.openMarket(s);
  G.closeMarket(s);
  assert.throws(() => G.openMarket(s));
  G.endDay(s);
  G.openMarket(s);
  assert.equal(s.hour, 9);
  s.day = 20;
  G.endDay(s);
  assert.equal(s.day, 1);
  assert.equal(s.season, 2);
});
function shopper() {
  let s = G.initial();
  s.inventory.corn = 4;
  s.display.corn = 4;
  G.openMarket(s);
  G.newCustomer(s, "Maya");
  return s;
}
test("greeting, requested quantities and calculated total gate payment", () => {
  let s = shopper();
  s.basket = { corn: 1 };
  assert.throws(() => G.ring(s, 3));
  G.greet(s);
  s.basket = {};
  assert.throws(() => G.ring(s, 3));
  s.basket = { corn: 1 };
  assert.throws(() => G.ring(s, 4));
  G.ring(s, 3);
  assert.equal(s.step, "pay");
});
test("wrong change cannot charge; correct payment settles once", () => {
  let s = shopper();
  G.greet(s);
  s.basket = { corn: 1 };
  G.ring(s, 3);
  s.change = 1;
  assert.throws(() => G.finish(s));
  assert.equal(s.cash, 50);
  s.change = 2;
  G.finish(s);
  assert.equal(s.cash, 53);
  assert.equal(s.inventory.corn, 3);
  assert.equal(s.display.corn, 3);
  assert.throws(() => G.finish(s));
  assert.equal(s.cash, 53);
});
test("scale is required for by-pound orders", () => {
  let s = G.initial();
  s.inventory.beans = 1;
  s.display.beans = 1;
  G.openMarket(s);
  G.newCustomer(s, "Maya");
  G.greet(s);
  s.basket = { beans: 1 };
  assert.throws(() => G.ring(s, 4));
  s.owned.scale = 1;
  G.ring(s, 4);
});
test("save recovery handles malformed, partial, invalid, and valid saves", () => {
  for (const raw of [
    "{",
    "null",
    JSON.stringify({ version: 1, plots: Array(25).fill(null) }),
    JSON.stringify({ ...G.initial(), goal: 999 }),
    JSON.stringify({ ...G.initial(), plots: [{}] }),
  ])
    assert.deepEqual(G.recover(raw), G.initial());
  let s = shopper();
  s.cash = 37.5;
  let recovered = G.recover(JSON.stringify(s));
  assert.equal(recovered.cash, 37.5);
  assert.equal(recovered.customer, null);
  assert.equal(recovered.marketPlayed, true);
  assert.equal(recovered.inventory.corn, 4);
});

test("a corrupt primary save recovers the last valid backup", () => {
  const s = G.initial();
  s.cash = 42;
  assert.equal(G.recover("{broken", JSON.stringify(s)).cash, 42);
  assert.deepEqual(G.recover("{broken", "{also broken"), G.initial());
});

test("original 0.6 and extracted 0.9 artwork are byte-for-byte preserved", () => {
  const fs = require("node:fs"),
    path = require("node:path");
  const root = path.join(__dirname, "..");
  assert.deepEqual(
    fs.readFileSync(path.join(root, "index.html")),
    fs.readFileSync(path.join(root, "prototypes/my_garden_grows_v06.html")),
  );
  const original = fs.readFileSync(
    path.join(root, "prototypes/my_garden_grows_v09.html"),
    "utf8",
  );
  const matches = [
    ...original.matchAll(
      /data:image\/(png|webp|jpeg);base64,([A-Za-z0-9+/=]+)/g,
    ),
  ];
  assert.equal(matches.length, 6);
  matches.forEach((m, i) =>
    assert.deepEqual(
      fs.readFileSync(
        path.join(
          root,
          `development/assets/scene-${i + 1}.${m[1] === "jpeg" ? "jpg" : m[1]}`,
        ),
      ),
      Buffer.from(m[2], "base64"),
    ),
  );
});
