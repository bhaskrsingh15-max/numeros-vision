const { spawn } = require('child_process');
const fs = require('fs');

async function capturePage(pageId, outputPath) {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9229',
    '--disable-gpu',
    '--window-size=1400,1600',
    'http://127.0.0.1:8000/sample?format=master'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const list = await (await fetch('http://127.0.0.1:9229/json')).json();
    const target = list.find(p => p.url.includes('http://127.0.0.1:8000'));
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    await new Promise(resolve => {
      ws.onopen = () => {
        ws.send(JSON.stringify({
          id: 1,
          method: 'Runtime.evaluate',
          params: {
            expression: `
              (() => {
                const el = document.getElementById('${pageId}');
                if (!el) return null;
                el.scrollIntoView();
                const r = el.getBoundingClientRect();
                return { x: r.x, y: r.y, width: r.width, height: r.height };
              })()
            `,
            returnByValue: true
          }
        }));
      };

      ws.onmessage = (m) => {
        const res = JSON.parse(m.data);
        if (res.id === 1) {
          const rect = res.result?.result?.value;
          if (rect) {
            setTimeout(() => {
              ws.send(JSON.stringify({
                id: 2,
                method: 'Page.captureScreenshot',
                params: {
                  clip: {
                    x: Math.max(0, rect.x),
                    y: Math.max(0, rect.y),
                    width: rect.width,
                    height: rect.height,
                    scale: 1
                  }
                }
              }));
            }, 300);
          } else {
            resolve();
          }
        } else if (res.id === 2) {
          const base64Data = res.result?.data;
          if (base64Data) {
            fs.writeFileSync(outputPath, Buffer.from(base64Data, 'base64'));
            console.log(`Saved screenshot of ${pageId} to ${outputPath}`);
          }
          resolve();
        }
      };
    });

    ws.close();
  } catch (e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

capturePage('page-12', 'scratch/page_12_exact.png');
