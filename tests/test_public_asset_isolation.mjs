import assert from 'node:assert/strict';
import worker from '../app/static/_worker.js';

console.log('Running HTTP-level public asset isolation test suite...');

const mockEnv = {
  ASSETS: {
    async fetch(req) {
      return new Response('Mock Asset Found', { status: 200 });
    }
  },
  ENVIRONMENT: 'production',
  PRIMARY_DOMAIN: 'https://numerosvision.com'
};

const mockCtx = {
  waitUntil() {}
};

const forbiddenPaths = [
  '/data/panchang_2027_delhi.json',
  '/app/engine/',
  '/app/engine/calculator.py',
  '/planner_2027_engine.py',
  '/pdf_service/',
  '/pdf_service/generator.py',
  '/.env',
  '/.git/config',
  '/scripts/gen_panchang_2027.py',
  '/_worker.js'
];

for (const path of forbiddenPaths) {
  const req = new Request(`https://numerosvision.com${path}`, {
    method: 'GET'
  });
  const res = await worker.fetch(req, mockEnv, mockCtx);
  assert.equal(
    res.status,
    404,
    `Expected status 404 for forbidden path ${path}, got ${res.status}`
  );
  console.log(`PASS: ${path} returned HTTP ${res.status}`);
}

// Ensure legitimate paths are allowed through to env.ASSETS
const legitimatePaths = [
  '/',
  '/pricing.html',
  '/index.html',
  '/static/css/theme.css',
  '/how_we_work.html'
];

for (const path of legitimatePaths) {
  const req = new Request(`https://numerosvision.com${path}`, {
    method: 'GET'
  });
  const res = await worker.fetch(req, mockEnv, mockCtx);
  assert.equal(
    res.status,
    200,
    `Expected status 200 for legitimate path ${path}, got ${res.status}`
  );
  console.log(`PASS: Legitimate path ${path} allowed through (HTTP ${res.status})`);
}

console.log('\nAll public asset isolation tests passed successfully.');
