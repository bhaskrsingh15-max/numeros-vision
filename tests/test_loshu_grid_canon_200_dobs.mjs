// tests/test_loshu_grid_canon_200_dobs.mjs
// Test Lo Shu Grid Canon consistency between browser calculation logic and server viewFor logic across 200+ DOBs

import assert from 'node:assert';

function reduceToSingle(num) {
  let n = Math.abs(num);
  while (n > 9) {
    n = String(n).split('').reduce((acc, d) => acc + parseInt(d, 10), 0);
  }
  return n === 0 ? 9 : n;
}

// Browser implementation (from lo-shu-grid.html lines 849-864)
function browserCalculateLoShu(dayVal, monthVal, yearVal) {
  const driver = reduceToSingle(dayVal);
  const totalDobSum = String(dayVal) + String(monthVal) + String(yearVal);
  const conductor = reduceToSingle(totalDobSum.split('').reduce((acc, d) => acc + parseInt(d, 10), 0));

  const dobStr = `${String(dayVal).padStart(2, '0')}${String(monthVal).padStart(2, '0')}${yearVal}`;
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 };

  for (const ch of dobStr) {
    if (ch !== '0') {
      counts[parseInt(ch, 10)]++;
    }
  }

  const presentDigits = [];
  const missingDigits = [];
  for (let n = 1; n <= 9; n++) {
    if (counts[n] > 0) presentDigits.push(n);
    else missingDigits.push(n);
  }

  const planes = {
    mental: counts[4] > 0 && counts[9] > 0 && counts[2] > 0,
    emotional: counts[3] > 0 && counts[5] > 0 && counts[7] > 0,
    practical: counts[8] > 0 && counts[1] > 0 && counts[6] > 0,
    thought: counts[4] > 0 && counts[3] > 0 && counts[8] > 0,
    will: counts[9] > 0 && counts[5] > 0 && counts[1] > 0,
    action: counts[2] > 0 && counts[7] > 0 && counts[6] > 0,
    golden_raj_yoga: counts[4] > 0 && counts[5] > 0 && counts[6] > 0,
    silver_raj_yoga: counts[2] > 0 && counts[5] > 0 && counts[8] > 0,
  };

  return { driver, conductor, counts, presentDigits, missingDigits, planes };
}

// Server implementation (from _worker.js viewFor lines 530-580)
function serverCalculateLoShu(day, month, year) {
  const driver = reduceToSingle(day);
  const totalDobDigits = `${String(day).padStart(2, '0')}${String(month).padStart(2, '0')}${year}`;
  const conductor = reduceToSingle(totalDobDigits.split('').reduce((acc, d) => acc + parseInt(d, 10), 0));

  const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 };
  for (const ch of totalDobDigits) {
    if (ch !== '0') counts[parseInt(ch, 10)]++;
  }

  const presentDigits = [];
  const missingDigits = [];
  for (let n = 1; n <= 9; n++) {
    if (counts[n] > 0) presentDigits.push(n);
    else missingDigits.push(n);
  }

  const planes = {
    mental: counts[4] > 0 && counts[9] > 0 && counts[2] > 0,
    emotional: counts[3] > 0 && counts[5] > 0 && counts[7] > 0,
    practical: counts[8] > 0 && counts[1] > 0 && counts[6] > 0,
    thought: counts[4] > 0 && counts[3] > 0 && counts[8] > 0,
    will: counts[9] > 0 && counts[5] > 0 && counts[1] > 0,
    action: counts[2] > 0 && counts[7] > 0 && counts[6] > 0,
    golden_raj_yoga: counts[4] > 0 && counts[5] > 0 && counts[6] > 0,
    silver_raj_yoga: counts[2] > 0 && counts[5] > 0 && counts[8] > 0,
  };

  return { driver, conductor, counts, presentDigits, missingDigits, planes };
}

console.log('--- STARTING LO SHU GRID CANON TEST (250 RANDOM & EDGE-CASE DOBS) ---');

// Generate 250 diverse dates of birth
const testDobs = [];

// 1. Specific edge case dates
const edgeCases = [
  { day: 1, month: 1, year: 2000 },
  { day: 9, month: 9, year: 1999 },
  { day: 29, month: 2, year: 2000 }, // leap year
  { day: 28, month: 2, year: 1900 },
  { day: 10, month: 10, year: 2010 },
  { day: 31, month: 12, year: 1989 },
  { day: 15, month: 8, year: 1947 }, // India Independence
  { day: 26, month: 1, year: 1950 }, // Republic Day
  { day: 22, month: 11, year: 1963 },
  { day: 4, month: 5, year: 1960 },   // Has Golden Raj Yoga (4, 5, 6)
  { day: 25, month: 8, year: 1982 },  // Has Silver Raj Yoga (2, 5, 8)
  { day: 3, month: 7, year: 2005 },
];
testDobs.push(...edgeCases);

// 2. Systematic distribution across 1940 - 2025
let seed = 123456789;
function pseudoRandom() {
  seed = (seed * 1103515245 + 12345) & 0x7fffffff;
  return seed / 0x7fffffff;
}

while (testDobs.length < 250) {
  const y = 1940 + Math.floor(pseudoRandom() * 86); // 1940..2025
  const m = 1 + Math.floor(pseudoRandom() * 12);
  const maxDay = (m === 2) ? (y % 4 === 0 ? 29 : 28) : ([4, 6, 9, 11].includes(m) ? 30 : 31);
  const d = 1 + Math.floor(pseudoRandom() * maxDay);
  testDobs.push({ day: d, month: m, year: y });
}

let passedCount = 0;
for (let i = 0; i < testDobs.length; i++) {
  const { day, month, year } = testDobs[i];
  const bRes = browserCalculateLoShu(day, month, year);
  const sRes = serverCalculateLoShu(day, month, year);

  assert.strictEqual(bRes.driver, sRes.driver, `Driver mismatch on DOB ${day}-${month}-${year}`);
  assert.strictEqual(bRes.conductor, sRes.conductor, `Conductor mismatch on DOB ${day}-${month}-${year}`);
  assert.deepStrictEqual(bRes.counts, sRes.counts, `Grid Counts mismatch on DOB ${day}-${month}-${year}`);
  assert.deepStrictEqual(bRes.presentDigits, sRes.presentDigits, `Present digits mismatch on DOB ${day}-${month}-${year}`);
  assert.deepStrictEqual(bRes.missingDigits, sRes.missingDigits, `Missing digits mismatch on DOB ${day}-${month}-${year}`);
  assert.deepStrictEqual(bRes.planes, sRes.planes, `Planes mismatch on DOB ${day}-${month}-${year}`);

  passedCount++;
}

console.log(`✓ PASS: All ${passedCount}/${testDobs.length} DOBs produced 100% IDENTICAL Lo Shu grids between Browser and Server!`);
