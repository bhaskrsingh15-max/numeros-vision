/**
 * Numeros Vision — Deterministic Tool Runtime Helpers
 * Provides inline status feedback, live working stages (Calculating -> Analysing -> Preparing your reading),
 * and transparent provenance badge rendering (calculated | traditional rule | not configured).
 */
(function () {
  'use strict';

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
    box.textContent = message || '';
    box.style.display = message ? 'block' : 'none';
  }

  function nvStartWorkingStages(anchorEl) {
    var stages = [
      'Calculating...',
      'Analysing...',
      'Preparing your reading...'
    ];
    var idx = 0;
    var box = null;
    if (anchorEl && anchorEl.parentNode) {
      var existingId = anchorEl.getAttribute('data-nv-working-id');
      box = existingId ? document.getElementById(existingId) : null;
      if (!box) {
        box = document.createElement('div');
        var wid = 'nv-working-stage-' + Math.random().toString(36).slice(2, 9);
        box.id = wid;
        box.setAttribute('role', 'status');
        box.setAttribute('aria-live', 'polite');
        anchorEl.setAttribute('data-nv-working-id', wid);
        anchorEl.parentNode.insertBefore(box, anchorEl.nextSibling);
      }
      box.style.marginTop = '12px';
      box.style.padding = '11px 16px';
      box.style.borderRadius = '10px';
      box.style.fontSize = '0.85rem';
      box.style.fontWeight = '600';
      box.style.border = '1px solid rgba(201, 162, 39, 0.42)';
      box.style.background = '#F7F3EA';
      box.style.color = '#8B6914';
      box.style.display = 'block';
      box.textContent = stages[0];
    }
    var timer = setInterval(function () {
      idx = Math.min(idx + 1, stages.length - 1);
      if (box) {
        box.textContent = stages[idx];
      }
    }, 380);
    return {
      stop: function () {
        clearInterval(timer);
        if (box) {
          box.style.display = 'none';
        }
      }
    };
  }

  function escapeHtml(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function nvRenderProvenance(containerEl, provenanceLines) {
    if (!containerEl || !Array.isArray(provenanceLines) || provenanceLines.length === 0) {
      return;
    }
    var panel = containerEl.querySelector('[data-nv-provenance-panel]');
    if (!panel) {
      panel = document.createElement('div');
      panel.setAttribute('data-nv-provenance-panel', 'true');
      panel.style.marginTop = '24px';
      panel.style.padding = '20px 22px';
      panel.style.borderRadius = '14px';
      panel.style.background = '#FFFDF7';
      panel.style.border = '1px solid rgba(201, 162, 39, 0.32)';
      containerEl.appendChild(panel);
    }

    var rowsHtml = provenanceLines
      .map(function (item) {
        var basis = String(item.basis || 'calculated').toLowerCase();
        var badgeBg = '#EFF9F5';
        var badgeColor = '#16835B';
        var badgeBorder = 'rgba(22, 131, 91, 0.35)';
        if (basis === 'traditional rule') {
          badgeBg = '#F7F3EA';
          badgeColor = '#8B6914';
          badgeBorder = 'rgba(139, 105, 20, 0.35)';
        } else if (basis === 'not configured') {
          badgeBg = '#FDF5F3';
          badgeColor = '#7A654D';
          badgeBorder = 'rgba(122, 101, 77, 0.35)';
        }
        var valStr =
          item.value !== undefined && item.value !== null && item.value !== ''
            ? '<strong style="color:#523E28;">' + escapeHtml(item.value) + '</strong>'
            : '';
        var detailStr = item.detail
          ? '<div style="font-size:0.81rem; color:#7A654D; margin-top:3px;">' + escapeHtml(item.detail) + '</div>'
          : '';
        return (
          '<div style="display:flex; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; gap:10px; padding:10px 0; border-bottom:1px solid rgba(201,162,39,0.16);">' +
          '<div style="flex:1 1 240px;">' +
          '<div style="font-size:0.88rem; font-weight:600; color:#523E28;">' +
          escapeHtml(item.label || 'Line item') +
          (valStr ? ': ' + valStr : '') +
          '</div>' +
          detailStr +
          '</div>' +
          '<span style="display:inline-block; padding:3px 10px; border-radius:999px; font-size:0.74rem; font-weight:700; text-transform:uppercase; letter-spacing:0.6px; background:' +
          badgeBg +
          '; color:' +
          badgeColor +
          '; border:1px solid ' +
          badgeBorder +
          ';">' +
          escapeHtml(basis) +
          '</span>' +
          '</div>'
        );
      })
      .join('');

    panel.innerHTML =
      '<div style="font-family:\'Cinzel\',serif; font-size:0.8rem; font-weight:700; letter-spacing:1.4px; color:#8B6914; text-transform:uppercase; margin-bottom:6px;">Calculation &amp; Rule Basis</div>' +
      '<p style="font-size:0.82rem; color:#7A654D; margin:0 0 10px; line-height:1.5;">Each line is labelled as calculated mathematics, an interpretive traditional rule, or not configured.</p>' +
      rowsHtml;
  }

  window.nvShowInlineNotice = nvShowInlineNotice;
  window.nvStartWorkingStages = nvStartWorkingStages;
  window.nvRenderProvenance = nvRenderProvenance;
})();
