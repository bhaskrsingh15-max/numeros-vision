/**
 * Numeros Vision — Coming Soon & Inline Status Module
 * Handles DPDP-compliant update sign-ups on tools awaiting backend activation
 * and provides non-blocking inline status feedback (zero alert() dialogs).
 */
(function () {
  'use strict';

  var WAITLIST_CONSENT_STATEMENT =
    'I consent to Numeros Vision storing my encrypted email address for 12 months solely for the purpose: "tell me when this report is available", with the right to delete my email record on request at any time under the DPDP Act 2023.';

  function nvShowInlineNotice(anchorEl, message, tone) {
    if (!anchorEl) return;
    var boxId = anchorEl.getAttribute('data-nv-notice-id');
    var box = boxId ? document.getElementById(boxId) : null;
    if (!box) {
      box = document.createElement('div');
      var generatedId = 'nv-inline-notice-' + Math.random().toString(36).slice(2, 9);
      box.id = generatedId;
      box.setAttribute('role', 'status');
      box.setAttribute('aria-live', 'polite');
      anchorEl.setAttribute('data-nv-notice-id', generatedId);
      if (anchorEl.parentNode) {
        anchorEl.parentNode.insertBefore(box, anchorEl.nextSibling);
      }
    }
    var isError = tone === 'error';
    var isSuccess = tone === 'success';
    box.style.marginTop = '12px';
    box.style.padding = '12px 16px';
    box.style.borderRadius = '10px';
    box.style.fontSize = '0.86rem';
    box.style.lineHeight = '1.55';
    box.style.fontWeight = '600';
    box.style.border = isError
      ? '1px solid rgba(180, 65, 45, 0.4)'
      : isSuccess
      ? '1px solid rgba(22, 131, 91, 0.4)'
      : '1px solid rgba(201, 162, 39, 0.4)';
    box.style.background = isError
      ? '#FDF5F3'
      : isSuccess
      ? '#EFF9F5'
      : '#FFFDF7';
    box.style.color = isError ? '#9B2C2C' : isSuccess ? '#16835B' : '#523E28';
    box.textContent = message;
    box.style.display = message ? 'block' : 'none';
  }

  window.nvShowInlineNotice = nvShowInlineNotice;

  async function handleComingSoonSubmit(evt) {
    evt.preventDefault();
    var form = evt.currentTarget;
    var emailInput = form.querySelector('input[type="email"]');
    var consentInput = form.querySelector('input[type="checkbox"]');
    var submitBtn = form.querySelector('button[type="submit"]');
    var statusEl = form.querySelector('[data-nv-waitlist-status]');
    var sourcePage = (form.getAttribute('data-source-page') || 'tool_coming_soon').slice(0, 64);

    function setStatus(msg, tone) {
      if (!statusEl) return;
      statusEl.style.display = 'block';
      statusEl.style.color =
        tone === 'error' ? '#9B2C2C' : tone === 'success' ? '#16835B' : '#8B6914';
      statusEl.style.background =
        tone === 'error' ? '#FDF5F3' : tone === 'success' ? '#EFF9F5' : '#FFFDF7';
      statusEl.style.borderColor =
        tone === 'error'
          ? 'rgba(180, 65, 45, 0.35)'
          : tone === 'success'
          ? 'rgba(22, 131, 91, 0.35)'
          : 'rgba(201, 162, 39, 0.35)';
      statusEl.textContent = msg;
    }

    var email = emailInput ? emailInput.value.trim().toLowerCase() : '';
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setStatus('Please enter a valid email address so we can notify you.', 'error');
      return;
    }
    if (!consentInput || !consentInput.checked) {
      setStatus('Please tick the DPDP 2023 notification consent box before submitting.', 'error');
      return;
    }

    if (submitBtn) submitBtn.disabled = true;
    setStatus('Preparing your request and saving your update preference...', 'working');

    try {
      var res = await fetch('/api/v1/waitlist/notify-me', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email,
          pack_id: 'report_advanced',
          consent: true,
          purpose: 'tell me when this report is available',
          consent_text: WAITLIST_CONSENT_STATEMENT,
          source_page: sourcePage
        })
      });
      var data = await res.json().catch(function () { return {}; });
      if (!res.ok || data.success === false) {
        setStatus(data.error || 'Could not save your email right now. Please try again shortly.', 'error');
      } else {
        setStatus('Thank you — your email is saved. We will write to you as soon as this tool opens.', 'success');
        form.reset();
      }
    } catch (_) {
      setStatus('Network connection interrupted while saving your request. Please try again.', 'error');
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  }

  function bindWaitlistForms() {
    var forms = document.querySelectorAll('form[data-nv-waitlist-form]');
    for (var i = 0; i < forms.length; i++) {
      if (!forms[i].hasAttribute('data-nv-bound')) {
        forms[i].setAttribute('data-nv-bound', 'true');
        forms[i].addEventListener('submit', handleComingSoonSubmit);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindWaitlistForms);
  } else {
    bindWaitlistForms();
  }
})();
