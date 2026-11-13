const { spawn } = require('child_process');

async function testBriefP1Tuning() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9237',
    '--disable-gpu',
    '--window-size=1400,1200',
    'http://127.0.0.1:8000/sample?format=brief'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const list = await (await fetch('http://127.0.0.1:9237/json')).json();
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
              const content = p1.querySelector('.page-content');
              const footer = p1.querySelector('.page-footer');
              
              // Remove inline justify-content
              content.style.justifyContent = 'flex-start';
              
              const img = content.querySelector('img');
              if (img) {
                img.style.width = '84px';
                img.style.height = '84px';
                img.parentElement.style.marginBottom = '6px';
              }
              
              const fRect = footer.getBoundingClientRect();
              const lastChild = content.children[content.children.length - 1];
              const lRect = lastChild.getBoundingClientRect();

              return {
                pageHeight: Math.round(p1.getBoundingClientRect().height),
                footerTop: Math.round(fRect.top),
                lastChildBottom: Math.round(lRect.bottom),
                gapToFooter: Math.round(fRect.top - lRect.bottom)
              };
            })()
          `,
          returnByValue: true
        }
      }));
    };

    ws.onmessage = (m) => {
      console.log('Tuned Brief P1 Result:', JSON.stringify(JSON.parse(m.data)?.result?.result?.value, null, 2));
      ws.close();
      chrome.kill();
    };
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}

testBriefP1Tuning();
