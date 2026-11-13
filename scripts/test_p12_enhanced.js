const { spawn } = require('child_process');

async function testEnhancedP12() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9236',
    '--disable-gpu',
    '--window-size=1400,1400',
    'http://127.0.0.1:8000/sample?format=master&dob=1990-01-01'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const list = await (await fetch('http://127.0.0.1:9236/json')).json();
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
              const content = p12.querySelector('.page-content');
              const footer = p12.querySelector('.page-footer');
              
              // Let's inject the enhanced layout into page-12 content and measure!
              const driver = 1;
              const deityObj = EMBEDDED_DATA.deities['1'];
              const fastingObj = EMBEDDED_DATA.fasting['1'];
              const braceletObj = EMBEDDED_DATA.bracelets['1'];
              const yantraName = EMBEDDED_DATA.yantras['1'];
              const beejMantra = EMBEDDED_DATA.mantras['1'] || 'ॐ घृणि सूर्याय नमः';

              content.innerHTML = \`
                <div class="content-top-group">
                  <div class="chapter-hero-title">Spiritual Sadhana &amp; Divine Guardians</div>
                  <div class="chapter-hero-subtitle">Aligning the Microcosm with Celestial Order</div>

                  <!-- Side-by-side 2-column grid for Deity Sadhana & Fasting Discipline -->
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:10px;">
                    <div class="report-card" style="margin-bottom:0;padding:12px 16px;">
                      <div class="card-title">🕉️ \${deityObj.heading}</div>
                      <p class="body-p" style="font-size:11px;line-height:1.5;">\${deityObj.body}</p>
                    </div>

                    <div class="report-card" style="margin-bottom:0;padding:12px 16px;">
                      <div class="card-title">🥣 Fasting: \${fastingObj.heading}</div>
                      <p class="body-p" style="font-size:11px;line-height:1.5;">\${fastingObj.body}</p>
                    </div>
                  </div>

                  <!-- Sacred Beej Mantra & Chanting Attunement -->
                  <div class="report-card" style="border-left:3px solid #C9A227;margin-bottom:10px;padding:12px 16px;">
                    <div class="card-title" style="color:#8B6914;">📿 Sacred Beej Mantra &amp; Chanting Discipline</div>
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-top:4px;">
                      <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:15px;font-weight:700;color:#8B6914;letter-spacing:0.04em;">
                        ✦ \${beejMantra} ✦
                      </div>
                      <div style="font-size:11px;color:#523E28;font-family:'Manrope',sans-serif;">
                        <strong>Count:</strong> 108 Repetitions &nbsp;|&nbsp; <strong>Timing:</strong> Brahma Muhurta / Sunrise &nbsp;|&nbsp; <strong>Mala:</strong> Rudraksha
                      </div>
                    </div>
                  </div>

                  <!-- Crystal Attunement & Yantra -->
                  <div class="report-card" style="border-left:3px solid #16835B;margin-bottom:10px;padding:12px 16px;">
                    <div class="card-title" style="color:#16835B;">💎 Prescribed Crystals &amp; Sacred Yantra</div>
                    <p class="body-p" style="font-size:11px;line-height:1.5;">
                      <strong>Sacred Gemstones:</strong> \${braceletObj.items.join(' + ')} &nbsp;—&nbsp; <em>\${braceletObj.benefit}</em><br>
                      <strong>Sacred Yantra:</strong> \${yantraName}. Consecrate upon an altar oriented toward your prime vitality vector.
                    </p>
                  </div>
                </div>

                <!-- Grand Master Benediction Box -->
                <div style="text-align:center;padding:16px 22px;background:#FAF6EB;border-radius:12px;border:1.5px dashed #C9A227;margin-top:8px;">
                  <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:14px;color:#8B6914;font-weight:700;letter-spacing:0.08em;">✦ ASTROLOGER'S MASTER BENEDICTION &amp; SEAL ✦</div>
                  <p style="font-family:'Marcellus',serif;font-size:12.5px;color:#57534E;margin-top:6px;line-height:1.55;">
                    May divine harmony illuminate your mind, shield your vitality, and elevate your noble aspirations to enduring fruition. Walk forward with clarity, honour your karmic dharma, and reap the compounded abundance destined for your path.
                  </p>
                  <div style="margin-top:10px;font-family:'Cinzel',serif;font-size:10.5px;font-weight:700;color:#16835B;letter-spacing:0.12em;">
                    ✦ NUMEROS VISION · ANVEIL EVERY CHARM · CERTIFIED SACRED DOSSIER ✦
                  </div>
                </div>
              \`;

              const fRect = footer.getBoundingClientRect();
              const lastChild = content.children[content.children.length - 1];
              const lRect = lastChild.getBoundingClientRect();
              const pRect = p12.getBoundingClientRect();

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
      console.log('Enhanced P12 Driver 1 Result:', JSON.stringify(JSON.parse(m.data)?.result?.result?.value, null, 2));
      ws.close();
      chrome.kill();
    };
  } catch (e) {
    console.error(e);
    chrome.kill();
  }
}

testEnhancedP12();
