import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

function getHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getHtmlFiles(fullPath));
    } else if (file.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

const ampDir = path.resolve('app/static/amp');
const ampFiles = getHtmlFiles(ampDir);

console.log(`Auditing ${ampFiles.length} AMP files for zero tracking...`);
assert.equal(ampFiles.length, 25, `Expected exactly 25 AMP files, found ${ampFiles.length}`);

const forbiddenPatterns = [
  'amp-analytics',
  'GTM-5N2QCMZS',
  'G-3Z2E6416W7',
  'google-analytics.com',
  'googletagmanager.com'
];

let errors = 0;
for (const file of ampFiles) {
  const content = fs.readFileSync(file, 'utf-8');
  for (const pattern of forbiddenPatterns) {
    if (content.includes(pattern)) {
      console.error(`FAIL: ${file} contains forbidden tracking string: "${pattern}"`);
      errors++;
    }
  }
}

if (errors === 0) {
  console.log(`PASS: All 25 AMP files have 0 tracking scripts, 0 amp-analytics, 0 GTM, 0 GA4.`);
  process.exit(0);
} else {
  console.error(`FAILED with ${errors} violations across AMP files.`);
  process.exit(1);
}
