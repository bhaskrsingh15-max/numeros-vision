const { spawn } = require('child_process');
const http = require('http');

const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--headless=new',
  '--remote-debugging-port=9222',
  '--disable-gpu',
  '--no-sandbox',
  'http://127.0.0.1:8000/sample?format=master'
]);

setTimeout(async () => {
  try {
    const listRes = await fetch('http://127.0.0.1:9222/json');
    const pages = await listRes.json();
    const wsUrl = pages[0]?.webSocketDebuggerUrl;
    console.log('Chrome debugging active, WS:', wsUrl ? 'OK' : 'FAIL');
  } catch (err) {
    console.error('CDP connect error:', err.message);
  } finally {
    chrome.kill();
  }
}, 2000);
