const { spawn } = require('child_process');

async function testAllDrivers(format, pageNum, dobs) {
  const results = [];
  for (const dob of dobs) {
    const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
      '--headless=new',
      '--remote-debugging-port=9235',
      '--disable-gpu',
      '--window-size=1400,1400',
      `http://127.0.0.1:8000/sample?format=${format}&dob=${dob}`
    ]);

    await new Promise(r => setTimeout(r, 1800));

    try {
      const list = await (await fetch('http://127.0.0.1:9235/json')).json();
      const target = list.find(p => p.url.includes('http://127.0.0.1:8000'));
      const ws = new WebSocket(target.webSocketDebuggerUrl);

      const res = await new Promise(resolve => {
        ws.onopen = () => {
          ws.send(JSON.stringify({
            id: 1,
            method: 'Runtime.evaluate',
            params: {
              expression: `
                (() => {
                  const p = document.getElementById('page-${pageNum}');
                  if (!p) return { error: 'Page not found' };
                  const fRect = p.querySelector('.page-footer').getBoundingClientRect();
                  const c = p.querySelector('.page-content');
                  const lastChild = c.children[c.children.length - 1];
                  const lastRect = lastChild.getBoundingClientRect();
                  const pRect = p.getBoundingClientRect();
                  return {
                    dob: '${dob}',
                    pageHeight: Math.round(pRect.height),
                    footerTop: Math.round(fRect.top),
                    lastChildBottom: Math.round(lastRect.bottom),
                    gapToFooter: Math.round(fRect.top - lastRect.bottom)
                  };
                })()
              `,
              returnByValue: true
            }
          }));
        };

        ws.onmessage = (m) => {
          resolve(JSON.parse(m.data)?.result?.result?.value);
        };
      });

      results.push(res);
      ws.close();
      chrome.kill();
    } catch (e) {
      console.error(e);
      chrome.kill();
    }
  }
  return results;
}

async function run() {
  // Test drivers 1 to 9 (e.g. 1990-01-01 -> driver 1, 1990-01-02 -> driver 2, etc.)
  const dobs = [
    '1990-01-01', // driver 1
    '1990-01-02', // driver 2
    '1990-01-03', // driver 3
    '1990-01-04', // driver 4
    '1990-01-05', // driver 5
    '1990-01-06', // driver 6
    '1990-01-07', // driver 7
    '1990-01-08', // driver 8
    '1990-01-09'  // driver 9
  ];
  console.log('Testing Master Page 12 across all 9 drivers...');
  const res = await testAllDrivers('master', 12, dobs);
  console.table(res);
}

run();
