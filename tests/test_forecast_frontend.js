// Controller contract test with a fake API; no browser or MySQL required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

let forecastController;
const angular = {
  module: () => ({
    factory() { return this; },
    run() { return this; },
    controller(name, fn) { if (name === 'forecastController') forecastController = fn; return this; },
    config() { return this; }
  })
};
const charts = [];
function Chart(canvas, config) {
  charts.push(config);
  this.destroy = () => {};
}
const context = { angular, Chart, window: { Chart }, document: { getElementById: id => ({ id }) } };
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../fancyhotel/static/js/controllers.js'), 'utf8'), context);
assert.equal(typeof forecastController, 'function');

const scope = { $on() {} };
const calls = [];
const data = {
  locations: ['Atlanta'], room_types: ['Standard'],
  history: [{ month: '2026-07', location: 'Atlanta', room_nights: 4, occupancy_percent: 6.5 }],
  forecast: [{ month: '2026-08', location: 'Atlanta', room_nights: 5, occupancy_percent: 8.1 }],
  backtest_mae: {}, insufficient_data: false
};
const reportFactory = { Forecast(filters) {
  calls.push({ ...filters });
  return { $promise: Promise.resolve(data) };
} };
forecastController(scope, { userType: 'manager' }, reportFactory, fn => fn());
setImmediate(() => {
  assert.equal(calls.length, 1);
  assert.equal(scope.totalHistorical, 4);
  assert.equal(scope.totalForecast, 5);
  assert.equal(charts.length, 3);
  assert.equal(charts[0].data.labels.length, 1);
  assert.equal(charts[1].data.labels.length, 2);
  assert.equal(charts[1].data.datasets[1].data[1], 5);
  scope.filters.location = 'Atlanta';
  scope.filters.type = 'Standard';
  scope.filters.horizon = 2;
  scope.load();
  setImmediate(() => {
    assert.equal(calls.length, 2);
    assert.equal(calls[1].location, 'Atlanta');
    assert.equal(calls[1].type, 'Standard');
    assert.equal(calls[1].horizon, 2);
    data.forecast = [];
    scope.filters.type = 'Suite';
    scope.load();
    setImmediate(() => {
      assert.equal(scope.totalForecast, 0);
      assert.equal(charts[7].data.datasets.length, 1);
      console.log('Frontend controller contract: OK');
    });
  });
});
