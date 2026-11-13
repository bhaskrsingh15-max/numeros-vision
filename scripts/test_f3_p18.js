const { spawn } = require('child_process');

async function testF3P18() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9238',
    '--disable-gpu',
    '--window-size=1400,1200',
    'http://127.0.0.1:8000/sample?format=roadmap'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const list = await (await fetch('http://127.0.0.1:9238/json')).json();
    const target = list.find(p => p.url.includes('http://127.0.0.1:8000'));
    const ws = new WebSocket(target.webSocketDebuggerUrl);

    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: {
          expression: `
            (() => {
              const p18 = document.getElementById('page-18');
              const content = p18.querySelector('.page-content');
              const footer = p18.querySelector('.page-footer');
              
              const beejMantra = EMBEDDED_DATA.mantras['9'] || 'ॐ अं अंगारकाय नमः';
              const braceletObj = EMBEDDED_DATA.bracelets['9'];
              const yantraName = EMBEDDED_DATA.yantras['9'];

              content.innerHTML = \`
                <div class="content-top-group">
                  <div class="chapter-hero-title">Digital Resonance &amp; Sovereign Benediction</div>
                  <div class="chapter-hero-subtitle">Mobile Frequency, Ambient Spaces &amp; The Astrologer's Lifetime Blessing</div>

                  <div class="report-card" style="padding:12px 16px;margin-bottom:10px;">
                    <div class="card-title">📱 Mobile &amp; Ambient Digital Resonance: 9876543210</div>
                    <p class="body-p" style="font-size:11px;line-height:1.5;">
                      Your mobile digits generate high-frequency micro-pulses throughout daily communications. Maintaining balanced neutral pairs fosters smooth commercial negotiations and protective boundaries against digital burnout.
                    </p>
                  </div>

                  <!-- Sacred Beej Mantra & Chanting Attunement -->
                  <div class="report-card" style="border-left:3px solid #C9A227;margin-bottom:10px;padding:12px 16px;">
                    <div class="card-title" style="color:#8B6914;">📿 Sacred Beej Mantra &amp; Lifetime Invocation</div>
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-top:4px;">
                      <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:15px;font-weight:700;color:#8B6914;letter-spacing:0.04em;">
                        ✦ \${beejMantra} ✦
                      </div>
                      <div style="font-size:11px;color:#523E28;font-family:'Manrope',sans-serif;">
                        <strong>Discipline:</strong> 108 Repetitions &nbsp;|&nbsp; <strong>Orientation:</strong> Supportive Vitality Vector &nbsp;|&nbsp; <strong>Mala:</strong> Rudraksha
                      </div>
                    </div>
                  </div>

                  <div class="report-card" style="border-left:3px solid #16835B;margin-bottom:10px;padding:12px 16px;">
                    <div class="card-title" style="color:#16835B;">💎 Prescribed Crystals &amp; Sacred Yantra Consecration</div>
                    <p class="body-p" style="font-size:11px;line-height:1.5;">
                      <strong>Supporting Crystals:</strong> \${braceletObj.items.join(' + ')} (\${braceletObj.benefit}).<br>
                      <strong>Sacred Yantra:</strong> \${yantraName}. Consecrate upon an altar oriented toward your wealth sanctuary.
                    </p>
                  </div>
                </div>

                <div style="text-align:center;padding:16px 22px;background:#FAF6EB;border-radius:12px;border:1.5px dashed #C9A227;margin-top:8px;">
                  <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:14px;color:#8B6914;font-weight:700;letter-spacing:0.08em;">✦ THE SOVEREIGN LIFETIME BENEDICTION ✦</div>
                  <p style="font-family:'Marcellus',serif;font-size:12.5px;color:#57534E;margin-top:6px;line-height:1.55;">
                    May celestial wisdom illuminate your intellect, may unshakeable peace guard your heart, and may the divine planetary currents carry your noble aspirations to supreme fruition. Walk forward with courage and sovereign poise.
                  </p>
                  <div style="margin-top:10px;font-family:'Cinzel',serif;font-size:10.5px;font-weight:700;color:#16835B;letter-spacing:0.12em;">
                    ✦ NUMEROS VISION · ANVEIL EVERY CHARM · VERIFIED ROYAL SEAL ✦
                  </div>
                </div>
              \`;

              const fRect = footer.getBoundingClientRect();
              const lastChild = content.children[content.children.length - 1];
              const lRect = lastChild.getBoundingClientRect();
              const pRect = p18.getBoundingClientRect();

              return {
                pageHeight: Math.round(pRect.height),
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
      console.log('Tuned F3 P18 Result:', JSON.stringify(JSON.parse(m.data)?.result?.result?.value, null, 2));
      ws.close();
      chrome.kill();
    };
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}

testF3P18();
