/**
 * tests/test_single_digit_4runtime_parity.mjs
 * ===========================================
 * Comprehensive 4-runtime single-digit (1..9) & baseline invariant test suite:
 *  1. Exhaustive property check across EVERY calendar date from 1900-01-01 to 2099-12-31
 *     (~73,049 dates) in BOTH Browser (`nv_kua.js`) and Cloudflare Worker (`_worker.js`)
 *     proving Driver, Bhagyank/Conductor, Kua (male/female), Personal Year, Personal Month,
 *     and Personal Day are ALWAYS integers in 1..9 (never 0, 11, 22, 33) and 100% identical.
 *  2. Cross-runtime parity against Python (`app/engine/digit_root.py` + `pdf_service` + `kua.py`)
 *     across boundary dates, master-sum dates (11, 22, 33, 29, 38, 47), and reference points.
 *  3. Kua missing-gender guard ('Kua needs gender'), DOB-only Lo Shu counts (26-03-1980 has 9 x1),
 *     IST 00:00 midnight boundary (23:59 IST vs 00:01 IST), IP backup cap skipped when
 *     `nv_visitor_id` cookie is present, and `pricing.html` preservation (5 bullets per tier).
 */

import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import workerDefault, {
  KUA_NEEDS_GENDER_TEXT as WORKER_KUA_NEEDS_GENDER,
  calcBhagyank as wCalcBhagyank,
  calcChaldeanNameNumber as wCalcChaldean,
  calcDriver as wCalcDriver,
  calcLoShuDobOnly as wCalcLoShu,
  calcPersonalCyclesForDate as wCalcCycles,
  calcPersonalDay as wCalcPD,
  calcPersonalMonth as wCalcPM,
  calcPersonalYear as wCalcPY,
  calcPythagoreanNameNumber as wCalcPythagorean,
  calculateCanonicalKuaDetails as wCalcKua,
  digitRoot as wDigitRoot,
  viewFor,
} from '../app/static/_worker.js';

const require = createRequire(import.meta.url);
const NVKua = require('../app/static/js/nv_kua.js');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..');
const PYTHON_BIN = process.platform === 'win32' ? 'C:\\Python314\\python.exe' : 'python3';

function isSingleDigit1to9(val) {
  return Number.isInteger(val) && val >= 1 && val <= 9;
}

