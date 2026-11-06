import worker, { encryptField, decryptField, getAesGcmKey, requireSecret } from '../app/static/_worker.js';

console.log('--- STARTING AES-GCM & FAIL-CLOSED SECRETS TESTS ---');

async function assertCase(name, fn) {
  try {
    await fn();
    console.log(`✓ PASS: ${name}`);
  } catch (err) {
    console.error(`✗ FAIL: ${name}`);
    console.error(err);
    process.exit(1);
  }
}

const VALID_32BYTE_HEX_KEY = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';

const testEnv = {
  ENVIRONMENT: 'production',
  DATA_ENCRYPTION_KEY: VALID_32BYTE_HEX_KEY,
  OTP_HMAC_SECRET: 'test-otp-hmac-secret-32bytes-long',
  SESSION_SECRET: 'test-session-secret-32bytes-long',
  IP_HASH_SALT: 'test-ip-hash-salt-32bytes-long'
};

async function run() {
  // 1. Fail-closed missing OTP_HMAC_SECRET outside ENVIRONMENT=local
  await assertCase('Missing OTP_HMAC_SECRET outside ENVIRONMENT=local returns 500 and logs variable name', async () => {
    const logs = [];
    const origErr = console.error;
    console.error = (...args) => logs.push(args.join(' '));
    try {
      const envNoOtp = { ...testEnv };
      delete envNoOtp.OTP_HMAC_SECRET;
      const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
        body: JSON.stringify({ phone: '9876543210' })
      });
      const res = await worker.fetch(req, envNoOtp);
      if (res.status !== 500) throw new Error(`Expected 500, got ${res.status}`);
      if (!logs.some(l => l.includes('OTP_HMAC_SECRET'))) {
        throw new Error(`Expected console.error to log OTP_HMAC_SECRET, got: ${JSON.stringify(logs)}`);
      }
    } finally {
      console.error = origErr;
    }
  });

  // 2. Fail-closed missing IP_HASH_SALT outside ENVIRONMENT=local
  await assertCase('Missing IP_HASH_SALT outside ENVIRONMENT=local returns 500 and logs variable name', async () => {
    const logs = [];
    const origErr = console.error;
    console.error = (...args) => logs.push(args.join(' '));
    try {
      const envNoIp = { ...testEnv };
      delete envNoIp.IP_HASH_SALT;
      const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
        body: JSON.stringify({ phone: '9876543210' })
      });
      const res = await worker.fetch(req, envNoIp);
      if (res.status !== 500) throw new Error(`Expected 500, got ${res.status}`);
      if (!logs.some(l => l.includes('IP_HASH_SALT'))) {
        throw new Error(`Expected console.error to log IP_HASH_SALT, got: ${JSON.stringify(logs)}`);
      }
    } finally {
      console.error = origErr;
    }
  });

  // 3. Fail-closed missing SESSION_SECRET outside ENVIRONMENT=local
  await assertCase('Missing SESSION_SECRET outside ENVIRONMENT=local returns 500 and logs variable name', async () => {
    const logs = [];
    const origErr = console.error;
    console.error = (...args) => logs.push(args.join(' '));
    try {
      const envNoSess = { ...testEnv };
      delete envNoSess.SESSION_SECRET;
      const req = new Request('https://numerosvision.com/api/me', {
        method: 'GET',
        headers: { 'Cookie': '__Host-nv_session=some_token_val' }
      });
      const res = await worker.fetch(req, envNoSess);
      if (res.status !== 500) throw new Error(`Expected 500, got ${res.status}`);
      if (!logs.some(l => l.includes('SESSION_SECRET'))) {
        throw new Error(`Expected console.error to log SESSION_SECRET, got: ${JSON.stringify(logs)}`);
      }
    } finally {
      console.error = origErr;
    }
  });

  // 4. Fail-closed missing DATA_ENCRYPTION_KEY outside ENVIRONMENT=local
  await assertCase('Missing DATA_ENCRYPTION_KEY outside ENVIRONMENT=local returns 500 and logs variable name', async () => {
    const logs = [];
    const origErr = console.error;
    console.error = (...args) => logs.push(args.join(' '));
    try {
      const mockDb = {
        prepare: (sql) => ({
          bind: () => ({
            first: async () => {
              if (sql.includes('SELECT s.id as session_id')) {
                return { session_id: 'ses_1', user_id: 'usr_test_1', expires_at: Date.now() + 100000 };
              }
              if (sql.includes('COUNT(*)')) return { cnt: 0 };
              return null;
            }
          })
        })
      };
      const envNoEnc = { ...testEnv, DB: mockDb };
      delete envNoEnc.DATA_ENCRYPTION_KEY;
      const req = new Request('https://numerosvision.com/api/v1/subjects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': '__Host-nv_session=dummy_token',
          'Origin': 'https://numerosvision.com'
        },
        body: JSON.stringify({ name: 'Aaditya', dob: '1990-08-15', consent: true })
      });
      const res = await worker.fetch(req, envNoEnc);
      if (res.status !== 500) throw new Error(`Expected 500, got ${res.status}`);
      if (!logs.some(l => l.includes('DATA_ENCRYPTION_KEY'))) {
        throw new Error(`Expected console.error to log DATA_ENCRYPTION_KEY, got: ${JSON.stringify(logs)}`);
      }
    } finally {
      console.error = origErr;
    }
  });

  // 5. Reject non-64-hex key (passphrases including 32-char UTF-8 strings are rejected)
  await assertCase('getAesGcmKey requires 64-hex DATA_ENCRYPTION_KEY and rejects passphrases', async () => {
    for (const invalidKey of ['short-passphrase', 'exactly-32-character-passphrase!', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz']) {
      let threw = false;
      try {
        await getAesGcmKey(invalidKey);
      } catch (e) {
        threw = true;
      }
      if (!threw) throw new Error(`Expected getAesGcmKey to throw on non-64-hex key: ${invalidKey}`);
    }
  });

  // 6. decryptField throws on plain-text fallback or tampered ciphertext
  await assertCase('decryptField throws on plain-text string (no legacy plain-text fallback) and corrupted ciphertext', async () => {
    let threwPlain = false;
    try {
      await decryptField('1990-08-15', VALID_32BYTE_HEX_KEY);
    } catch (e) {
      threwPlain = true;
    }
    if (!threwPlain) throw new Error('decryptField must throw on plain-text input instead of returning it');

    const validCipher = await encryptField('1990-08-15', VALID_32BYTE_HEX_KEY);
    const tampered = validCipher.slice(0, -2) + (validCipher.endsWith('ff') ? '00' : 'ff');
    let threwTampered = false;
    try {
      await decryptField(tampered, VALID_32BYTE_HEX_KEY);
    } catch (e) {
      threwTampered = true;
    }
    if (!threwTampered) throw new Error('decryptField must throw when AES-GCM authentication tag fails');
  });

  // 7. AES-GCM encrypts with random 12-byte IV (non-deterministic ciphertexts) and round-trips
  await assertCase('AES-GCM encrypts with random 12-byte IV (non-deterministic ciphertexts) and decrypts cleanly', async () => {
    const mockDb = {
      inserted: [],
      prepare: function(sql) {
        return {
          bind: (...args) => ({
            run: async () => {
              mockDb.inserted.push({ sql, args });
              return { success: true };
            },
            first: async () => {
              if (sql.includes('SELECT s.id as session_id')) {
                return { session_id: 'ses_1', user_id: 'usr_test_1', expires_at: Date.now() + 100000 };
              }
              if (sql.includes('COUNT(*)')) return { cnt: 0 };
              if (sql.includes('FROM users')) return { id: 'usr_test_1' };
              if (sql.includes('SELECT id FROM subjects')) return null;
              return null;
            },
            all: async () => ({ results: [] })
          })
        };
      }
    };

    const envWithDb = { ...testEnv, DB: mockDb };

    const req = new Request('https://numerosvision.com/api/v1/subjects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': '__Host-nv_session=dummy_token',
        'Origin': 'https://numerosvision.com'
      },
      body: JSON.stringify({
        name: 'Aaditya Sharma',
        dob: '1990-08-15',
        birthTime: '10:30',
        consent: true
      })
    });

    const res = await worker.fetch(req, envWithDb);
    if (res.status !== 201 && res.status !== 200) {
      const errText = await res.text();
      throw new Error(`Expected 201, got ${res.status}: ${errText}`);
    }

    const subInsert = mockDb.inserted.find(i => i.sql.includes('INSERT INTO subjects'));
    if (!subInsert) throw new Error('Subject insert was not recorded in DB');

    const dobEnc = subInsert.args[4];
    const birthTimeEnc = subInsert.args[5];

    if (!dobEnc || typeof dobEnc !== 'string' || !dobEnc.includes(':')) {
      throw new Error(`Expected AES-GCM iv:ciphertext format, got ${dobEnc}`);
    }
    if (dobEnc === '1990-08-15') {
      throw new Error('CRITICAL VULNERABILITY: Plain text DOB was stored in dob_enc!');
    }
    if (!birthTimeEnc || typeof birthTimeEnc !== 'string' || !birthTimeEnc.includes(':')) {
      throw new Error(`Expected AES-GCM iv:ciphertext format for birthTime, got ${birthTimeEnc}`);
    }

    const [ivHex, cipherHex] = dobEnc.split(':');
    if (ivHex.length !== 24) {
      throw new Error(`Expected 24-char hex IV (12 bytes), got ${ivHex.length}`);
    }

    const decryptedDob = await decryptField(dobEnc, VALID_32BYTE_HEX_KEY);
    if (decryptedDob !== '1990-08-15') {
      throw new Error(`Expected decrypted DOB 1990-08-15, got ${decryptedDob}`);
    }

    const req2 = new Request('https://numerosvision.com/api/v1/subjects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': '__Host-nv_session=dummy_token',
        'Origin': 'https://numerosvision.com'
      },
      body: JSON.stringify({
        name: 'Second Profile Same DOB',
        dob: '1990-08-15',
        consent: true
      })
    });

    await worker.fetch(req2, envWithDb);
    const subInsert2 = mockDb.inserted.filter(i => i.sql.includes('INSERT INTO subjects'))[1];
    const dobEnc2 = subInsert2.args[4];

    if (dobEnc === dobEnc2) {
      throw new Error('Deterministic IV vulnerability: identical DOB produced identical ciphertext!');
    }
  });

  console.log('\n--- RESULT: ALL 7 AES-GCM & FAIL-CLOSED SECRETS TESTS PASSED ---');
}

run();
