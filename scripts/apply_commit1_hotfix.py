import os
import re

WORKER_PATH = os.path.join("app", "static", "_worker.js")
LOGIN_PATH = os.path.join("app", "static", "login.html")

def patch_worker():
    with open(WORKER_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # 1. Remove hardcoded Fast2SMS API Key (around line 8)
        if 'const FAST2SMS_API_KEY =' in line:
            new_lines.append("    // Fast2SMS API key strictly loaded from env.FAST2SMS_API_KEY\n")
            i += 1
            continue

        # 2. Add /reports/ to forbiddenPatterns
        if '/^\\/scripts\\//i,' in line:
            new_lines.append(line)
            new_lines.append("      /^\\/reports\\//i,\n")
            new_lines.append("      /^\\/static\\/reports\\//i,\n")
            i += 1
            continue

        # 3. Remove /static/reports/ rewrite
        if 'if (url.pathname.startsWith(\'/static/reports/\')) {' in line:
            # skip 4 lines
            i += 4
            new_lines.append("    // Direct static reports rewrite removed for security lockdown\n")
            continue

        # 4. Patch /api/v1/auth/otp/send to fail closed and remove session_otp
        if "if (url.pathname === '/api/v1/auth/otp/send' && request.method === 'POST') {" in line:
            # capture block until route 2
            otp_lines = []
            while i < n and "if (url.pathname === '/api/v1/auth/otp/verify'" not in lines[i]:
                otp_lines.append(lines[i])
                i += 1

            new_otp_block = """    if (url.pathname === '/api/v1/auth/otp/send' && request.method === 'POST') {
      try {
        const fast2smsKey = env.FAST2SMS_API_KEY;
        if (!fast2smsKey) {
          return new Response(JSON.stringify({
            success: false,
            error: 'SMS service unavailable. Fast2SMS credentials not configured in server environment.'
          }), {
            status: 503,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*'
            }
          });
        }

        const body = await request.json().catch(() => ({}));
        const rawPhone = body.phone || body.identifier || '';
        const cleanDigits = rawPhone.replace(/\\D/g, '');
        const mobile10 = cleanDigits.length >= 10 ? cleanDigits.slice(-10) : '';

        // Generate genuine cryptographically random 6-digit OTP
        const randomArray = new Uint32Array(1);
        crypto.getRandomValues(randomArray);
        const otpCode = (100000 + (randomArray[0] % 900000)).toString();

        let smsDispatched = false;
        let fast2smsResponse = null;

        // Dispatch real SMS via Fast2SMS India Gateway if valid 10-digit number
        if (mobile10 && mobile10.length === 10) {
          try {
            const fast2smsUrl = `https://www.fast2sms.com/dev/bulkV2?authorization=${encodeURIComponent(fast2smsKey)}&route=otp&variables_values=${otpCode}&numbers=${mobile10}`;
            const fResp = await fetch(fast2smsUrl, {
              method: 'GET',
              headers: {
                'cache-control': 'no-cache',
                'User-Agent': 'NumerosVision/1.0'
              }
            });
            fast2smsResponse = await fResp.json().catch(() => ({}));
            if (fast2smsResponse && fast2smsResponse.return === true) {
              smsDispatched = true;
            }
          } catch (smsErr) {
            console.error('[Fast2SMS_Edge_Error]', smsErr);
          }
        }

        return new Response(JSON.stringify({
          success: true,
          sms_delivered: smsDispatched,
          channel: 'sms',
          destination: mobile10 ? `+91 ${mobile10}` : rawPhone,
          message: smsDispatched 
            ? `Verification code dispatched to +91 ${mobile10}` 
            : 'Verification code generated for authentication'
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({
          success: false,
          error: err.message || 'OTP dispatch error'
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

"""
            new_lines.append(new_otp_block)
            continue

        # 5. Patch order creation to remove hardcoded fallback keys and fail closed
        if "// Bypass stale / revoked Cloudflare environment variables" in line or "let rzpKeyId = env.RAZORPAY_KEY_ID;" in line:
            # Skip until `return new Response(JSON.stringify({`
            while i < n and "return new Response(JSON.stringify({" not in lines[i]:
                i += 1

            new_order_auth = """      // Razorpay Credentials strictly loaded from Cloudflare environment secrets
      const rzpKeyId = env.RAZORPAY_KEY_ID;
      const rzpSecret = env.RAZORPAY_KEY_SECRET;

      if (!rzpKeyId || !rzpSecret || rzpKeyId.includes('REPLACE_ME') || rzpKeyId.includes('PLACEHOLDER')) {
        return new Response(JSON.stringify({
          status: 'error',
          code: 'GATEWAY_CONFIG_MISSING',
          message: 'Payment gateway credentials are not configured in the server environment.'
        }), { status: 500, headers: corsHeaders });
      }

      let orderId = null;

      try {
        const authHeader = 'Basic ' + btoa(`${rzpKeyId}:${rzpSecret}`);
        const rzpReq = await fetch('https://api.razorpay.com/v1/orders', {
          method: 'POST',
          headers: {
            'Authorization': authHeader,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            amount: amountPaise,
            currency: 'INR',
            receipt: `nv_rcpt_${Date.now()}`,
            notes: {
              plan: plan,
              name: custName,
              email: custEmail,
              phone: custPhone,
              locked_dob: lockedDob,
              subject_hash: subjectHash
            }
          })
        });

        if (rzpReq.ok) {
          const rzpData = await rzpReq.json();
          if (rzpData.id) {
            orderId = rzpData.id;
          }
        } else {
          const errData = await rzpReq.json().catch(() => ({}));
          const errDesc = (errData && errData.error && errData.error.description) || 'Razorpay order creation failed';
          const isAuth = rzpReq.status === 401 || errDesc.toLowerCase().includes('auth');
          return new Response(JSON.stringify({
            status: 'error',
            code: isAuth ? 'RAZORPAY_AUTH_FAILED' : 'RAZORPAY_ORDER_FAILED',
            message: isAuth 
              ? 'Razorpay API authentication failed (HTTP 401). Please check server RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET.' 
              : errDesc,
            details: errData
          }), { status: rzpReq.status || 400, headers: corsHeaders });
        }
      } catch (apiErr) {
        return new Response(JSON.stringify({
          status: 'error',
          code: 'GATEWAY_NETWORK_ERROR',
          message: 'Unable to reach payment gateway to create order.'
        }), { status: 502, headers: corsHeaders });
      }

      if (!orderId) {
        return new Response(JSON.stringify({
          status: 'error',
          code: 'ORDER_CREATION_FAILED',
          message: 'Failed to obtain an authentic order ID from the payment gateway.'
        }), { status: 502, headers: corsHeaders });
      }

"""
            new_lines.append(new_order_auth)
            continue

        # 6. Patch payment verify: eliminate candidateSecrets and eliminate pay_ bypass
        if "// Multi-tier signature verification for seamless live and test checkout" in line:
            # Skip until `const currentYear = new Date().getFullYear();`
            while i < n and "const currentYear = new Date().getFullYear();" not in lines[i]:
                i += 1

            new_verify_code = """      const rzpSecret = env.RAZORPAY_KEY_SECRET;
      if (!rzpSecret) {
        return new Response(JSON.stringify({
          status: 'error',
          message: 'Payment gateway secret not configured on server.'
        }), { status: 500, headers: corsHeaders });
      }

      let isSigValid = false;
      const cleanOrderId = (orderId || '').trim();
      const cleanPaymentId = (paymentId || '').trim();
      const cleanSig = (signature || '').trim().toLowerCase();

      if (cleanSig && cleanOrderId && cleanPaymentId) {
        try {
          const encoder = new TextEncoder();
          const keyData = encoder.encode(rzpSecret.trim());
          const msgData = encoder.encode(`${cleanOrderId}|${cleanPaymentId}`);
          const cryptoKey = await crypto.subtle.importKey(
            'raw',
            keyData,
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
          );
          const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
          const hashArray = Array.from(new Uint8Array(sigBuffer));
          const genSig = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
          if (genSig.toLowerCase() === cleanSig) {
            isSigValid = true;
          }
        } catch (e) {
          console.error('[HMAC_Verification_Error]', e);
        }
      }

      // Mandatory check: Signature mismatch fails in every environment (zero bypass)
      if (!isSigValid) {
        return new Response(JSON.stringify({
          status: 'error',
          message: 'Invalid payment signature. Verification failed.'
        }), { status: 400, headers: corsHeaders });
      }

"""
            new_lines.append(new_verify_code)
            continue

        # 7. Patch /api/v1/reports/generate-pdf to return 403 upgrading
        if "if (url.pathname === '/api/v1/reports/generate-pdf' && request.method === 'POST') {" in line:
            while i < n and "if (url.pathname === '/api/charm/outcomes'" not in lines[i]:
                i += 1

            new_pdf_resp = """    if (url.pathname === '/api/v1/reports/generate-pdf' && request.method === 'POST') {
      return new Response(JSON.stringify({
        status: 'upgrading',
        code: 'REPORT_GENERATION_UPGRADING',
        message: 'Report generation is being upgraded to server-verified dynamic delivery. Purchases require server entitlement verification.'
      }), {
        status: 403,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

"""
            new_lines.append(new_pdf_resp)
            continue

        new_lines.append(line)
        i += 1

    with open(WORKER_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("_worker.js patched cleanly!")

def patch_login():
    with open(LOGIN_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean sandbox code print
    content = re.sub(
        r'const code = \(data && data\.otp_preview\) \? data\.otp_preview : \'123456\';\s*window\._activeLoginOtp = code;',
        '// OTP code delivered strictly via out-of-band SMS',
        content
    )
    content = re.sub(
        r'feedback\.innerHTML = `✓ Verification code sent! \(Testing Sandbox Code: <strong>\${code}</strong>\)`',
        "feedback.innerHTML = '✓ Verification code dispatched to your registered number.'",
        content
    )

    with open(LOGIN_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("login.html patched cleanly!")

if __name__ == "__main__":
    patch_worker()
    patch_login()
    print("All Commit 1 hotfixes applied successfully!")

def patch_webhook_secret():
    with open(WORKER_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    target = "const webhookSecret = env.RAZORPAY_WEBHOOK_SECRET || env.RAZORPAY_KEY_SECRET || '1ULhquBIAgRpt7D3VrAU56hZ';"
    replacement = """const webhookSecret = env.RAZORPAY_WEBHOOK_SECRET || env.RAZORPAY_KEY_SECRET;
      if (!webhookSecret) {
        return new Response(JSON.stringify({ status: 'error', message: 'Webhook secret not configured on server' }), { status: 500, headers: corsHeaders });
      }"""
    assert target in content, "webhookSecret target not found"
    content = content.replace(target, replacement)
    
    with open(WORKER_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("webhookSecret patched cleanly!")

if __name__ == "__main__":
    patch_webhook_secret()
