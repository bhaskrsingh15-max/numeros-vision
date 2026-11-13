import assert from 'node:assert/strict';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import worker from '../app/static/_worker.js';

const require = createRequire(import.meta.url);
const NVKua = require('../app/static/js/nv_kua.js');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATIC_DIR = path.resolve(__dirname, '../app/static');

function readStatic(rel) {
  return fs.readFileSync(path.join(STATIC_DIR, rel), 'utf8');
}

// Extract and run real functions from each page's inline script
function evalSnippet(code, extraContext = {}) {
  const ctx = vm.createContext({
    Math,
    String,
    Number,
    Array,
    Set,
    Object,
    JSON,
    Date,
    parseInt,
    isNaN,
    console,
    ...extraContext,
  });
  vm.runInContext(code, ctx);
  return ctx;
}

// 1. Worker calcDriver & calcBhagyank
assert.equal(worker.calcBhagyank(28, 11, 1981), 4, 'worker 28 Nov 1981 -> 4');
assert.equal(worker.calcBhagyank(29, 11, 1991), 6, 'worker 29 Nov 1991 -> 6 (never 33)');

// 2. nv_kua.js (used by your-reading.html)
assert.equal(NVKua.digitRoot('28111981'), 4, 'nv_kua 28 Nov 1981 -> 4');
assert.equal(NVKua.digitRoot('29111991'), 6, 'nv_kua 29 Nov 1991 -> 6');

// 3. tools/life-path-calculator.html
{
  const html = readStatic('tools/life-path-calculator.html');
  const m = html.match(/function digitSum[\s\S]*?function reduce\(n\)\s*\{[\s\S]*?\}/);
  assert.ok(m, 'Extracted reduce functions from life-path-calculator.html');
  const ctx = evalSnippet(m[0]);
  const lp1 = ctx.reduceToSingle(ctx.digitSum('28111981'));
  const lp2 = ctx.reduceToSingle(ctx.digitSum('29111991'));
  assert.equal(lp1, 4, 'life-path-calculator 28 Nov 1981 -> 4');
  assert.equal(lp2, 6, 'life-path-calculator 29 Nov 1991 -> 6 (never 33)');
}

// 4. tools/lo-shu-grid.html
{
  const html = readStatic('tools/lo-shu-grid.html');
  const m = html.match(/function reduceToSingle\(num\)\s*\{[\s\S]*?return num;\s*\}/);
  assert.ok(m, 'Extracted reduceToSingle from lo-shu-grid.html');
  const ctx = evalSnippet(m[0]);
  const sumDigits = (s) => s.split('').reduce((a, c) => a + parseInt(c, 10), 0);
  assert.equal(ctx.reduceToSingle(sumDigits('28111981')), 4, 'lo-shu-grid 28 Nov 1981 -> 4');
  assert.equal(ctx.reduceToSingle(sumDigits('29111991')), 6, 'lo-shu-grid 29 Nov 1991 -> 6 (never 33)');
}

// 5. tools/name-numerology.html
{
  const html = readStatic('tools/name-numerology.html');
  const m = html.match(/function digitSum[\s\S]*?function reduce\(n\)\s*\{[\s\S]*?\}/);
  assert.ok(m, 'Extracted reduce from name-numerology.html');
  const ctx = evalSnippet(m[0]);
  assert.equal(ctx.reduce(11), 2, 'name-numerology 11 -> 2');
  assert.equal(ctx.reduce(22), 4, 'name-numerology 22 -> 4');
  assert.equal(ctx.reduce(33), 6, 'name-numerology 33 -> 6');
  assert.equal(ctx.reduce(ctx.digitSum('28111981')), 4, 'name-numerology 28 Nov 1981 -> 4');
  assert.equal(ctx.reduce(ctx.digitSum('29111991')), 6, 'name-numerology 29 Nov 1991 -> 6');
}

// 6. tools/favourable-numbers.html
{
  const html = readStatic('tools/favourable-numbers.html');
  const m = html.match(/function digitSum[\s\S]*?function reduce\(n\)\{[\s\S]*?\}/);
  assert.ok(m, 'Extracted reduceToSingle from favourable-numbers.html');
  const ctx = evalSnippet(m[0]);
  assert.equal(ctx.reduceToSingle(ctx.digitSum('28111981')), 4, 'favourable-numbers 28 Nov 1981 -> 4');
  assert.equal(ctx.reduceToSingle(ctx.digitSum('29111991')), 6, 'favourable-numbers 29 Nov 1991 -> 6');
}

// 7. index.html
{
  const html = readStatic('index.html');
  assert.ok(!html.includes('conductorRaw !== 11'), 'index.html has no master 11 exception');
  assert.ok(!html.includes('conductorRaw !== 33'), 'index.html has no master 33 exception');
  const m = html.match(/function reduceToSingleDigit\(num\)\s*\{[\s\S]*?return num;\s*\}/);
  assert.ok(m, 'Extracted reduceToSingleDigit from index.html');
  const ctx = evalSnippet(m[0]);
  const sumDigits = (s) => s.split('').reduce((a, c) => a + parseInt(c, 10), 0);
  assert.equal(ctx.reduceToSingleDigit(sumDigits('28111981')), 4, 'index.html 28 Nov 1981 -> 4');
  assert.equal(ctx.reduceToSingleDigit(sumDigits('29111991')), 6, 'index.html 29 Nov 1991 -> 6');
}

// 8. pythagorean_calculator.html, property-numerology.html, baby-naming.html, compatibility-calculator.html
for (const [rel, fnName] of [
  ['pythagorean_calculator.html', 'reducePyth'],
  ['tools/property-numerology.html', 'reduceToSingle'],
  ['tools/baby-naming.html', 'reduceToSingle'],
  ['tools/compatibility-calculator.html', 'reduceToSingle'],
]) {
  const html = readStatic(rel);
  const re = new RegExp(`(function digitSum[\\s\\S]*?)?function ${fnName}\\(n\\)\\s*\\{[\\s\\S]*?return[^;]+;\\s*\\}`);
  const m = html.match(re);
  assert.ok(m, `Extracted ${fnName} from ${rel}`);
  const ctx = evalSnippet(m[0]);
  assert.equal(ctx[fnName](31), 4, `${rel} 31 (28 Nov 1981 sum) -> 4`);
  assert.equal(ctx[fnName](33), 6, `${rel} 33 (29 Nov 1991 sum) -> 6`);
  assert.equal(ctx[fnName](22), 4, `${rel} 22 -> 4`);
  assert.equal(ctx[fnName](11), 2, `${rel} 11 -> 2`);
}

console.log('PASS: test_phase2_single_digit_every_page — 28 Nov 1981 -> 4 and 29 Nov 1991 -> 6 on every page.');