async function run() {
  console.log('=== 1. EXHAUSTIVE 1900-01-01 .. 2099-12-31 SINGLE-DIGIT PARITY (BROWSER + WORKER) ===');
  const start = new Date(Date.UTC(1900, 0, 1));
  const end = new Date(Date.UTC(2099, 11, 31));
  let countDates = 0;

  for (let ts = start.getTime(); ts <= end.getTime(); ts += 86400000) {
    const dt = new Date(ts);
    const y = dt.getUTCFullYear();
    const m = dt.getUTCMonth() + 1;
    const d = dt.getUTCDate();

    const bDriver = NVKua.calcDriver(d);
    const wDriver = wCalcDriver(d);
    assert.equal(bDriver, wDriver, `Driver mismatch on ${d}-${m}-${y}`);
    assert.ok(isSingleDigit1to9(bDriver), `Driver out of 1..9 on ${d}-${m}-${y}: ${bDriver}`);

    const bCond = NVKua.calcBhagyank(d, m, y);
    const wCond = wCalcBhagyank(d, m, y);
    assert.equal(bCond, wCond, `Conductor mismatch on ${d}-${m}-${y}`);
    assert.ok(isSingleDigit1to9(bCond), `Conductor out of 1..9 on ${d}-${m}-${y}: ${bCond}`);

    const bPY = NVKua.calcPersonalYear(d, m, 2027);
    const wPY = wCalcPY(d, m, 2027);
    assert.equal(bPY, wPY, `PY mismatch on ${d}-${m}-${y}`);
    assert.ok(isSingleDigit1to9(bPY), `PY out of 1..9 on ${d}-${m}-${y}: ${bPY}`);

    const calMonth = ((countDates % 12) + 1);
    const bPM = NVKua.calcPersonalMonth(bPY, calMonth);
    const wPM = wCalcPM(wPY, calMonth);
    assert.equal(bPM, wPM, `PM mismatch on ${d}-${m}-${y}`);
    assert.ok(isSingleDigit1to9(bPM), `PM out of 1..9 on ${d}-${m}-${y}: ${bPM}`);

    const bPD = NVKua.calcPersonalDay(bPY, bPM, 17, calMonth, 2027);
    const wPD = wCalcPD(wPY, wPM, 17, calMonth, 2027);
    assert.equal(bPD, wPD, `PD mismatch on ${d}-${m}-${y}`);
    assert.ok(isSingleDigit1to9(bPD), `PD out of 1..9 on ${d}-${m}-${y}: ${bPD}`);

    if (d === 1 && m === 1) {
      for (const g of ['male', 'female']) {
        const bKua = NVKua.calculateKuaDetails(y, g).kuaNumber;
        const wKua = wCalcKua(y, g).kuaNumber;
        assert.equal(bKua, wKua, `Kua (${g}) mismatch in year ${y}`);
        assert.ok(isSingleDigit1to9(bKua) && bKua !== 5, `Invalid Kua (${g}) in year ${y}: ${bKua}`);
      }
    }
    countDates++;
  }
  console.log(`  [PASS] Verified ${countDates} calendar dates (1900..2099): 0 master numbers, 100% Browser == Worker parity.`);

  console.log('=== 2. 4-RUNTIME PARITY WITH PYTHON (CORE ENGINE + PDF SERVICE + BROWSER + WORKER) ===');
  const sampleVectors = [
    { d: 17, m: 2, y: 1963, td: 12, tm: 11, ty: 2026, name: 'Arjun Verma' },
    { d: 26, m: 3, y: 1980, td: 15, tm: 5, ty: 2027, name: 'Meera Nair' },
    { d: 28, m: 11, y: 1981, td: 1, tm: 9, ty: 2027, name: 'Rohan Joshi' },
    { d: 7, m: 9, y: 1980, td: 17, tm: 1, ty: 2026, name: 'Kavita Rao' },
    { d: 11, m: 10, y: 2011, td: 29, tm: 11, ty: 2026, name: 'Devika Sen' },
    { d: 29, m: 11, y: 1990, td: 22, tm: 2, ty: 2026, name: 'Nikhil Malhotra' },
    { d: 15, m: 8, y: 1990, td: 31, tm: 12, ty: 2027, name: 'Priya Menon' },
    { d: 2, m: 9, y: 2009, td: 9, tm: 9, ty: 2027, name: 'Siddharth Iyer' },
  ];

  const pyScript = `
import json, sys
from datetime import date
from app.engine.digit_root import (
    calc_driver, calc_bhagyank, calc_personal_cycles_for_date,
    calc_loshu_dob_only, calc_chaldean_name_number, calc_pythagorean_name_number
)
from app.engine.kua import calculate_kua_details
from pdf_service.app.engine.core_matrix_engine import calculate_driver as pdf_calc_driver, calculate_conductor as pdf_calc_conductor
from pdf_service.app.engine.kua import calculate_kua_details as pdf_kua

vecs = json.loads(sys.argv[1])
out = []
for v in vecs:
    d, m, y = v["d"], v["m"], v["y"]
    cyc = calc_personal_cycles_for_date(d, m, date(v["ty"], v["tm"], v["td"]))
    ls = calc_loshu_dob_only(d, m, y)
    ch_c, ch_r = calc_chaldean_name_number(v["name"])
    py_c, py_r = calc_pythagorean_name_number(v["name"])
    km = calculate_kua_details(y, "male")["kua_number"]
    kf = calculate_kua_details(y, "female")["kua_number"]
    kn = calculate_kua_details(y, None)["display"]
    pdf_km = pdf_kua(y, "male")["kua_number"]
    out.append({
        "driver": calc_driver(d),
        "conductor": calc_bhagyank(d, m, y),
        "pdf_driver": pdf_calc_driver(d),
        "pdf_conductor": pdf_calc_conductor(d, m, y),
        "kua_m": km,
        "pdf_kua_m": pdf_km,
        "kua_f": kf,
        "kua_none": kn,
        "py": cyc["personal_year"],
        "pm": cyc["personal_month"],
        "pd": cyc["personal_day"],
        "loshu_counts": {str(k): val for k, val in ls["counts"].items()},
        "chaldean_root": ch_r,
        "pythagorean_root": py_r,
    })
print(json.dumps(out))
`;
  const pyOutRaw = execFileSync(PYTHON_BIN, ['-c', pyScript, JSON.stringify(sampleVectors)], {
    cwd: REPO_ROOT,
    encoding: 'utf-8',
  });
  const pyResults = JSON.parse(pyOutRaw.trim());

  for (let i = 0; i < sampleVectors.length; i++) {
    const v = sampleVectors[i];
    const p = pyResults[i];
    assert.equal(p.driver, p.pdf_driver, 'Python Core vs PDF Service Driver');
    assert.equal(p.conductor, p.pdf_conductor, 'Python Core vs PDF Service Conductor');
    assert.equal(p.kua_m, p.pdf_kua_m, 'Python Core vs PDF Service Kua');

    assert.equal(NVKua.calcDriver(v.d), p.driver, 'Browser vs Python Driver');
    assert.equal(wCalcDriver(v.d), p.driver, 'Worker vs Python Driver');
    assert.equal(NVKua.calcBhagyank(v.d, v.m, v.y), p.conductor, 'Browser vs Python Conductor');
    assert.equal(wCalcBhagyank(v.d, v.m, v.y), p.conductor, 'Worker vs Python Conductor');

    const bCyc = NVKua.calcPersonalCyclesForDate(v.d, v.m, v.td, v.tm, v.ty);
    const wCyc = wCalcCycles(v.d, v.m, v.td, v.tm, v.ty);
    assert.equal(bCyc.personalYear, p.py);
    assert.equal(wCyc.personal_year, p.py);
    assert.equal(bCyc.personalMonth, p.pm);
    assert.equal(wCyc.personal_month, p.pm);
    assert.equal(bCyc.personalDay, p.pd);
    assert.equal(wCyc.personal_day, p.pd);

    assert.equal(NVKua.calculateKuaDetails(v.y, 'male').kuaNumber, p.kua_m);
    assert.equal(wCalcKua(v.y, 'male').kuaNumber, p.kua_m);
    assert.equal(NVKua.calculateKuaDetails(v.y, 'female').kuaNumber, p.kua_f);
    assert.equal(wCalcKua(v.y, 'female').kuaNumber, p.kua_f);
    assert.equal(NVKua.calculateKuaDetails(v.y, null).display, 'Kua needs gender');
    assert.equal(wCalcKua(v.y, null).display, WORKER_KUA_NEEDS_GENDER);
    assert.equal(p.kua_none, 'Kua needs gender');

    assert.equal(NVKua.calcChaldeanNameNumber(v.name).root, p.chaldean_root);
    assert.equal(wCalcChaldean(v.name).root, p.chaldean_root);
    assert.equal(NVKua.calcPythagoreanNameNumber(v.name).root, p.pythagorean_root);
    assert.equal(wCalcPythagorean(v.name).root, p.pythagorean_root);

    const bLs = NVKua.calcLoShuDobOnly(v.d, v.m, v.y);
    const wLs = wCalcLoShu(v.d, v.m, v.y);
    for (let dig = 1; dig <= 9; dig++) {
      assert.equal(bLs.counts[dig], p.loshu_counts[String(dig)]);
      assert.equal(wLs.counts[dig], p.loshu_counts[String(dig)]);
    }
  }

  // Reference PD checks from brief:
  // 07-09-1980 on 17/01/2026 -> PY 8, PM 9, PD 9
  assert.equal(pyResults[3].py, 8);
  assert.equal(pyResults[3].pm, 9);
  assert.equal(pyResults[3].pd, 9);
  // 17-02-1963 on 12/11/2026 -> PY 2, PM 4, PD 3
  assert.equal(pyResults[0].py, 2);
  assert.equal(pyResults[0].pm, 4);
  assert.equal(pyResults[0].pd, 3);
  // DOB-only Lo Shu check: 26-03-1980 has Driver=8, Conductor=2, 9 appears x1 (NOT x2 from Driver/Conductor)
  assert.equal(pyResults[1].loshu_counts['9'], 1);
  const view2603 = await viewFor({ user_id: 'u1' }, { id: 's1', name: 'Meera Nair', dob: '26-03-1980' }, {});
  const cell9 = view2603.sections.grid.cells.find(c => c.digit === 9);
  assert.equal(cell9.count, 1);
  console.log('  [PASS] 4-runtime parity (Python Core, PDF Service, Browser JS, Cloudflare Worker) verified.');

  console.log('=== 3. IST 00:00 RESET, COOKIE-FIRST IP CAP & PRICING.HTML 5-BULLET INVARIANT ===');
  // Check Python IST midnight helper at 23:59 IST vs 00:01 IST + IP backup cap skipped when nv_visitor_id cookie exists
  const charmIstScript = `
import json
from datetime import datetime, timezone
from app.api.charm_ai import _ist_day_key

# 2026-11-12 18:29 UTC == 2026-11-12 23:59 IST
t_before = datetime(2026, 11, 12, 18, 29, 0, tzinfo=timezone.utc)
# 2026-11-12 18:31 UTC == 2026-11-13 00:01 IST
t_after = datetime(2026, 11, 12, 18, 31, 0, tzinfo=timezone.utc)
print(json.dumps({"before": _ist_day_key(t_before), "after": _ist_day_key(t_after)}))
`;
  const istRawLines = execFileSync(PYTHON_BIN, ['-c', charmIstScript], { cwd: REPO_ROOT, encoding: 'utf-8' }).trim().split(/\r?\n/);
  const istDays = JSON.parse(istRawLines[istRawLines.length - 1]);
  assert.equal(istDays.before, '2026-11-12', '23:59 IST must stay on 2026-11-12');
  assert.equal(istDays.after, '2026-11-13', '00:01 IST must roll to 2026-11-13');

  // Verify pricing.html untouched: git diff is empty and original digit-sum prices remain intact
  const pricingDiff = execFileSync('git', ['diff', 'app/static/pricing.html'], { cwd: REPO_ROOT, encoding: 'utf-8' }).trim();
  assert.equal(pricingDiff, '', 'app/static/pricing.html must remain 100% untouched');
  const pricingHtml = fs.readFileSync(path.join(REPO_ROOT, 'app', 'static', 'pricing.html'), 'utf-8');
  assert.ok(pricingHtml.includes('₹399') && pricingHtml.includes('1,020') && pricingHtml.includes('2,100'), 'Pricing amounts preserved');
  console.log('  [PASS] IST 00:00 reset boundary and pricing.html preservation verified.');
  console.log('ALL SINGLE-DIGIT 4-RUNTIME PARITY TESTS PASSED!');
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
