/**
 * Test Suite: CSRF Origin Verification in _worker.js
 * Verifies strict adherence to Directive 1:
 * - Origin http://x.numeros-vision.pages.dev rejected
 * - https://other-project.pages.dev rejected
 * - https://evil.example rejected
 * - Same-origin preview request accepted
 * - Production domains accepted
 * - Missing Origin accepted
 */

import fs from 'fs';
import assert from 'assert';

console.log('--- STARTING CSRF ORIGIN VALIDATION TEST SUITE ---');

const workerCode = fs.readFileSync('app/static/_worker.js', 'utf-8');

// Extract verifyOrigin function definition
const match = workerCode.match(/function verifyOrigin\(request,\s*env\)[\s\S]*?\n\}/);
assert.ok(match, 'verifyOrigin function must exist in _worker.js');

const verifyOriginFn = new Function('request', 'env', `
  ${match[0]}
  return verifyOrigin(request, env);
`);

function createMockRequest(url, originHeader) {
  return {
    url: url,
    headers: {
      get: (headerName) => {
        if (headerName.toLowerCase() === 'origin') return originHeader;
        return null;
      }
    }
  };
}

const mockEnv = {};

// Test 1: Cross-origin HTTP subdomains on pages.dev rejected
console.log('\n[Test 1] Testing HTTP subdomain on pages.dev...');
{
  const req = createMockRequest('https://preview.numeros-vision.pages.dev/api/v1/payments/create-order', 'http://x.numeros-vision.pages.dev');
  const allowed = verifyOriginFn(req, mockEnv);
  assert.strictEqual(allowed, false, 'http://x.numeros-vision.pages.dev must be rejected');
  console.log('✔ PASS: Insecure HTTP subdomain rejected.');
}

// Test 2: Other project on pages.dev rejected
console.log('\n[Test 2] Testing other-project.pages.dev...');
{
  const req = createMockRequest('https://preview.numeros-vision.pages.dev/api/v1/payments/create-order', 'https://other-project.pages.dev');
  const allowed = verifyOriginFn(req, mockEnv);
  assert.strictEqual(allowed, false, 'https://other-project.pages.dev must be rejected');
  console.log('✔ PASS: Unrelated Cloudflare Pages project rejected.');
}

// Test 3: Evil cross-origin site rejected
console.log('\n[Test 3] Testing arbitrary cross-origin site...');
{
  const req = createMockRequest('https://numerosvision.com/api/v1/payments/create-order', 'https://evil.example');
  const allowed = verifyOriginFn(req, mockEnv);
  assert.strictEqual(allowed, false, 'https://evil.example must be rejected');
  console.log('✔ PASS: Arbitrary malicious origin rejected.');
}

// Test 4: Same-origin preview request accepted
console.log('\n[Test 4] Testing same-origin request on preview deployment...');
{
  const req = createMockRequest('https://preview.numeros-vision.pages.dev/api/v1/payments/create-order', 'https://preview.numeros-vision.pages.dev');
  const allowed = verifyOriginFn(req, mockEnv);
  assert.strictEqual(allowed, true, 'Same-origin preview request must be accepted');
  console.log('✔ PASS: Same-origin preview request accepted.');
}

// Test 5: Production canonical domains accepted
console.log('\n[Test 5] Testing production domains...');
{
  const req1 = createMockRequest('https://numerosvision.com/api/v1/payments/create-order', 'https://numerosvision.com');
  assert.strictEqual(verifyOriginFn(req1, mockEnv), true, 'https://numerosvision.com must be accepted');

  const req2 = createMockRequest('https://numerosvision.com/api/v1/payments/create-order', 'https://www.numerosvision.com');
  assert.strictEqual(verifyOriginFn(req2, mockEnv), true, 'https://www.numerosvision.com must be accepted');
  console.log('✔ PASS: Production domains (apex and www) accepted.');
}

// Test 6: Missing Origin header accepted (standard browser same-origin navigations/scripts)
console.log('\n[Test 6] Testing missing Origin header...');
{
  const req = createMockRequest('https://numerosvision.com/api/v1/payments/create-order', null);
  assert.strictEqual(verifyOriginFn(req, mockEnv), true, 'Missing origin must return true');
  console.log('✔ PASS: Missing Origin header returns true.');
}

// Test 7: Confirm NO wildcard or regex for *.pages.dev exists in verifyOrigin
console.log('\n[Test 7] Verifying wildcard deletion from codebase...');
{
  assert.ok(!match[0].includes('.endsWith(\'.numeros-vision.pages.dev\')'), 'Wildcard endsWith for pages.dev must be deleted from verifyOrigin');
  assert.ok(!match[0].includes('env.ENVIRONMENT'), 'ENVIRONMENT-based bypass must not exist in verifyOrigin');
  console.log('✔ PASS: Wildcard and environment allowances completely removed from verifyOrigin.');
}

console.log('\n--- ALL CSRF ORIGIN VALIDATION TESTS PASSED (100%) ---');
