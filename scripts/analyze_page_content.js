const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('app/static/sample.html', 'utf8');

// Extract script
const lastScriptStart = html.lastIndexOf('<script>');
const lastScriptEnd = html.lastIndexOf('</script>');
const code = html.substring(lastScriptStart + 8, lastScriptEnd);

// Mock DOM
const makeEl = (id = '') => ({
  id,
  value: '',
  textContent: '',
  innerHTML: '',
  style: {},
  classList: { toggle: () => {}, add: () => {}, remove: () => {} },
  appendChild: () => {},
  scrollIntoView: () => {}
});

const dom = {
  document: {
    readyState: 'complete',
    getElementById: (id) => makeEl(id),
    querySelectorAll: () => [],
    createElement: (tag) => makeEl(),
    addEventListener: () => {}
  },
  window: { addEventListener: () => {}, location: { search: '' } },
  console: console
};

const ctx = vm.createContext(dom);
vm.runInContext(code, ctx);

const client = {
  name: 'Alexander Vance',
  dob: '1990-10-18',
  gender: 'male',
  phone: '9876543210'
};

const f1 = ctx.generateFormat1Pages(client);
const f2 = ctx.generateFormat2Pages(client);
const f3 = ctx.generateFormat3Pages(client);

function analyzePages(formatName, pages) {
  console.log(`\n=================== ${formatName} (${pages.length} Pages) ===================`);
  pages.forEach((pageHtml, idx) => {
    const pageNum = idx + 1;
    // Count characters, cards, paragraphs, headings
    const charLen = pageHtml.length;
    const cardMatches = (pageHtml.match(/class=["'][^"']*report-card[^"']*["']/g) || []).length;
    const pMatches = (pageHtml.match(/<p[\s\S]*?<\/p>/g) || []).length;
    const tableMatches = (pageHtml.match(/<table[\s\S]*?<\/table>/g) || []).length;
    
    // Check if page has header and footer
    const hasHeader = pageHtml.includes('page-header');
    const hasFooter = pageHtml.includes('page-footer');

    // Extract title
    const titleMatch = pageHtml.match(/class=["']chapter-hero-title["']>([^<]+)<\/div>/) ||
                       pageHtml.match(/class=["']cover-title["']>([^<]+)<\/div>/) ||
                       pageHtml.match(/<h[1-3][^>]*>([^<]+)<\/h[1-3]>/);
    const title = titleMatch ? titleMatch[1].trim() : (pageNum === 1 ? 'Cover Page' : 'Content Page');

    console.log(`P${pageNum.toString().padStart(2, ' ')} | Len: ${charLen.toString().padStart(5, ' ')} | Cards: ${cardMatches} | P: ${pMatches.toString().padStart(2, ' ')} | Tables: ${tableMatches} | Header: ${hasHeader ? 'YES' : 'NO '} | Footer: ${hasFooter ? 'YES' : 'NO '} | ${title}`);
  });
}

analyzePages('FORMAT 1: EXECUTIVE BRIEF', f1);
analyzePages('FORMAT 2: MASTER DOSSIER', f2);
analyzePages('FORMAT 3: SOVEREIGN ROADMAP', f3);
