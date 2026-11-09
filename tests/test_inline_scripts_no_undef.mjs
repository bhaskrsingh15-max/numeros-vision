/**
 * Automated Undefined Identifiers & Syntax Verification Suite
 * 
 * Scans every inline script tag across all app/static/*.html files.
 * Enforces:
 * 1. Zero JavaScript syntax errors.
 * 2. Zero undefined identifier / dangling reference errors (ESLint no-undef).
 */

import fs from 'fs';
import path from 'path';
import assert from 'assert';
import { fileURLToPath } from 'url';
import { Linter } from 'eslint';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const staticDir = path.resolve(__dirname, '../app/static');
const linter = new Linter();

const BROWSER_GLOBALS = {
  window: 'readonly',
  document: 'readonly',
  navigator: 'readonly',
  location: 'readonly',
  history: 'readonly',
  localStorage: 'readonly',
  sessionStorage: 'readonly',
  console: 'readonly',
  fetch: 'readonly',
  setTimeout: 'readonly',
  clearTimeout: 'readonly',
  setInterval: 'readonly',
  clearInterval: 'readonly',
  requestAnimationFrame: 'readonly',
  cancelAnimationFrame: 'readonly',
  CustomEvent: 'readonly',
  Event: 'readonly',
  Date: 'readonly',
  Math: 'readonly',
  JSON: 'readonly',
  Array: 'readonly',
  Object: 'readonly',
  String: 'readonly',
  Number: 'readonly',
  Boolean: 'readonly',
  RegExp: 'readonly',
  Map: 'readonly',
  Set: 'readonly',
  Promise: 'readonly',
  Error: 'readonly',
  TypeError: 'readonly',
  RangeError: 'readonly',
  SyntaxError: 'readonly',
  Uint8Array: 'readonly',
  Uint32Array: 'readonly',
  ArrayBuffer: 'readonly',
  TextEncoder: 'readonly',
  TextDecoder: 'readonly',
  btoa: 'readonly',
  atob: 'readonly',
  encodeURIComponent: 'readonly',
  decodeURIComponent: 'readonly',
  parseInt: 'readonly',
  parseFloat: 'readonly',
  isNaN: 'readonly',
  isFinite: 'readonly',
  crypto: 'readonly',
  URL: 'readonly',
  URLSearchParams: 'readonly',
  FormData: 'readonly',
  Blob: 'readonly',
  Headers: 'readonly',
  Request: 'readonly',
  Response: 'readonly',
  Image: 'readonly',
  Audio: 'readonly',
  alert: 'readonly',
  confirm: 'readonly',
  prompt: 'readonly',
  MutationObserver: 'readonly',
  IntersectionObserver: 'readonly',
  ResizeObserver: 'readonly',
  performance: 'readonly',
  screen: 'readonly',
  HTMLElement: 'readonly',
  Element: 'readonly',
  Node: 'readonly',
  NodeList: 'readonly',
  HTMLInputElement: 'readonly',
  EventTarget: 'readonly',
  AbortController: 'readonly',
  // Vendor SDK globals expected on window:
  Razorpay: 'readonly',
  turnstile: 'readonly',
  google: 'readonly',
  dataLayer: 'readonly',
  gtag: 'readonly',
  jspdf: 'readonly',
  jsPDF: 'readonly',
  html2canvas: 'readonly',
  NV_TURNSTILE_SITE_KEY: 'readonly',
  NV_TURNSTILE_TOKEN: 'readonly'
};

const htmlFiles = fs.readdirSync(staticDir).filter(f => f.endsWith('.html'));
assert(htmlFiles.length >= 30, `Expected at least 30 HTML files in app/static, found ${htmlFiles.length}`);

let totalErrors = 0;
const errorsByFile = {};

for (const file of htmlFiles) {
  const filePath = path.join(staticDir, file);
  const content = fs.readFileSync(filePath, 'utf8');
  const scriptRegex = /<script\b(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi;
  let match;
  let scriptIdx = 0;

  const scripts = [];
  while ((match = scriptRegex.exec(content)) !== null) {
    const attrs = match[1];
    const code = match[2];
    if (/type\s*=\s*["']application\/ld\+json["']/i.test(attrs)) continue;
    if (!code.trim()) continue;
    scripts.push(code);
  }

  const documentGlobals = { ...BROWSER_GLOBALS };
  for (const code of scripts) {
    const declRegex = /(?:function\s+([a-zA-Z0-9_$]+)|var\s+([a-zA-Z0-9_$]+))/g;
    let m;
    while ((m = declRegex.exec(code)) !== null) {
      const name = m[1] || m[2];
      if (name) documentGlobals[name] = 'writable';
    }
  }

  for (const code of scripts) {
    scriptIdx++;
    const messages = linter.verify(code, {
      rules: {
        'no-undef': 'error'
      },
      languageOptions: {
        ecmaVersion: 'latest',
        sourceType: 'script',
        globals: documentGlobals
      }
    });

    if (messages.length > 0) {
      errorsByFile[file] = errorsByFile[file] || [];
      for (const m of messages) {
        errorsByFile[file].push({
          scriptIdx,
          line: m.line,
          column: m.column,
          message: m.message,
          ruleId: m.ruleId
        });
        totalErrors++;
      }
    }
  }
}

if (totalErrors > 0) {
  console.error('FAIL: Undefined identifiers / syntax errors found in HTML scripts:', JSON.stringify(errorsByFile, null, 2));
  process.exit(1);
}

console.log(`PASS: test_inline_scripts_no_undef — ${htmlFiles.length} HTML files verified with 0 syntax or undefined-identifier errors.`);
