const fs = require('fs');
const html = fs.readFileSync('app/static/sample.html', 'utf8');

function showPage(pageId) {
  const start = html.indexOf(`id="${pageId}"`);
  if (start === -1) return console.log(`Page ${pageId} not found`);
  const pageStart = html.lastIndexOf('<div class="pdf-page"', start);
  const nextDiv = html.indexOf('<div class="pdf-page"', start + 10);
  const pageEnd = nextDiv !== -1 ? nextDiv : html.indexOf('return pages', start);
  console.log(`\n================== ${pageId} ==================`);
  console.log(html.substring(pageStart, pageStart + 1200));
}

showPage('page-2'); // Format 3 or 1
showPage('page-18');
