// NUMEROS VISION — Companion Scheduled Worker
//
// Schedules:
//   1. Every 10 min (cron: */10 * * * *) — Stale-Order Razorpay Reconcile:
//      Polls D1 `orders` stuck in ('CREATED', 'PAYMENT_PENDING', 'PAYMENT_VERIFIED', 'pending')
//      between 10 minutes and 7 days old with a non-null `rzp_order_id`, queries Razorpay
//      `GET /v1/orders/{rzp_order_id}/payments`, verifies `status === 'captured'` (auto-capture on)
//      and exact INR `amount_paise`, and fulfills idempotently in D1.
//
//   2. Daily 02:15 UTC (cron: 15 2 * * *) — 30-Day Retention Audit / Purge:
//      - Strictly disabled unless `ENABLE_RETENTION_PURGE_30D === "true"`.
//      - Defaults to `RETENTION_PURGE_MODE = "report_only"` (counts only, ZERO deletes).
//      - Scoped strictly to:
//          * expired `email_otp_challenges` (`expires_at < now`)
//          * expired `otp_challenges` (`expires_at < now`)
//          * expired `sessions` (`expires_at < now`)
//          * abandoned unpaid `orders` older than 30 days with zero payments/entitlements/report_jobs/invoices
//      - NEVER touches `users` or `subjects` (user accounts and natal profiles are preserved).

const CHARM_PACK_CREDITS = Object.freeze({
  charm_starter_5: 5,
  charm_guided_15: 15,
  charm_deep_40: 40,
});

const REPORT_PACK_IDS = new Set([
  'report_basic',
  'report_advanced',
  'report_premium',
  'planner_2027',
]);

function randomHex(bytesLen = 6) {
  const bytes = new Uint8Array(bytesLen);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('');
}

async function writeAuditLog(db, actorId, action, resourceType, resourceId, detailsObj, nowMs) {
  if (!db) return;
  const auditId = `aud_${nowMs}_${randomHex(4)}`;
  await db
    .prepare(
      `INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?)`
    )
    .bind(
      auditId,
      actorId,
      action,
      resourceType,
      resourceId,
      JSON.stringify(detailsObj || {}),
      nowMs
    )
    .run();
}

function validateRazorpayKeyForEnvironment(rzpKeyId, environment) {
  const envName = String(environment || 'preview').trim().toLowerCase();
  if (envName === 'production') {
    if (!rzpKeyId.startsWith('rzp_live_')) {
      return { ok: false, reason: 'production_requires_live_razorpay_key' };
    }
    return { ok: true };
  }
  if (!rzpKeyId.startsWith('rzp_test_')) {
    return { ok: false, reason: 'preview_requires_test_razorpay_key' };
  }
  return { ok: true };
}

/**
 * Idempotently fulfills a verified captured order in D1.
 */
