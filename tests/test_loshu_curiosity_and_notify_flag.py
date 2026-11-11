import json
import os
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from fastapi import HTTPException

from app.api.payments import (
    CreateOrderRequest,
    NotifyMeDeleteRequest,
    NotifyMeWaitlistRequest,
    create_order,
    delete_notify_me_waitlist,
    get_pricing_catalog,
    get_public_loshu_teasers,
    register_notify_me_waitlist,
)
from app.config.pricing_config import (
    is_notify_me_higher_tiers_enabled,
    recommend_ladder_tier,
)
from app.services.waitlist_service import (
    WAITLIST_DPDP_CONSENT_TEXT,
    WAITLIST_PURPOSE,
    WAITLIST_RETENTION_MONTHS,
    WAITLIST_RETENTION_SECONDS,
    build_waitlist_notification_email,
    decrypt_pii_field,
    delete_waitlist_records,
    encrypt_pii_field,
    produce_waitlist_notifications_for_pack,
    upsert_waitlist_record,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist_cloudflare_pages")
TEST_HEX_KEY = "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"


class TestLoShuCuriosityAndNotifyMeFlag(unittest.TestCase):
    """Verifies Mockup A Lo Shu Curiosity Block, encrypted DPDP waitlist, GST removal, and ladder recommendation rules."""

    def test_01_decorative_assets_budget_under_60kb(self):
        expected_assets = [
            "texture-pearl-gold.webp",
            "emblem-seal-lock.webp",
            "elem-wood.webp",
            "elem-fire.webp",
            "elem-earth.webp",
            "elem-metal.webp",
            "elem-water.webp",
        ]
        asset_dir = os.path.join(BASE_DIR, "app", "static", "assets", "loshu")
        for fname in expected_assets:
            fpath = os.path.join(asset_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing decorative asset: {fname}")
            size_bytes = os.path.getsize(fpath)
            self.assertLessEqual(
                size_bytes, 60 * 1024, f"Asset {fname} exceeds 60 KB budget ({size_bytes} bytes)"
            )

    def test_02_mockup_a_markup_no_prices_on_cells_no_gst_claims_and_consent_gate(self):
        yr_path = os.path.join(BASE_DIR, "app", "static", "your-reading.html")
        pr_path = os.path.join(BASE_DIR, "app", "static", "pricing.html")
        packs_path = os.path.join(BASE_DIR, "app", "config", "packs.json")

        with open(yr_path, "r", encoding="utf-8") as f:
            html = f.read()
        with open(pr_path, "r", encoding="utf-8") as f:
            pricing_html = f.read()
        with open(packs_path, "r", encoding="utf-8") as f:
            packs_raw = f.read()

        # Zero raw black #000000
        self.assertNotIn("#000000", html.upper())

        # Zero "GST included" or tax claim on prices across ladder, pricing page, packs.json, and dist
        for forbidden_tax in ("gst included", "incl. gst", "inclusive of gst", "including gst"):
            self.assertNotIn(forbidden_tax, html.lower())
            self.assertNotIn(forbidden_tax, pricing_html.lower())
        self.assertNotIn("price_includes_gst", packs_raw)

        if os.path.isdir(DIST_DIR):
            for root, _, files in os.walk(DIST_DIR):
                for fn in files:
                    if fn.lower().endswith((".html", ".js", ".json")):
                        with open(
                            os.path.join(root, fn), "r", encoding="utf-8", errors="ignore"
                        ) as fh:
                            txt = fh.read()
                        self.assertNotIn(
                            "gst included",
                            txt.lower(),
                            f"Found forbidden 'GST included' in built file {fn}",
                        )

        # Approved pattern label, reduced motion, and consent-gated analytics
        self.assertIn("Key Lo Shu Patterns:", html)
        self.assertIn("@media (prefers-reduced-motion: reduce)", html)
        self.assertIn("prefersReducedMotion()", html)
        self.assertIn("window.nvConsent.getStatus().analytics === true", html)
        self.assertIn("if (!hasAnalyticsConsent()) return;", html)

        # Extract #loshu-curiosity-card section and verify ZERO price strings or ₹ symbols inside it
        m = re.search(
            r'<section class="loshu-curiosity-card" id="loshu-curiosity-card".*?</section>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(m, "Could not locate #loshu-curiosity-card section")
        curiosity_markup = m.group(0)
        self.assertNotIn("₹", curiosity_markup)
        for price_tok in ("199", "289", "489", "699", "1,050", "1050", "1,479", "1479"):
            self.assertNotIn(price_tok, curiosity_markup)

        # Verify one three-card ladder with approved prices (199, 489, 1,050) and launch MRPs (289, 699, 1,479)
        self.assertIn('id="price-report_basic">₹199', html)
        self.assertIn('id="price-report_advanced">₹489', html)
        self.assertIn('id="price-report_premium">₹1,050', html)
        self.assertIn("Launch offer valid until 31 Jan 2027</div>", html)

        # Verify explicit DPDP consent text, purpose, 12-month retention, and delete-on-request UI in both pages
        for page_txt in (html, pricing_html):
            self.assertIn("tell me when this report is available", page_txt)
            self.assertIn("12 months", page_txt)
            self.assertIn("DPDP Act 2023", page_txt)
            self.assertIn("/api/v1/waitlist/notify-me/delete", page_txt)

    def test_03_never_ship_paid_report_prose_to_browser(self):
        lib_path = os.path.join(BASE_DIR, "app", "data", "basic_report_content_library.json")
        with open(lib_path, "r", encoding="utf-8") as f:
            lib = json.load(f)

        paid_sentinels = []
        topics = lib.get("topics", {})
        for topic_name, topic_obj in topics.items():
            if topic_name == "loshu_curiosity_teasers":
                continue
            raw_json = json.dumps(topic_obj, ensure_ascii=False)
            for match in re.findall(r'"([^"]{65,})"', raw_json):
                paid_sentinels.append(match)

        self.assertGreater(len(paid_sentinels), 50, "Expected substantial paid sentinel strings")

        files_to_scan = [
            os.path.join(BASE_DIR, "app", "static", "data", "loshu_public_teasers.json"),
            os.path.join(BASE_DIR, "app", "static", "your-reading.html"),
        ]
        dist_yr = os.path.join(DIST_DIR, "your-reading", "index.html")
        if os.path.exists(dist_yr):
            files_to_scan.append(dist_yr)
        dist_teasers = os.path.join(DIST_DIR, "data", "loshu_public_teasers.json")
        if os.path.exists(dist_teasers):
            files_to_scan.append(dist_teasers)

        self.assertFalse(
            os.path.exists(os.path.join(DIST_DIR, "basic_report_content_library.json"))
        )
        self.assertFalse(
            os.path.exists(os.path.join(DIST_DIR, "data", "basic_report_content_library.json"))
        )

        for fpath in files_to_scan:
            with open(fpath, "r", encoding="utf-8") as fh:
                content = fh.read()
            for sentinel in paid_sentinels:
                self.assertNotIn(
                    sentinel,
                    content,
                    f"PAID CONTENT LEAK in {fpath}: {sentinel[:60]}...",
                )

    def test_04_waitlist_encrypted_storage_dedupe_retention_delete_and_email_production(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            wl_path = os.path.join(tmpdir, "waitlist_notify_me.jsonl")
            fixed_now = 1_794_000_000

            # 1. Consent required
            with self.assertRaises(ValueError):
                upsert_waitlist_record(
                    email="seeker@example.com",
                    pack_id="report_advanced",
                    consent=False,
                    storage_path=wl_path,
                    encryption_key=TEST_HEX_KEY,
                    now_ts=fixed_now,
                )

            # 2. Wrong purpose rejected
            with self.assertRaises(ValueError):
                upsert_waitlist_record(
                    email="seeker@example.com",
                    pack_id="report_advanced",
                    consent=True,
                    purpose="marketing_newsletter",
                    storage_path=wl_path,
                    encryption_key=TEST_HEX_KEY,
                    now_ts=fixed_now,
                )

            # 3. Valid registration stores encrypted email (never plaintext), purpose, consent text, 12-month expiry
            reg1 = upsert_waitlist_record(
                email="Seeker@Example.com",
                pack_id="report_advanced",
                consent=True,
                purpose=WAITLIST_PURPOSE,
                consent_text=WAITLIST_DPDP_CONSENT_TEXT,
                source_page="your-reading",
                storage_path=wl_path,
                encryption_key=TEST_HEX_KEY,
                now_ts=fixed_now,
            )
            self.assertTrue(reg1["success"])
            self.assertFalse(reg1["deduplicated"])
            self.assertEqual(reg1["purpose"], "tell me when this report is available")
            self.assertEqual(reg1["retention_months"], 12)
            self.assertEqual(reg1["expires_at"], fixed_now + WAITLIST_RETENTION_SECONDS)

            with open(wl_path, "r", encoding="utf-8") as fh:
                raw_disk = fh.read()
            self.assertNotIn("seeker@example.com", raw_disk.lower())

            stored_rows = [json.loads(line) for line in raw_disk.splitlines() if line.strip()]
            self.assertEqual(len(stored_rows), 1)
            rec = stored_rows[0]
            self.assertIn(":", rec["email_enc"])
            self.assertEqual(decrypt_pii_field(rec["email_enc"], TEST_HEX_KEY), "seeker@example.com")
            self.assertEqual(rec["purpose"], "tell me when this report is available")
            self.assertEqual(rec["retention_months"], WAITLIST_RETENTION_MONTHS)
            self.assertIn("DPDP Act 2023", rec["consent_text"])

            # 4. De-duplication by email_sha256 + pack_id (second submission updates in-place, still 1 row)
            reg2 = upsert_waitlist_record(
                email="seeker@example.com",
                pack_id="report_advanced",
                consent=True,
                storage_path=wl_path,
                encryption_key=TEST_HEX_KEY,
                now_ts=fixed_now + 60,
            )
            self.assertTrue(reg2["deduplicated"])
            with open(wl_path, "r", encoding="utf-8") as fh:
                stored_rows_after = [json.loads(line) for line in fh.read().splitlines() if line.strip()]
            self.assertEqual(len(stored_rows_after), 1)

            # 5. Produce an actual notification email from the stored record!
            outbox = produce_waitlist_notifications_for_pack(
                "report_advanced",
                storage_path=wl_path,
                encryption_key=TEST_HEX_KEY,
                now_ts=fixed_now + 120,
            )
            self.assertEqual(len(outbox), 1)
            msg = outbox[0]
            self.assertEqual(msg["to"], "seeker@example.com")
            self.assertIn("Advanced Master Dossier", msg["subject"])
            self.assertEqual(msg["purpose"], "tell me when this report is available")
            self.assertIn("tell you when", msg["text"])
            self.assertIn("https://numerosvision.com/pricing.html", msg["html"])

            # 6. Retention enforcement: after 12 months, notification email CANNOT be produced
            with self.assertRaises(ValueError):
                build_waitlist_notification_email(
                    stored_rows_after[0],
                    encryption_key=TEST_HEX_KEY,
                    now_ts=fixed_now + WAITLIST_RETENTION_SECONDS + 100,
                )
            expired_outbox = produce_waitlist_notifications_for_pack(
                "report_advanced",
                storage_path=wl_path,
                encryption_key=TEST_HEX_KEY,
                now_ts=fixed_now + WAITLIST_RETENTION_SECONDS + 100,
            )
            self.assertEqual(expired_outbox, [])

            # 7. Delete-on-request erases the encrypted email record and prevents email production
            del_res = delete_waitlist_records(
                email="seeker@example.com",
                storage_path=wl_path,
            )
            self.assertTrue(del_res["success"])
            self.assertEqual(del_res["deleted_count"], 1)
            with open(wl_path, "r", encoding="utf-8") as fh:
                self.assertEqual(fh.read().strip(), "")
            post_delete_outbox = produce_waitlist_notifications_for_pack(
                "report_advanced",
                storage_path=wl_path,
                encryption_key=TEST_HEX_KEY,
                now_ts=fixed_now + 120,
            )
            self.assertEqual(post_delete_outbox, [])

    def test_05_worker_cross_crypto_and_notification_dispatch_and_recommendation_rule(self):
        # Verify Python <-> Cloudflare Worker AES-256-GCM cross-compatibility, Worker notification dispatch,
        # and Ladder Recommendation Rule parity across Python, Worker JS, and Browser catalog JS.
        py_ct = encrypt_pii_field("cross.check@example.com", TEST_HEX_KEY)
        node_script = f"""
import assert from 'node:assert';
import fs from 'node:fs';
import vm from 'node:vm';
import * as workerMod from './app/static/_worker.js';

const key = '{TEST_HEX_KEY}';

// 1. Decrypt ciphertext produced by Python waitlist_service
const decFromPy = await workerMod.decryptField('{py_ct}', key);
assert.strictEqual(decFromPy, 'cross.check@example.com');

// 2. Register waitlist record in Worker, verify zero plaintext in memoryStore, produce & dispatch notification email
workerMod.memoryStore.waitlistNotifyMe.clear();
workerMod.memoryStore.sentEmails.length = 0;
const env = {{
  ENVIRONMENT: 'test',
  DATA_ENCRYPTION_KEY: key,
  NV_EMAIL_LOG_ADAPTER: 'true',
  EMAIL_FROM: 'alerts@numerosvision.com'
}};

const reg = await workerMod.registerWaitlistNotifyMe(env, {{
  email: 'Notify.Me@Example.com',
  pack_id: 'report_premium',
  consent: true,
  purpose: 'tell me when this report is available'
}}, 1794000000);
assert.strictEqual(reg.status, 200);
assert.strictEqual(reg.payload.deduplicated, false);
assert.strictEqual(reg.payload.retention_months, 12);

const regDup = await workerMod.registerWaitlistNotifyMe(env, {{
  email: 'notify.me@example.com',
  pack_id: 'report_premium',
  consent: true
}}, 1794000050);
assert.strictEqual(regDup.payload.deduplicated, true);
assert.strictEqual(workerMod.memoryStore.waitlistNotifyMe.size, 1);

const rawStored = JSON.stringify(Array.from(workerMod.memoryStore.waitlistNotifyMe.values()));
assert.strictEqual(rawStored.toLowerCase().includes('notify.me@example.com'), false);

const dispatched = await workerMod.dispatchWaitlistNotificationsForPack(env, 'report_premium', 1794000100);
assert.strictEqual(dispatched.length, 1);
assert.strictEqual(dispatched[0].email.to, 'notify.me@example.com');
assert.strictEqual(workerMod.memoryStore.sentEmails.length, 1);
assert.strictEqual(workerMod.memoryStore.sentEmails[0].to, 'notify.me@example.com');

// 3. Delete-on-request removes stored record so subsequent dispatch produces 0 emails
const delRes = await workerMod.deleteWaitlistNotifyMe(env, {{ email: 'notify.me@example.com' }});
assert.strictEqual(delRes.status, 200);
assert.strictEqual(delRes.payload.deleted_count, 1);
const afterDel = await workerMod.dispatchWaitlistNotificationsForPack(env, 'report_premium', 1794000200);
assert.strictEqual(afterDel.length, 0);

// 4. Verify recommendation rule parity across Worker & Browser nv_pricing_catalog.js
const winCtx = {{ window: {{ location: {{ hostname: 'numerosvision.com', search: '' }} }} }};
winCtx.window.window = winCtx.window;
vm.runInNewContext(fs.readFileSync('./app/static/js/nv_pricing_catalog.js', 'utf8'), winCtx);

const workerCipher = await workerMod.encryptField('worker.to.py@example.com', key);
const ruleMatrix = [];
for (let g = 0; g <= 9; g++) {{
  const wFalse = workerMod.recommendLadderTier(g, false);
  const bFalse = winCtx.window.NV_PRICING.recommendLadderTier(g, false);
  const wTrue = workerMod.recommendLadderTier(g, true);
  const bTrue = winCtx.window.NV_PRICING.recommendLadderTier(g, true);
  assert.strictEqual(wFalse, bFalse);
  assert.strictEqual(wTrue, 'report_basic');
  assert.strictEqual(bTrue, 'report_basic');
  ruleMatrix.push([g, wFalse, wTrue]);
}}
console.log(JSON.stringify({{ workerCipher, ruleMatrix }}));
"""
        proc = subprocess.run(
            ["node", "--input-type=module", "-e", node_script],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True,
        )
        out = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(
            decrypt_pii_field(out["workerCipher"], TEST_HEX_KEY),
            "worker.to.py@example.com",
        )
        for gaps, worker_false, worker_true in out["ruleMatrix"]:
            py_false = recommend_ladder_tier(gaps, notify_me_higher_tiers=False)
            py_true = recommend_ladder_tier(gaps, notify_me_higher_tiers=True)
            self.assertEqual(py_false, worker_false)
            self.assertEqual(py_true, "report_basic")
            self.assertEqual(worker_true, "report_basic")
            if gaps <= 2:
                self.assertEqual(py_false, "report_basic")
            elif gaps <= 5:
                self.assertEqual(py_false, "report_advanced")
            else:
                self.assertEqual(py_false, "report_premium")

    def test_06_notify_me_flag_off_by_default_and_api_endpoints(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("NV_NOTIFY_ME_HIGHER_TIERS", None)
            self.assertFalse(is_notify_me_higher_tiers_enabled())
            cat_default = get_pricing_catalog()
            self.assertFalse(cat_default["feature_flags"]["notify_me_higher_tiers"])
            self.assertEqual(
                cat_default["ladder_recommendation_rule"]["default_recommended_tier"],
                "report_advanced",
            )

        teasers = get_public_loshu_teasers()
        self.assertTrue(teasers.get("public_browser_safe"))
        self.assertEqual(len(teasers.get("digits", {})), 9)
        self.assertEqual(len(teasers.get("planes", {})), 8)

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("app.api.payments.DATA_DIR", tmpdir):
                with self.assertRaises(HTTPException) as ctx_consent:
                    register_notify_me_waitlist(
                        NotifyMeWaitlistRequest(
                            email="seeker@example.com",
                            sku_id="report_advanced",
                            consent=False,
                        )
                    )
                self.assertEqual(ctx_consent.exception.status_code, 400)

                ok_resp = register_notify_me_waitlist(
                    NotifyMeWaitlistRequest(
                        email="seeker@example.com",
                        sku_id="report_advanced",
                        consent=True,
                        purpose="tell me when this report is available",
                        source_page="your-reading",
                    )
                )
                self.assertTrue(ok_resp["success"])
                self.assertEqual(ok_resp["status"], "registered")

                del_resp = delete_notify_me_waitlist(
                    NotifyMeDeleteRequest(email="seeker@example.com")
                )
                self.assertTrue(del_resp["success"])
                self.assertEqual(del_resp["deleted_count"], 1)

        def _run_sync_coro(coro):
            try:
                coro.send(None)
            except StopIteration as stop:
                return stop.value
            finally:
                coro.close()
            raise AssertionError("Expected synchronous return before any network await")

        with patch.dict(os.environ, {"NV_NOTIFY_ME_HIGHER_TIERS": "true"}):
            self.assertTrue(is_notify_me_higher_tiers_enabled())
            cat_on = get_pricing_catalog()
            self.assertTrue(cat_on["feature_flags"]["notify_me_higher_tiers"])
            self.assertEqual(
                cat_on["ladder_recommendation_rule"]["default_recommended_tier"],
                "report_basic",
            )
            for blocked_sku in ("report_advanced", "report_premium"):
                resp = _run_sync_coro(
                    create_order(
                        CreateOrderRequest(
                            plan=blocked_sku,
                            email="seeker@example.com",
                        )
                    )
                )
                self.assertEqual(resp.status_code, 409)
                payload = json.loads(resp.body.decode("utf-8"))
                self.assertEqual(payload["code"], "TIER_WAITLIST_ONLY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
