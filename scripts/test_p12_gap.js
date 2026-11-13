const { spawn } = require('child_process');

async function testPage12Variations() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9234',
    '--disable-gpu',
    '--window-size=1400,1200',
    'http://127.0.0.1:8000/sample?format=master'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const list = await (await fetch('http://127.0.0.1:9234/json')).json();
    const target = list.find(p => p.url.includes('http://127.0.0.1:8000'));
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: {
          expression: `
            (() => {
              const p12 = document.getElementById('page-12');
              const fRect = p12.querySelector('.page-footer').getBoundingClientRect();
              const c = p12.querySelector('.page-content');
              const lastChild = c.children[c.children.length - 1];
              const lastRect = lastChild.getBoundingClientRect();
              return {
                pageHeight: p12.getBoundingClientRect().height,
                footerTop: fRect.top,
                lastChildBottom: lastRect.bottom,
                gapToFooter: Math.round(fRect.top - lastRect.bottom)
              };
            })()
          `,
          returnByValue: true
        }
      }));
    };

    ws.onmessage = (m) => {
      console.log('Current P12 result:', JSON.stringify(JSON.parse(m.data)?.result?.result?.value, null, 2));
      ws.close();
      chrome.kill();
    };
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}

testPage12Variations();
