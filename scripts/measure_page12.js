const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('app/static/sample.html', 'utf8');
const lastScriptStart = html.lastIndexOf('<script>');
const lastScriptEnd = html.lastIndexOf('</script>');
const code = html.substring(lastScriptStart + 8, lastScriptEnd);

const makeEl = (id = '') => ({
  id, value: '', textContent: '', innerHTML: '', style: {},
  classList: { toggle: () => {}, add: () => {}, remove: () => {} },
  appendChild: () => {}, scrollIntoView: () => {}
});

const dom = {
  document: {
    readyState: 'complete',
    getElementById: (id) => makeEl(id),
    querySelectorAll: () => [],
    createElement: () => makeEl(),
    addEventListener: () => {}
  },
  window: { addEventListener: () => {}, location: { search: '' } },
  console: console
};

const ctx = vm.createContext(dom);
vm.runInContext(code, ctx);

const client = {
  name: 'Ankur Sachdeva',
  dob: '1984-06-18',
  gender: 'male',
  phone: '9876543210'
};

const f2 = ctx.generateFormat2Pages(client);
const f3 = ctx.generateFormat3Pages(client);

console.log('=== FORMAT 2 PAGE 12 ===');
console.log(f2[11]);

console.log('\n=== FORMAT 3 PAGE 12 ===');
console.log(f3[11]);