async function fulfillCapturedOrderInD1(db, order, capturedPayment, nowMs, env) {
  const existingJob = await db
    .prepare('SELECT id, status FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1')
    .bind(order.id)
    .first();

  const existingPmt = await db
    .prepare('SELECT id FROM payments WHERE order_id = ? LIMIT 1')
    .bind(order.id)
    .first();

  if (order.status === 'PAID' && (existingJob || !REPORT_PACK_IDS.has(order.pack_id)) && existingPmt) {
    return {
      alreadyFulfilled: true,
      orderId: order.id,
      jobId: existingJob ? existingJob.id : null,
    };
  }

  // 1. Mark order PAID
  await db
    .prepare("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?")
    .bind(nowMs, order.id)
    .run();

  // 2. Record payment row
  const paymentId = String(capturedPayment.id || `rzp_cron_${order.id}`);
  const amountPaise = Number(capturedPayment.amount || order.amount_paise);
  const method = String(capturedPayment.method || 'razorpay_reconcile');
  if (!existingPmt) {
    await db
      .prepare(
        `INSERT OR IGNORE INTO payments (id, order_id, rzp_payment_id, amount_paise, status, method, captured_at)
         VALUES (?, ?, ?, ?, 'CAPTURED', ?, ?)`
      )
      .bind(`pmt_${nowMs}_${randomHex(4)}`, order.id, paymentId, amountPaise, method, nowMs)
      .run();
  }

  // 3. Grant entitlement if subject_id is attached
  if (order.subject_id) {
    await db
      .prepare(
        `INSERT OR IGNORE INTO entitlements (id, user_id, subject_id, pack_id, order_id, granted_at)
         VALUES (?, ?, ?, ?, ?, ?)`
      )
      .bind(
        `ent_${nowMs}_${randomHex(4)}`,
        order.user_id,
        order.subject_id,
        order.pack_id,
        order.id,
        nowMs
      )
      .run();
  }

  // 4. Credit ledger grant for Charm AI credit packs
  const creditCount = CHARM_PACK_CREDITS[order.pack_id] || 0;
  if (creditCount > 0) {
    const orderRefId = `order_${order.id}`;
    const existingCredit = await db
      .prepare('SELECT id FROM credit_ledger WHERE ref_id = ? LIMIT 1')
      .bind(orderRefId)
      .first();
    if (!existingCredit) {
      const prevRow = await db
        .prepare('SELECT COALESCE(SUM(delta), 0) AS bal FROM credit_ledger WHERE user_id = ?')
        .bind(order.user_id)
        .first();
      const newBalance = Number(prevRow ? prevRow.bal : 0) + creditCount;
      await db
        .prepare(
          `INSERT OR IGNORE INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
           VALUES (?, ?, ?, 'pack_purchase', ?, ?, ?)`
        )
        .bind(`crd_${nowMs}_${randomHex(4)}`, order.user_id, creditCount, orderRefId, newBalance, nowMs)
        .run();
    }
  }

  // 5. Queue report generation job if applicable
  let createdJobId = existingJob ? existingJob.id : null;
  if (!createdJobId && order.subject_id && REPORT_PACK_IDS.has(order.pack_id)) {
    createdJobId = `job_${nowMs}_${randomHex(4)}`;
    await db
      .prepare(
        `INSERT OR IGNORE INTO report_jobs (id, user_id, subject_id, pack_id, order_id, status, created_at)
         VALUES (?, ?, ?, ?, ?, 'QUEUED', ?)`
      )
      .bind(createdJobId, order.user_id, order.subject_id, order.pack_id, order.id, nowMs)
      .run();
  }

  // 6. Optional downstream notify to Pages Worker if WORKER_RECONCILE_URL is configured
  let downstreamNotified = false;
  if (env && env.WORKER_RECONCILE_URL && env.INTERNAL_CRON_SECRET) {
    try {
      const resp = await fetch(String(env.WORKER_RECONCILE_URL), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${String(env.INTERNAL_CRON_SECRET)}`,
        },
        body: JSON.stringify({
          order_id: order.id,
          job_id: createdJobId,
          source: 'companion_cron_worker',
        }),
      });
      downstreamNotified = resp.ok;
    } catch (_) {
      downstreamNotified = false;
    }
  }

  // 7. Audit log entry
  await writeAuditLog(
    db,
    'cron_reconcile',
    'cron_stale_order_reconciled',
    'orders',
    order.id,
    {
      paymentId,
      amountPaise,
      method,
      jobId: createdJobId,
      downstreamNotified,
    },
    nowMs
  );

  return {
    alreadyFulfilled: false,
    orderId: order.id,
    paymentId,
    jobId: createdJobId,
  };
}

/**
 * Every 10 minutes: Reconcile stale unfulfilled orders via Razorpay Orders Payments API.
 */
export async function runStaleOrderReconcile(env, nowMs = Date.now(), fetchImpl = fetch) {
  if (!env || !env.DB) {
    return { enabled: false, skipped: true, reason: 'missing_db_binding' };
  }
  if (String(env.ENABLE_STALE_RECONCILE || 'true').toLowerCase() === 'false') {
    return { enabled: false, skipped: true, reason: 'stale_reconcile_disabled' };
  }

  const rzpKeyId = String(env.RAZORPAY_KEY_ID || '').trim();
  const rzpSecret = String(env.RAZORPAY_KEY_SECRET || '').trim();
  if (!rzpKeyId || !rzpSecret) {
    return { enabled: true, skipped: true, reason: 'missing_razorpay_credentials' };
  }

  const keyCheck = validateRazorpayKeyForEnvironment(rzpKeyId, env.ENVIRONMENT);
  if (!keyCheck.ok) {
    await writeAuditLog(
      env.DB,
      'cron_reconcile',
      'cron_reconcile_blocked_key_mismatch',
      'system',
      'razorpay_config',
      { environment: env.ENVIRONMENT || 'preview', reason: keyCheck.reason },
      nowMs
    );
    return { enabled: true, skipped: true, reason: keyCheck.reason };
  }

  const minAgeMs = Math.max(60_000, Number(env.STALE_RECONCILE_MIN_AGE_MS || 600_000));
  const maxAgeMs = Math.max(minAgeMs + 60_000, Number(env.STALE_RECONCILE_MAX_AGE_MS || 604_800_000));
  const olderThanTs = nowMs - minAgeMs;
  const newerThanTs = nowMs - maxAgeMs;

  const { results } = await env.DB.prepare(
    `SELECT id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at, updated_at
     FROM orders
     WHERE status IN ('CREATED', 'PAYMENT_PENDING', 'PAYMENT_VERIFIED', 'pending')
       AND rzp_order_id IS NOT NULL
       AND created_at <= ?
       AND created_at >= ?
     ORDER BY created_at ASC
     LIMIT 50`
  )
    .bind(olderThanTs, newerThanTs)
    .all();

  const candidates = Array.isArray(results) ? results : [];
  const authHeader = 'Basic ' + btoa(`${rzpKeyId}:${rzpSecret}`);

  let reconciledCount = 0;
  let uncapturedAuthorizedCount = 0;
  let unpaidCount = 0;
  let errorCount = 0;
  const reconciledOrderIds = [];

  for (const order of candidates) {
    try {
      const rzpResp = await fetchImpl(
        `https://api.razorpay.com/v1/orders/${encodeURIComponent(order.rzp_order_id)}/payments`,
        {
          method: 'GET',
          headers: {
            Authorization: authHeader,
            Accept: 'application/json',
          },
        }
      );
      if (!rzpResp.ok) {
        errorCount += 1;
        continue;
      }
      const payload = await rzpResp.json().catch(() => ({}));
      const items = Array.isArray(payload && payload.items) ? payload.items : [];

      const capturedItem = items.find(
        (it) =>
          it &&
          String(it.status || '').toLowerCase() === 'captured' &&
          it.captured !== false &&
          Number(it.amount) === Number(order.amount_paise) &&
          String(it.currency || 'INR').toUpperCase() === 'INR'
      );

      if (capturedItem) {
        const res = await fulfillCapturedOrderInD1(env.DB, order, capturedItem, nowMs, env);
        reconciledCount += 1;
        reconciledOrderIds.push(res.orderId);
        continue;
      }

      const authorizedOnly = items.find(
        (it) => it && String(it.status || '').toLowerCase() === 'authorized'
      );
      if (authorizedOnly) {
        uncapturedAuthorizedCount += 1;
        await writeAuditLog(
          env.DB,
          'cron_reconcile',
          'reconcile_uncaptured_authorized_payment',
          'orders',
          order.id,
          {
            rzp_order_id: order.rzp_order_id,
            rzp_payment_id: authorizedOnly.id || null,
            note: 'Payment is authorized but not captured; check Razorpay auto-capture setting.',
          },
          nowMs
        );
      } else {
        unpaidCount += 1;
      }
    } catch (_) {
      errorCount += 1;
    }
  }

  return {
    enabled: true,
    skipped: false,
    scanned: candidates.length,
    reconciled: reconciledCount,
    reconciledOrderIds,
    uncapturedAuthorized: uncapturedAuthorizedCount,
    unpaid: unpaidCount,
    errors: errorCount,
  };
}

