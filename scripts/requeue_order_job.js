// Re-queue stuck report job for order ord_1794036800739_8370d031
// Resets attempts to 0, status to QUEUED, last_error to NULL.
// Does NOT invoke the PDF service until confirmed working.

const { execSync } = require('child_process');

const sql = `
UPDATE report_jobs
SET status = 'QUEUED',
    attempts = 0,
    last_error = NULL,
    updated_at = ${Date.now()}
WHERE order_id = 'ord_1794036800739_8370d031';
`;

console.log('Re-queuing report job for order ord_1794036800739_8370d031 in D1 preview...');
const fs = require('fs');
fs.writeFileSync('temp_requeue.sql', sql, 'utf8');

try {
  const out = execSync('npx.cmd wrangler d1 execute numeros-vision-db-preview --remote --file=temp_requeue.sql', { encoding: 'utf8' });
  console.log(out);
  console.log('Successfully re-queued job in D1 preview.');
} catch (err) {
  console.error('Failed to execute re-queue:', err.stdout || err.message);
  process.exit(1);
} finally {
  if (fs.existsSync('temp_requeue.sql')) fs.unlinkSync('temp_requeue.sql');
}
