const fs = require('fs');
const path = require('path');

const srcHtml = fs.readFileSync('app/static/dashboard.html', 'utf8');

const baseView = {
  tier: 'free',
  entitlements: [],
  calculation: {
    driver: 1,
    conductor: 4,
    conductorDisplay: '13/4',
    driverPlanet: 'Sun',
    conductorPlanet: 'Rahu',
    presentDigits: [1, 4, 8, 9],
    missingDigits: [2, 3, 5, 6, 7]
  },
  sections: {
    grid: {
      cells: [
        { digit: 4, count: 1, status: 'present' },
        { digit: 9, count: 1, status: 'present' },
        { digit: 2, count: 0, status: 'locked' },
        { digit: 3, count: 0, status: 'locked' },
        { digit: 5, count: 0, status: 'locked' },
        { digit: 7, count: 0, status: 'locked' },
        { digit: 8, count: 1, status: 'present' },
        { digit: 1, count: 1, status: 'present' },
        { digit: 6, count: 0, status: 'locked' }
      ]
    }
  }
};

// 1. New User (Free tier)
const stateNewUser = {
  user: { userId: 'NV-USR-8821', name: 'Priya Sharma', email: 'priya.sharma@example.com', phone: '+91 98765 43210' },
  activeSubject: { id: 'sbj_1', name: 'Priya Sharma', dob: '1995-04-12' },
  subjects: [{ id: 'sbj_1', name: 'Priya Sharma', dob: '1995-04-12' }],
  charmCredits: 3,
  view: { ...baseView, tier: 'free', entitlements: [] },
  reports: [],
  receipts: []
};

// 2. ₹199 Buyer (Basic Report ready)
const state199Buyer = {
  user: { userId: 'NV-USR-1981', name: 'Bhaskr Singh', email: 'bhaskrsingh15@gmail.com', phone: '+91 98184 18039' },
  activeSubject: { id: 'sbj_2', name: 'Bhaskr Singh', dob: '1981-11-28' },
  subjects: [{ id: 'sbj_2', name: 'Bhaskr Singh', dob: '1981-11-28' }],
  charmCredits: 3,
  view: { ...baseView, tier: 'basic', entitlements: ['report_basic'] },
  reports: [
    {
      id: 'job_1794036935595_69d200c2',
      orderId: 'ord_1794036800739_8370d031',
      packId: 'report_basic',
      tier: 'basic',
      title: 'Basic Report',
      pages: 3,
      subjectName: 'Bhaskr Singh',
      subjectDob: '1981-11-28',
      status: 'ready',
      statusBadge: 'READY ✓',
      message: 'Your bespoke dossier has been rendered and verified.',
      isDownloadable: true,
      downloadUrl: '/samples/Numeros_Vision_Sample_Excerpt_Alexander_Vance.pdf'
    }
  ],
  receipts: [
    {
      order_id: 'ord_1794036800739_8370d031',
      payment_id: 'pay_TxCl4ha0lEITEn',
      pack_name: 'Basic Report (3 Pages)',
      amount_inr: 199,
      status: 'PAID',
      created_at: 1794036800739
    }
  ]
};

// 3. ₹1,050 Buyer (Premium Sovereign Blueprint ready)
const state1050Buyer = {
  user: { userId: 'NV-USR-7910', name: 'Alexander Vance', email: 'alexander.vance@example.com', phone: '+91 99100 22334' },
  activeSubject: { id: 'sbj_3', name: 'Alexander Vance', dob: '1979-08-22' },
  subjects: [{ id: 'sbj_3', name: 'Alexander Vance', dob: '1979-08-22' }],
  charmCredits: 10,
  view: { ...baseView, tier: 'premium', entitlements: ['report_premium'] },
  reports: [
    {
      id: 'job_sov_1050',
      orderId: 'ord_sov_1050',
      packId: 'report_premium',
      tier: 'premium',
      title: 'Premium Sovereign Blueprint',
      pages: 32,
      subjectName: 'Alexander Vance',
      subjectDob: '1979-08-22',
      status: 'ready',
      statusBadge: 'READY ✓',
      message: 'Your bespoke 32-page Sovereign Executive Master Blueprint is ready for download.',
      isDownloadable: true,
      downloadUrl: '/samples/Numeros_Vision_Sample_Excerpt_Alexander_Vance.pdf'
    }
  ],
  receipts: [
    {
      order_id: 'ord_sov_1050',
      payment_id: 'pay_sov_1050_rzp',
      pack_name: 'Premium Sovereign Blueprint (32 Pages)',
      amount_inr: 1050,
      status: 'PAID',
      created_at: 1794036000000
    }
  ]
};

function makePreviewHtml(state) {
  // Replace initDashboard with immediate mock render
  return srcHtml.replace(
    'document.addEventListener(\'DOMContentLoaded\', initDashboard);',
    `document.addEventListener('DOMContentLoaded', () => {
      _dashboardState = ${JSON.stringify(state, null, 2)};
      renderDashboard(_dashboardState);
    });`
  );
}

fs.writeFileSync('preview_new_user.html', makePreviewHtml(stateNewUser), 'utf8');
fs.writeFileSync('preview_199_buyer.html', makePreviewHtml(state199Buyer), 'utf8');
fs.writeFileSync('preview_1050_buyer.html', makePreviewHtml(state1050Buyer), 'utf8');

console.log('Successfully generated preview_new_user.html, preview_199_buyer.html, preview_1050_buyer.html');