/**
 * Daily 02:15 UTC: 30-day retention job.
 * - Strictly gated behind ENABLE_RETENTION_PURGE_30D === 'true'.
 * - Defaults to RETENTION_PURGE_MODE === 'report_only' (counts only, ZERO deletes).
 * - Scoped ONLY to expired OTPs, expired sessions, and abandoned unpaid orders >30 days old.
 * - NEVER touches `users` or `subjects`.
 */
export async function runRetentionPurge30d(env, nowMs = Date.now()) {
  const zeroSummary = {
    email_otp_challenges: 0,
    otp_challenges: 0,
    sessions: 0,
    abandoned_orders: 0,
  };

  if (!env || !env.DB) {
    return {
      enabled: false,
      skipped: true,
      mode: 'disabled',
      reason: 'missing_db_binding',
      candidates: { ...zeroSummary },
      deleted: { ...zeroSummary },
    };
  }

  const flagEnabled = String(env.ENABLE_RETENTION_PURGE_30D || 'false').trim().toLowerCase() === 'true';
  if (!flagEnabled) {
    return {
      enabled: false,
      skipped: true,
      mode: 'disabled',
      reason: 'ENABLE_RETENTION_PURGE_30D_DISABLED',
      candidates: { ...zeroSummary },
      deleted: { ...zeroSummary },
    };
  }

  const rawMode = String(env.RETENTION_PURGE_MODE || 'report_only').trim().toLowerCase();
  const mode = rawMode === 'delete' ? 'delete' : 'report_only';
  const retentionDays = Math.max(30, Number(env.RETENTION_WINDOW_DAYS || 30));
  const cutoffOrderMs = nowMs - retentionDays * 24 * 60 * 60 * 1000;

  const abandonedOrdersWhere = `
    status IN ('CREATED', 'PAYMENT_PENDING', 'pending')
    AND created_at < ?
    AND NOT EXISTS (SELECT 1 FROM payments p WHERE p.order_id = orders.id)
    AND NOT EXISTS (SELECT 1 FROM entitlements e WHERE e.order_id = orders.id)
    AND NOT EXISTS (SELECT 1 FROM report_jobs rj WHERE rj.order_id = orders.id)
    AND NOT EXISTS (SELECT 1 FROM invoices inv WHERE inv.order_id = orders.id)
  `;

  const emailOtpRow = await env.DB.prepare(
    'SELECT COUNT(*) AS cnt FROM email_otp_challenges WHERE expires_at < ?'
  )
    .bind(nowMs)
    .first()
    .catch(() => ({ cnt: 0 }));

  const phoneOtpRow = await env.DB.prepare(
    'SELECT COUNT(*) AS cnt FROM otp_challenges WHERE expires_at < ?'
  )
    .bind(nowMs)
    .first()
    .catch(() => ({ cnt: 0 }));

  const sessionsRow = await env.DB.prepare(
    'SELECT COUNT(*) AS cnt FROM sessions WHERE expires_at < ?'
  )
    .bind(nowMs)
    .first()
    .catch(() => ({ cnt: 0 }));

  const ordersRow = await env.DB.prepare(
    `SELECT COUNT(*) AS cnt FROM orders WHERE ${abandonedOrdersWhere}`
  )
    .bind(cutoffOrderMs)
    .first()
    .catch(() => ({ cnt: 0 }));

  const candidates = {
    email_otp_challenges: Number((emailOtpRow && emailOtpRow.cnt) || 0),
    otp_challenges: Number((phoneOtpRow && phoneOtpRow.cnt) || 0),
    sessions: Number((sessionsRow && sessionsRow.cnt) || 0),
    abandoned_orders: Number((ordersRow && ordersRow.cnt) || 0),
  };

  if (mode !== 'delete') {
    await writeAuditLog(
      env.DB,
      'cron_retention',
      'retention_purge_30d_report_only',
      'system',
      'retention_30d',
      {
        mode: 'report_only',
        retentionDays,
        cutoffOrderMs,
        candidates,
        note: 'Report-only mode: counts recorded, zero rows deleted. Users and subjects are never in scope.',
      },
      nowMs
    );
    return {
      enabled: true,
      skipped: false,
      mode: 'report_only',
      retentionDays,
      candidates,
      deleted: { ...zeroSummary },
    };
  }

  // Delete mode (only reachable when BOTH ENABLE_RETENTION_PURGE_30D='true' AND RETENTION_PURGE_MODE='delete')
  const delEmailOtps = await env.DB.prepare(
    'DELETE FROM email_otp_challenges WHERE expires_at < ?'
  )
    .bind(nowMs)
    .run();

  const delPhoneOtps = await env.DB.prepare(
    'DELETE FROM otp_challenges WHERE expires_at < ?'
  )
    .bind(nowMs)
    .run();

  const delSessions = await env.DB.prepare(
    'DELETE FROM sessions WHERE expires_at < ?'
  )
    .bind(nowMs)
    .run();

  const delOrders = await env.DB.prepare(
    `DELETE FROM orders WHERE ${abandonedOrdersWhere}`
  )
    .bind(cutoffOrderMs)
    .run();

  const deleted = {
    email_otp_challenges: Number((delEmailOtps && delEmailOtps.meta && delEmailOtps.meta.changes) ?? candidates.email_otp_challenges),
    otp_challenges: Number((delPhoneOtps && delPhoneOtps.meta && delPhoneOtps.meta.changes) ?? candidates.otp_challenges),
    sessions: Number((delSessions && delSessions.meta && delSessions.meta.changes) ?? candidates.sessions),
    abandoned_orders: Number((delOrders && delOrders.meta && delOrders.meta.changes) ?? candidates.abandoned_orders),
  };

  await writeAuditLog(
    env.DB,
    'cron_retention',
    'retention_purge_30d_executed',
    'system',
    'retention_30d',
    {
      mode: 'delete',
      retentionDays,
      cutoffOrderMs,
      candidates,
      deleted,
      preservedTables: ['users', 'subjects'],
    },
    nowMs
  );

  return {
    enabled: true,
    skipped: false,
    mode: 'delete',
    retentionDays,
    candidates,
    deleted,
  };
}

