const { spawn } = require('child_process');

async function testFormat(formatName) {
  return new Promise((resolve) => {
    const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
      '--headless=new',
      '--remote-debugging-port=9223',
      '--disable-gpu',
      '--window-size=1400,1200',
      '--no-sandbox',
      `http://127.0.0.1:8000/sample?format=${formatName}`
    ]);

    setTimeout(async () => {
      try {
        const listRes = await fetch('http://127.0.0.1:9223/json');
        const pages = await listRes.json();
        const wsUrl = pages[0]?.webSocketDebuggerUrl;
        
        const ws = new WebSocket(wsUrl);
        let idCounter = 1;

        ws.onopen = () => {
          const expr = `
            (() => {
              const pages = Array.from(document.querySelectorAll('.pdf-page'));
              return pages.map((page, idx) => {
                const header = page.querySelector('.page-header');
                const footer = page.querySelector('.page-footer');
                const content = page.querySelector('.page-content');
                
                const pageRect = page.getBoundingClientRect();
                const footerRect = footer ? footer.getBoundingClientRect() : null;
                const contentRect = content ? content.getBoundingClientRect() : null;
                const headerRect = header ? header.getBoundingClientRect() : null;

                const lastContentChild = content ? content.lastElementChild : null;
                const lastChildRect = lastContentChild ? lastContentChild.getBoundingClientRect() : null;

                const distanceToFooter = (footerRect && lastChildRect) ? (footerRect.top - lastChildRect.bottom) : null;
                const footerBottomOffset = footerRect ? (pageRect.bottom - footerRect.bottom) : null;

                return {
                  pageNum: idx + 1,
                  pageId: page.id,
                  scrollHeight: Math.round(page.scrollHeight),
                  clientHeight: Math.round(page.clientHeight),
                  hasOverflow: page.scrollHeight > page.clientHeight + 1,
                  overflowPx: Math.round(page.scrollHeight - page.clientHeight),
                  footerBottomOffset: footerBottomOffset !== null ? Math.round(footerBottomOffset) : null,
                  distanceToFooter: distanceToFooter !== null ? Math.round(distanceToFooter) : null,
                  contentHeight: contentRect ? Math.round(contentRect.height) : null
                };
              });
            })()
          `;

          ws.send(JSON.stringify({
            id: idCounter++,
            method: 'Runtime.evaluate',
            params: { expression: expr, returnByValue: true }
          }));
        };

        ws.onmessage = (msg) => {
          const res = JSON.parse(msg.data);
          if (res.result?.result?.value) {
            console.log(`\n======================================================`);
            console.log(`=== METRICS FOR ${formatName.toUpperCase()} (${res.result.result.value.length} Pages) ===`);
            console.log(`======================================================`);
            res.result.result.value.forEach(p => {
              const status = p.hasOverflow ? `❌ OVERFLOW by ${p.overflowPx}px!` :
                             (p.distanceToFooter !== null && p.distanceToFooter < 5) ? `⚠️ TIGHT (${p.distanceToFooter}px gap)` : `✅ OK (${p.distanceToFooter}px gap)`;
              console.log(`P${p.pageNum.toString().padStart(2, ' ')} (${p.pageId}) | ScrollH: ${p.scrollHeight} / ClientH: ${p.clientHeight} | FooterBottom: ${p.footerBottomOffset}px | GapToFooter: ${p.distanceToFooter}px | ${status}`);
            });
            ws.close();
            chrome.kill();
            resolve();
          }
        };

        ws.onerror = (e) => {
          console.error('WS Error:', e);
          chrome.kill();
          resolve();
        };

      } catch (err) {
        console.error('Test error:', err.message);
        chrome.kill();
        resolve();
      }
    }, 2500);
  });
}

async function run() {
  await testFormat('brief');
  await new Promise(r => setTimeout(r, 1000));
  await testFormat('master');
  await new Promise(r => setTimeout(r, 1000));
  await testFormat('roadmap');
}

run();
