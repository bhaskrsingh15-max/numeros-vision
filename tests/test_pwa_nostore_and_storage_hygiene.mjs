import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import workerModule from '../dist_cloudflare_pages/_worker.js';

console.log('--- STARTING PWA NO-STORE & STORAGE HYGIENE TESTS ---');

// Test 1: Worker returns private, no-store, must-revalidate on /api/* and /dashboard
async function testNoStoreHeaders() {
  const env = {
    DB: {
      prepare: () => ({
        bind: () => ({
          first: async () => null,
          all: async () => ({ results: [] }),
          run: async () => ({ success: true })
        })
      })
    },
    ASSETS: {
      fetch: async (req) => new Response('<html><body>Dashboard</body></html>', { status: 200, headers: { 'Content-Type': 'text/html' } })
    }
  };

  // 1a. /dashboard
  const dashReq = new Request('https://numeros.vision/dashboard', { method: 'GET' });
  const dashRes = await workerModule.fetch(dashReq, env, {});
  const dashCc = dashRes.headers.get('Cache-Control');
  assert(dashCc && dashCc.includes('no-store'), `Expected /dashboard Cache-Control to include no-store, got: ${dashCc}`);
  console.log('✓ PASS: /dashboard returns Cache-Control:', dashCc);

  // 1b. /api/v1/auth/session/verify
  const apiReq = new Request('https://numeros.vision/api/v1/auth/session/verify', { method: 'GET' });
  const apiRes = await workerModule.fetch(apiReq, env, {});
  const apiCc = apiRes.headers.get('Cache-Control');
  assert(apiCc && apiCc.includes('no-store'), `Expected /api/* Cache-Control to include no-store, got: ${apiCc}`);
  console.log('✓ PASS: /api/* returns Cache-Control:', apiCc);
}

// Test 2: Verify iosBridge is completely removed from marketing-analytics.js
function testIosBridgeRemoved() {
  const analyticsPath = path.resolve('dist_cloudflare_pages/js/marketing-analytics.js');
  const content = fs.readFileSync(analyticsPath, 'utf8');
  assert(!content.includes('iosBridge'), 'Error: iosBridge found in marketing-analytics.js');
  console.log('✓ PASS: iosBridge is completely removed from marketing-analytics.js');
}

// Test 3: Verify zero localStorage.setItem writes for nv_user_* in dist HTML files
function testZeroUserStorageWrites() {
  const distDir = path.resolve('dist_cloudflare_pages');
  const files = fs.readdirSync(distDir).filter(f => f.endsWith('.html'));
  for (const file of files) {
    const content = fs.readFileSync(path.join(distDir, file), 'utf8');
    assert(!/localStorage\.setItem\(\s*['"]nv_user_[a-zA-Z0-9_]+['"]/.test(content), `Found nv_user_* localStorage.setItem in ${file}`);
    assert(!/localStorage\.setItem\(\s*['"]nv_user_invoices['"]/.test(content), `Found nv_user_invoices localStorage.setItem in ${file}`);
    assert(!/localStorage\.setItem\(\s*['"]nv_family_profiles['"]/.test(content), `Found nv_family_profiles localStorage.setItem in ${file}`);
  }
  console.log('✓ PASS: Zero localStorage.setItem writes for nv_user_*, invoices, or family in all HTML pages');
}

// Test 4: One-time migration exists in nv_consent.js
function testMigrationExists() {
  const consentPath = path.resolve('dist_cloudflare_pages/js/nv_consent.js');
  const content = fs.readFileSync(consentPath, 'utf8');
  assert(content.includes('runOneTimeLegacyStorageMigration'), 'Error: runOneTimeLegacyStorageMigration missing from nv_consent.js');
  assert(content.includes('nv_storage_migrated_v5'), 'Error: MIGRATION_FLAG missing from nv_consent.js');
  console.log('✓ PASS: One-time migration routine present in nv_consent.js');
}

async function run() {
  await testNoStoreHeaders();
  testIosBridgeRemoved();
  testZeroUserStorageWrites();
  testMigrationExists();
  console.log('--- ALL PWA NO-STORE & STORAGE HYGIENE TESTS PASSED ---');
}

run().catch(err => {
  console.error('Test failure:', err);
  process.exit(1);
});
