const { spawn } = require('child_process');

const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--headless=new',
  '--remote-debugging-port=9225',
  '--disable-gpu',
  '--window-size=1400,1200',
  'http://127.0.0.1:8000/sample?format=master'
]);

setTimeout(async () => {
  try {
    const list = await (await fetch('http://127.0.0.1:9225/json')).json();
    console.log('Pages in chrome:', list.map(p => ({ title: p.title, url: p.url })));
    const target = list.find(p => p.type === 'page') || list[0];
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: {
          expression: `
            ({
              title: document.title,
              stageExists: !!document.getElementById('pagesStage'),
              pageCount: document.querySelectorAll('.pdf-page').length,
              page12: !!document.getElementById('page-12'),
              page12ScrollH: document.getElementById('page-12')?.scrollHeight,
              page12ClientH: document.getElementById('page-12')?.clientHeight
            })
          `,
          returnByValue: true
        }
      }));
    };
    ws.onmessage = (m) => {
      console.log('Eval result:', JSON.parse(m.data)?.result?.result?.value);
      chrome.kill();
    };
  } catch (e) {
    console.error('Error:', e.message);
    chrome.kill();
  }
}, 3000);
