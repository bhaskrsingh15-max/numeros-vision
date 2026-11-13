const { spawn } = require('child_process');

async function testBrief() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9233',
    '--disable-gpu',
    '--window-size=1400,1200',
    'http://127.0.0.1:8000/sample?format=brief'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const list = await (await fetch('http://127.0.0.1:9233/json')).json();
    const target = list.find(p => p.url.includes('http://127.0.0.1:8000'));
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: {
          expression: `
            (() => {
              const p1 = document.getElementById('page-1');
              const header = p1.querySelector('.page-header');
              const footer = p1.querySelector('.page-footer');
              const content = p1.querySelector('.page-content');
              const fRect = footer.getBoundingClientRect();
              
              const children = Array.from(content.children).map(c => {
                const r = c.getBoundingClientRect();
                return {
                  tag: c.tagName,
                  class: c.className,
                  height: Math.round(r.height),
                  gapToFooter: Math.round(fRect.top - r.bottom),
                  text: c.innerText.substring(0, 45).replace(/\\n/g, ' ')
                };
              });

              return {
                pageHeight: Math.round(p1.getBoundingClientRect().height),
                headerHeight: Math.round(header.getBoundingClientRect().height),
                footerTop: Math.round(fRect.top),
                footerHeight: Math.round(fRect.height),
                children
              };
            })()
          `,
          returnByValue: true
        }
      }));
    };

    ws.onmessage = (m) => {
      console.log('Brief P1 Breakdown:', JSON.stringify(JSON.parse(m.data)?.result?.result?.value, null, 2));
      ws.close();
      chrome.kill();
    };
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}

testBrief();
