const { spawn } = require('child_process');

async function testFormat(formatName) {
  return new Promise((resolve) => {
    const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
      '--headless=new',
      '--remote-debugging-port=9227',
      '--disable-gpu',
      '--window-size=1400,1200',
      `http://127.0.0.1:8000/sample?format=${formatName}`
    ]);

    setTimeout(async () => {
      try {
        const list = await (await fetch('http://127.0.0.1:9227/json')).json();
        const target = list.find(p => p.url.includes('http://127.0.0.1:8000'));
        if (!target) {
          console.error('Target not found for', formatName);
          chrome.kill();
          return resolve();
        }

        const ws = new WebSocket(target.webSocketDebuggerUrl);

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
                const headerRect = header ? header.getBoundingClientRect() : null;
                const contentRect = content ? content.getBoundingClientRect() : null;

                const lastContentChild = content ? content.lastElementChild : null;
                const lastChildRect = lastContentChild ? lastContentChild.getBoundingClientRect() : null;

                const gapToFooter = (footerRect && lastChildRect) ? Math.round(footerRect.top - lastChildRect.bottom) : null;
                const footerBottomOffset = footerRect ? Math.round(pageRect.bottom - footerRect.bottom) : null;
                const headerTopOffset = headerRect ? Math.round(headerRect.top - pageRect.top) : null;

                return {
                  pageNum: idx + 1,
                  pageId: page.id,
                  scrollHeight: Math.round(page.scrollHeight),
                  clientHeight: Math.round(page.clientHeight),
                  headerTop: headerTopOffset,
                  footerBottom: footerBottomOffset,
                  gapToFooter: gapToFooter,
                  overflow: page.scrollHeight > page.clientHeight
                };
              });
            })()
          `;

          ws.send(JSON.stringify({
            id: 1,
            method: 'Runtime.evaluate',
            params: { expression: expr, returnByValue: true }
          }));
        };

        ws.onmessage = (msg) => {
          const res = JSON.parse(msg.data);
          const pages = res.result?.result?.value || [];
          console.log(`\n======================================================`);
          console.log(`FORMAT: ${formatName.toUpperCase()} (${pages.length} Pages)`);
          console.log(`======================================================`);
          pages.forEach(p => {
            const status = p.overflow ? `❌ OVERFLOW!` :
                           (p.gapToFooter !== null && p.gapToFooter <= 0) ? `❌ COLLISION with Footer (${p.gapToFooter}px)!` :
                           (p.gapToFooter !== null && p.gapToFooter < 8) ? `⚠️ VERY TIGHT (${p.gapToFooter}px gap)` :
                           `✅ OK (${p.gapToFooter}px gap)`;
            console.log(`P${p.pageNum.toString().padStart(2, ' ')} (${p.pageId}) | HeaderTop: ${p.headerTop}px | FooterBottom: ${p.footerBottom}px | GapToFooter: ${p.gapToFooter}px | ${status}`);
          });
          ws.close();
          chrome.kill();
          resolve();
        };

        ws.onerror = (e) => {
          console.error('WS Error:', e.message);
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
