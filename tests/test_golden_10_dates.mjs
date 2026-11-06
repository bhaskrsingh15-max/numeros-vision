import assert from 'node:assert/strict';
import { viewFor } from '../app/static/_worker.js';

const GOLDEN_10_DATES = [
  { dob: '28-11-1981', d: 28, m: 11, y: 1981, driver: 1, conductorRaw: 4, conductorRoot: 4, conductorDisplay: '4', planet: 'Rahu' },
  { dob: '15-07-1990', d: 15, m: 7, y: 1990, driver: 6, conductorRaw: 5, conductorRoot: 5, conductorDisplay: '5', planet: 'Mercury' },
  { dob: '10-08-1990', d: 10, m: 8, y: 1990, driver: 1, conductorRaw: 1, conductorRoot: 1, conductorDisplay: '1', planet: 'Sun' },
  { dob: '12-03-1982', d: 12, m: 3, y: 1982, driver: 3, conductorRaw: 8, conductorRoot: 8, conductorDisplay: '8', planet: 'Saturn' },
  { dob: '01-01-2007', d: 1, m: 1, y: 2007, driver: 1, conductorRaw: 11, conductorRoot: 2, conductorDisplay: '11/2', planet: 'Moon' },
  { dob: '14-06-1980', d: 14, m: 6, y: 1980, driver: 5, conductorRaw: 11, conductorRoot: 2, conductorDisplay: '11/2', planet: 'Moon' },
  { dob: '02-09-2009', d: 2, m: 9, y: 2009, driver: 2, conductorRaw: 22, conductorRoot: 4, conductorDisplay: '22/4', planet: 'Rahu' },
  { dob: '29-11-1999', d: 29, m: 11, y: 1999, driver: 2, conductorRaw: 5, conductorRoot: 5, conductorDisplay: '5', planet: 'Mercury' },
  { dob: '15-08-1990', d: 15, m: 8, y: 1990, driver: 6, conductorRaw: 33, conductorRoot: 6, conductorDisplay: '33/6', planet: 'Venus' },
  { dob: '24-09-1999', d: 24, m: 9, y: 1999, driver: 6, conductorRaw: 7, conductorRoot: 7, conductorDisplay: '7', planet: 'Ketu' },
];

// Browser calculator unified function (lo-shu-grid.html / life-path-calculator.html / index.html)
function browserCalculate(d, m, y) {
  function reduceToSingle(num, preserveMaster = false) {
    let val = Math.abs(num);
    while (val > 9) {
      if (preserveMaster && (val === 11 || val === 22 || val === 33)) return val;
      val = String(val).split('').reduce((acc, digit) => acc + parseInt(digit, 10), 0);
    }
    return val;
  }
  const PLANETS = {
    1: 'Sun', 2: 'Moon', 3: 'Jupiter', 4: 'Rahu', 5: 'Mercury',
    6: 'Venus', 7: 'Ketu', 8: 'Saturn', 9: 'Mars'
  };
  const driver = reduceToSingle(d, false);
  const dobStr = `${String(d).padStart(2, '0')}${String(m).padStart(2, '0')}${String(y).padStart(4, '0')}`;
  const conductorRaw = reduceToSingle(dobStr.split('').reduce((acc, ch) => acc + parseInt(ch, 10), 0), true);
  const conductorRoot = reduceToSingle(conductorRaw, false);
  const conductorDisplay = conductorRaw > 9 ? `${conductorRaw}/${conductorRoot}` : `${conductorRoot}`;
  return {
    driver,
    conductorRaw,
    conductorRoot,
    conductorDisplay,
    planet: PLANETS[conductorRoot]
  };
}

async function run() {
  const user = { user_id: 'usr_golden_test' };
  const env = {};

  for (const row of GOLDEN_10_DATES) {
    const view = await viewFor(user, { id: 'sub_golden', name: 'Seeker', dob: row.dob }, env);
    assert.equal(view.calculation.driver, row.driver, `${row.dob} viewFor driver`);
    assert.equal(view.calculation.conductorRaw, row.conductorRaw, `${row.dob} viewFor conductorRaw`);
    assert.equal(view.calculation.conductor, row.conductorRoot, `${row.dob} viewFor conductor root`);
    assert.equal(view.calculation.conductorDisplay, row.conductorDisplay, `${row.dob} viewFor conductorDisplay`);
    assert.equal(view.calculation.conductorPlanet, row.planet, `${row.dob} viewFor conductorPlanet`);

    const br = browserCalculate(row.d, row.m, row.y);
    assert.equal(br.driver, row.driver, `${row.dob} browser driver`);
    assert.equal(br.conductorRaw, row.conductorRaw, `${row.dob} browser conductorRaw`);
    assert.equal(br.conductorRoot, row.conductorRoot, `${row.dob} browser conductorRoot`);
    assert.equal(br.conductorDisplay, row.conductorDisplay, `${row.dob} browser conductorDisplay`);
    assert.equal(br.planet, row.planet, `${row.dob} browser planet`);
  }

  console.log('PASS: All 10 golden dates verified across viewFor and browser calculator rules.');
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