export default {
  async scheduled(controller, env, ctx) {
    const cron = String((controller && controller.cron) || '').trim();
    const nowMs = (controller && controller.scheduledTime) ? Number(controller.scheduledTime) : Date.now();

    const task = async () => {
      if (cron === '15 2 * * *') {
        return await runRetentionPurge30d(env, nowMs);
      }
      // Default & `*/10 * * * *`: run stale-order reconciliation
      return await runStaleOrderReconcile(env, nowMs);
    };

    if (ctx && typeof ctx.waitUntil === 'function') {
      ctx.waitUntil(task());
    } else {
      await task();
    }
  },

  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/health') {
      return new Response(
        JSON.stringify({
          ok: true,
          worker: 'numeros-vision-cron',
          environment: env.ENVIRONMENT || 'preview',
          stale_reconcile_enabled: String(env.ENABLE_STALE_RECONCILE || 'true').toLowerCase() !== 'false',
          retention_purge_30d_enabled: String(env.ENABLE_RETENTION_PURGE_30D || 'false').toLowerCase() === 'true',
          retention_purge_mode:
            String(env.RETENTION_PURGE_MODE || 'report_only').toLowerCase() === 'delete'
              ? 'delete'
              : 'report_only',
        }),
        {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'X-Robots-Tag': 'noindex, nofollow',
          },
        }
      );
    }

    return new Response(JSON.stringify({ error: 'Scheduled cron worker only' }), {
      status: 403,
      headers: {
        'Content-Type': 'application/json',
        'X-Robots-Tag': 'noindex, nofollow',
      },
    });
  },
};
