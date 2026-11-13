const fs = require('fs');
['app/services/internal_pdf_worker_service.py', 'pdf_service/app/services/internal_pdf_worker_service.py'].forEach(f => {
  let c = fs.readFileSync(f, 'utf8');
  if (!c.includes('@app.get("/healthz")')) {
    c = c.replace('@app.get("/internal/v1/health")', '@app.get("/internal/v1/health")\r\n@app.get("/healthz")');
    fs.writeFileSync(f, c, 'utf8');
    console.log('Updated ' + f);
  }
});
