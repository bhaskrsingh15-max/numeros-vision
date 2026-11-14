/**
 * Numeros Vision — Phase 5 Logo Intelligence Studio Controller (v1)
 * -----------------------------------------------------------------
 * 100% server-backed via:
 *   - POST /api/v1/logo/five-layer-evaluate (JSON or multipart/form-data PNG/JPEG/PDF/SVG)
 *   - POST /api/v1/logo/preview
 *   - POST /api/v1/logo/analyze-existing
 *
 * Strictly zero client-side numerology or contrast math.
 * Displays 4 separate results (Visual Quality, Brand & Category Fit, Name Intelligence,
 * Traditional Numerology & Timing Alignment) — never one blended score.
 */
(function () {
  'use strict';

  var CONSULTANT_REVIEW_PARTNER_THRESHOLD = 4;
  var state = {
    mode: 'new_logo', // 'new_logo' | 'audit_existing'
    selectedSymbol: 'ascending_peak',
    primaryColor: '#523E28',
    accentColor: '#16835B',
    bgColor: '#FFFDF7',
    paletteExplicitlyChosen: false,
    symbolExplicitlyChosen: false,
    variant: 'horizontal_lockup', // 'horizontal_lockup' | 'stacked_lockup' | 'icon' | 'monochrome'
    lastEvaluation: null,
    partnerCount: 0
  };

  function esc(val) {
    return String(val == null ? '' : val)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function basisBadge(basis) {
    var b = String(basis || 'calculated').toLowerCase();
    var bg = '#EFF9F5';
    var fg = '#16835B';
    var bd = 'rgba(22, 131, 91, 0.35)';
    if (b.indexOf('traditional') !== -1) {
      bg = '#F7F3EA';
      fg = '#8B6914';
      bd = 'rgba(139, 105, 20, 0.35)';
    } else if (b.indexOf('not configured') !== -1) {
      bg = '#FDF5F3';
      fg = '#7A654D';
      bd = 'rgba(122, 101, 77, 0.35)';
    } else if (b.indexOf('published') !== -1) {
      bg = '#F5F7FA';
      fg = '#523E28';
      bd = 'rgba(82, 62, 40, 0.3)';
    }
    return (
      '<span style="display:inline-block; padding:2px 9px; border-radius:999px; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; background:' +
      bg +
      '; color:' +
      fg +
      '; border:1px solid ' +
      bd +
      ';">' +
      esc(basis || 'calculated') +
      '</span>'
    );
  }

  function setStatusNotice(elId, msg, tone) {
    var el = document.getElementById(elId);
    if (!el) return;
    if (!msg) {
      el.style.display = 'none';
      el.textContent = '';
      return;
    }
    el.style.display = 'block';
    el.style.background = tone === 'error' ? '#FDF5F3' : tone === 'success' ? '#EFF9F5' : '#FFFDF7';
    el.style.color = tone === 'error' ? '#9B2C2C' : tone === 'success' ? '#16835B' : '#523E28';
    el.style.border =
      tone === 'error'
        ? '1px solid rgba(180, 65, 45, 0.38)'
        : tone === 'success'
        ? '1px solid rgba(22, 131, 91, 0.38)'
        : '1px solid rgba(201, 162, 39, 0.38)';
    el.textContent = msg;
  }

  function switchStudioMode(mode) {
    state.mode = mode === 'audit_existing' ? 'audit_existing' : 'new_logo';
    var btnCreate = document.getElementById('tabCreateBtn');
    var btnAudit = document.getElementById('tabAuditBtn');
    var uploadBlock = document.getElementById('existingUploadBlock');
    var newLogoControls = document.getElementById('newLogoDesignControls');
    var submitLabel = document.getElementById('btnEvaluateLabel');

    if (btnCreate) btnCreate.classList.toggle('active', state.mode === 'new_logo');
    if (btnAudit) btnAudit.classList.toggle('active', state.mode === 'audit_existing');
    if (uploadBlock) uploadBlock.style.display = state.mode === 'audit_existing' ? 'block' : 'none';
    if (newLogoControls) newLogoControls.style.display = state.mode === 'new_logo' ? 'block' : 'none';
    if (submitLabel) {
      submitLabel.textContent =
        state.mode === 'audit_existing'
          ? 'Inspect Uploaded Logo & Run 5-Layer Evaluation ✦'
          : 'Build Vector Preview & Run 5-Layer Evaluation ✦';
    }
  }

  function addPartnerRow() {
    var container = document.getElementById('partnersContainer');
    if (!container) return;
    var rows = container.querySelectorAll('.nv-partner-row');
    var idx = rows.length + 1;
    if (idx > CONSULTANT_REVIEW_PARTNER_THRESHOLD) {
      setStatusNotice(
        'studioInlineNotice',
        'More than 4 active partners entered — all partners will be evaluated and flagged for consultant review.',
        'working'
      );
    }
    var row = document.createElement('div');
    row.className = 'nv-partner-row';
    row.style.cssText =
      'display:grid; grid-template-columns:1fr 1fr auto; gap:12px; align-items:end; margin-top:12px; padding:12px; border-radius:12px; background:#FFFDF7; border:1px solid rgba(201,162,39,0.26);';
    row.innerHTML =
      '<div class="field-group">' +
      '<label>Active Partner ' + idx + ' Name</label>' +
      '<input type="text" class="partner-name-input" placeholder="Partner full name" />' +
      '</div>' +
      '<div class="field-group">' +
      '<label>Active Partner ' + idx + ' Birth Date (YYYY-MM-DD)</label>' +
      '<input type="date" class="partner-dob-input" />' +
      '</div>' +
      '<button type="button" class="btn-remove-partner" style="padding:11px 14px; border-radius:10px; border:1px solid rgba(180,65,45,0.35); background:#FDF5F3; color:#9B2C2C; font-weight:700; cursor:pointer;">Remove</button>';

    var removeBtn = row.querySelector('.btn-remove-partner');
    if (removeBtn) {
      removeBtn.addEventListener('click', function () {
        row.remove();
      });
    }
    container.appendChild(row);
  }

  function collectPartners() {
    var out = [];
    var rows = document.querySelectorAll('#partnersContainer .nv-partner-row');
    for (var i = 0; i < rows.length; i++) {
      var nameEl = rows[i].querySelector('.partner-name-input');
      var dobEl = rows[i].querySelector('.partner-dob-input');
      var n = nameEl ? nameEl.value.trim() : '';
      var d = dobEl ? dobEl.value.trim() : '';
      if (n || d) {
        out.push({ name: n || 'Partner ' + (i + 1), dob: d });
      }
    }
    return out;
  }

  function selectSymbol(sym) {
    state.selectedSymbol = sym;
    state.symbolExplicitlyChosen = true;
    var cards = document.querySelectorAll('#symbolGallery .symbol-card-item');
    for (var i = 0; i < cards.length; i++) {
      cards[i].classList.toggle('selected', cards[i].getAttribute('data-symbol') === sym);
    }
  }

  function selectPalette(el, primary, accent, bg) {
    state.primaryColor = primary;
    state.accentColor = accent;
    state.bgColor = bg;
    state.paletteExplicitlyChosen = true;
    var items = document.querySelectorAll('#paletteGallery .palette-item');
    for (var i = 0; i < items.length; i++) {
      items[i].classList.remove('selected');
    }
    if (el) el.classList.add('selected');
  }

  function switchVariant(variant) {
    state.variant = variant;
    var map = {
      horizontal_lockup: 'btnVarHoriz',
      stacked_lockup: 'btnVarStacked',
      icon: 'btnVarIcon',
      monochrome: 'btnVarMono'
    };
    Object.keys(map).forEach(function (k) {
      var btn = document.getElementById(map[k]);
      if (btn) btn.classList.toggle('active', k === variant);
    });

    if (!state.lastEvaluation) return;
    if (variant === 'stacked_lockup' && state.mode === 'new_logo') {
      var lvEl = document.getElementById('lockupVariant');
      if (lvEl) lvEl.value = 'stacked_lockup';
      runEvaluation(false);
      return;
    }
    if (variant === 'horizontal_lockup' && state.mode === 'new_logo') {
      var lvElH = document.getElementById('lockupVariant');
      if (lvElH && lvElH.value !== 'horizontal_lockup') {
        lvElH.value = 'horizontal_lockup';
        runEvaluation(false);
        return;
      }
    }
    renderCanvasFromEvaluation(state.lastEvaluation);
  }

  function renderCanvasFromEvaluation(data) {
    var stage = document.getElementById('svgStage');
    if (!stage || !data) return;
    var assets = data.generated_assets || {};
    if (state.variant === 'icon' && assets.icon_svg) {
      stage.innerHTML = assets.icon_svg;
    } else if (state.variant === 'monochrome' && assets.monochrome_svg) {
      stage.innerHTML = assets.monochrome_svg;
    } else if (assets.svg || data.svg) {
      stage.innerHTML = assets.svg || data.svg;
    } else if (data.upload_reading) {
      var ur = data.upload_reading;
      stage.innerHTML =
        '<div style="text-align:center; padding:18px; color:#523E28;">' +
        '<div style="font-family:\'Cinzel\',serif; font-size:0.84rem; color:#8B6914; font-weight:700; margin-bottom:8px;">Uploaded File Inspected (' +
        esc(ur.format) +
        ')</div>' +
        '<div style="font-size:0.95rem; font-weight:600; margin-bottom:10px;">Detected Wordmark: ' +
        esc(ur.extracted_text || 'None detected') +
        ' (confidence ' +
        Math.round((Number(ur.text_confidence) || 0) * 100) +
        '%)</div>' +
        '<div style="display:inline-flex; gap:8px; align-items:center;">' +
        '<span style="display:inline-block; width:22px; height:22px; border-radius:6px; border:1px solid rgba(82,62,40,0.25); background:' +
        esc(ur.primary_foreground_hex) +
        ';" title="Primary"></span>' +
        '<span style="font-size:0.82rem;">Primary ' +
        esc(ur.primary_foreground_hex) +
        '</span>' +
        '<span style="display:inline-block; width:22px; height:22px; border-radius:6px; border:1px solid rgba(82,62,40,0.25); background:' +
        esc(ur.background_hex) +
        ';" title="Background"></span>' +
        '<span style="font-size:0.82rem;">Background ' +
        esc(ur.background_hex) +
        '</span>' +
        '</div>' +
        '</div>';
    }
  }

  function gatherIntakePayload(includeOverrides) {
    var val = function (id) {
      var el = document.getElementById(id);
      return el ? el.value.trim() : '';
    };
    var partners = collectPartners();
    var ownerDob = val('ownerDob');
    var consentEl = document.getElementById('dpdpConsent');
    var dpdpConsent = Boolean(consentEl && consentEl.checked);

    if ((ownerDob || partners.length > 0) && !dpdpConsent) {
      throw new Error('Please tick the DPDP Act 2023 consent checkbox before evaluating personal or partner birth dates.');
    }

    var payload = {
      intake_mode: state.mode,
      business_name: val('businessName'),
      tagline: val('brandTagline'),
      business_category: val('industrySector'),
      business_activity: val('businessActivity'),
      product_function: val('productFunction'),
      customer_outcome: val('customerOutcome'),
      target_audience: val('targetAudience'),
      market_region: val('marketRegion') || 'INDIA',
      price_position: val('brandPositioning') || 'mid',
      brand_stage: val('brandStage') || 'startup',
      brand_personality: val('brandPersonality'),
      preferred_logo_type: val('preferredLogoType') || 'combination_mark',
      lockup_variant: val('lockupVariant') || 'horizontal_lockup',
      primary_touchpoint: val('primaryTouchpoint') || 'app_web',
      owner_name: val('ownerName'),
      owner_dob: ownerDob,
      owner_birth_time: val('ownerBirthTime'),
      partners: partners,
      dpdp_consent: dpdpConsent
    };

    var latStr = val('ownerBirthLat');
    var lonStr = val('ownerBirthLon');
    if (latStr && lonStr) {
      payload.owner_birth_lat = parseFloat(latStr);
      payload.owner_birth_lon = parseFloat(lonStr);
    }

    if (state.mode === 'new_logo') {
      if (state.symbolExplicitlyChosen) {
        payload.symbol_concept = state.selectedSymbol;
      }
      if (state.paletteExplicitlyChosen) {
        payload.primary_color = state.primaryColor;
        payload.accent_color = state.accentColor;
        payload.bg_color = state.bgColor;
      }
    } else {
      var svgPaste = val('auditSvgInput');
      if (svgPaste) {
        if (/<script|javascript:|onload|onerror/i.test(svgPaste)) {
          throw new Error('Executable script or event attributes were detected in the pasted SVG markup. Remove script tags or upload the file directly so the server can flag vector integrity.');
        }
        payload.svg_content = svgPaste;
      }
    }

    if (includeOverrides) {
      var cText = val('overrideConfirmedText');
      var cPrim = val('overridePrimaryHex');
      var cAcc = val('overrideAccentHex');
      var cBg = val('overrideBgHex');
      if (cText) payload.confirmed_text = cText;
      if (cPrim) payload.confirmed_primary_color = cPrim;
      if (cAcc) payload.confirmed_accent_color = cAcc;
      if (cBg) payload.confirmed_bg_color = cBg;
    }

    return payload;
  }

  async function runEvaluation(includeOverrides) {
    setStatusNotice('studioInlineNotice', '', 'working');
    var btn = document.getElementById('btnRunFiveLayer');
    var payload;
    try {
      payload = gatherIntakePayload(Boolean(includeOverrides));
    } catch (validationErr) {
      setStatusNotice('studioInlineNotice', validationErr.message, 'error');
      return;
    }

    var fileInput = document.getElementById('logoUploadFile');
    var selectedFile = state.mode === 'audit_existing' && fileInput && fileInput.files && fileInput.files[0] ? fileInput.files[0] : null;

    if (state.mode === 'new_logo' && !payload.business_name) {
      setStatusNotice('studioInlineNotice', 'Please enter your exact business name (wordmark) to build a logo preview.', 'error');
      return;
    }
    if (state.mode === 'audit_existing' && !selectedFile && !payload.svg_content) {
      setStatusNotice('studioInlineNotice', 'Please upload a PNG, JPEG, PDF, or SVG logo file, or paste SVG markup to inspect.', 'error');
      return;
    }

    var stageCtrl = window.nvStartWorkingStages ? window.nvStartWorkingStages(btn) : null;
    if (btn) btn.disabled = true;

    try {
      var fetchOpts;
      if (selectedFile) {
        var fd = new FormData();
        fd.append('file', selectedFile, selectedFile.name);
        fd.append('payload_json', JSON.stringify(payload));
        fetchOpts = { method: 'POST', body: fd };
      } else {
        fetchOpts = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        };
      }

      var res = await fetch('/api/v1/logo/five-layer-evaluate', fetchOpts);
      var data = await res.json();
      if (!res.ok || data.ok === false) {
        throw new Error(data.error || data.detail || 'Logo evaluation could not be completed. Check your inputs and try again.');
      }

      state.lastEvaluation = data;
      renderFullFiveLayerResults(data);
      setStatusNotice('studioInlineNotice', 'Five-layer deterministic evaluation complete.', 'success');
    } catch (err) {
      setStatusNotice('studioInlineNotice', err.message || 'Service temporarily unavailable.', 'error');
    } finally {
      if (stageCtrl) stageCtrl.stop();
      if (btn) btn.disabled = false;
    }
  }

  function renderFullFiveLayerResults(data) {
    var resultsWrap = document.getElementById('fiveLayerResultsWrap');
    if (resultsWrap) resultsWrap.style.display = 'block';

    // Update top wordmark numerology summary from server response
    var ni = (data.four_results && data.four_results.name_intelligence) || {};
    var briefEl = document.getElementById('briefNumCalc');
    var tagEl = document.getElementById('briefRecommendationTag');
    if (briefEl) {
      if (ni.compound_number != null) {
        briefEl.textContent =
          'Server Chaldean Calculation: "' +
          (ni.wordmark || '') +
          '" → Compound ' +
          ni.compound_number +
          ' → Single-Digit Root ' +
          ni.root_number +
          ' (' +
          (ni.ruling_planet || 'Planet') +
          ')';
      } else {
        briefEl.textContent = ni.note || 'Wordmark calculation not configured yet — supply or confirm the brand wordmark.';
      }
    }
    if (tagEl && data.four_results && data.four_results.traditional_alignment) {
      tagEl.textContent =
        data.four_results.traditional_alignment.charm_basis_label ||
        'Checked Chaldean name and Mulank–Bhagyank numerology tables only (birth time not supplied)';
    }

    // 1. Canvas
    renderCanvasFromEvaluation(data);

    // 2. Upload Confidence & User Override Box (when in audit_existing or upload reading available)
    var overrideCard = document.getElementById('uploadConfidenceCard');
    if (overrideCard && data.upload_reading) {
      var ur = data.upload_reading;
      overrideCard.style.display = state.mode === 'audit_existing' ? 'block' : 'none';
      var summaryEl = document.getElementById('uploadReadingSummary');
      if (summaryEl) {
        summaryEl.innerHTML =
          '<strong>Detected Format:</strong> ' +
          esc(ur.format) +
          ' · <strong>Extracted Text:</strong> ' +
          esc(ur.extracted_text || 'None') +
          ' (' +
          Math.round((Number(ur.text_confidence) || 0) * 100) +
          '% confidence) · <strong>Colour Confidence:</strong> ' +
          Math.round((Number(ur.colour_confidence) || 0) * 100) +
          '%' +
          (ur.user_corrected ? ' · <em>User override active</em>' : '');
      }
      var oText = document.getElementById('overrideConfirmedText');
      var oPrim = document.getElementById('overridePrimaryHex');
      var oAcc = document.getElementById('overrideAccentHex');
      var oBg = document.getElementById('overrideBgHex');
      if (oText && !oText.value) oText.value = ur.extracted_text || '';
      if (oPrim && !oPrim.value) oPrim.value = ur.primary_foreground_hex || '';
      if (oAcc && !oAcc.value) oAcc.value = ur.accent_foreground_hex || '';
      if (oBg && !oBg.value) oBg.value = ur.background_hex || '';
    }

    // 3. Free Scan Verdict + Up to 3 Named Gaps
    var fs = data.free_scan || {};
    var fsBox = document.getElementById('freeScanBox');
    if (fsBox) {
      var verdictTone =
        fs.verdict === 'Aligned' ? '#16835B' : fs.verdict === 'Not aligned' ? '#9B2C2C' : '#8B6914';
      var gaps = Array.isArray(fs.named_gaps) ? fs.named_gaps : [];
      var gapsHtml = gaps.length
        ? '<ul style="margin:10px 0 0; padding-left:20px; font-size:0.88rem; color:#523E28; line-height:1.6;">' +
          gaps
            .map(function (g) {
              return '<li>' + esc(g) + '</li>';
            })
            .join('') +
          '</ul>'
        : '<div style="margin-top:8px; font-size:0.88rem; color:#16835B; font-weight:600;">All 9 measurable and traditional gates passed with zero named gaps.</div>';

      fsBox.innerHTML =
        '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">' +
        '<div>' +
        '<div style="font-family:\'Cinzel\',serif; font-size:0.75rem; color:#8B6914; font-weight:700; letter-spacing:1.4px; text-transform:uppercase;">Free Scan Indication</div>' +
        '<div style="font-family:\'Cormorant Garamond\',serif; font-size:1.75rem; font-weight:700; color:' +
        verdictTone +
        ';">' +
        esc(fs.verdict || 'Partly aligned') +
        ' (' +
        esc(fs.hard_gates_passed_count) +
        '/' +
        esc(fs.hard_gates_total) +
        ' Hard Gates Passed)</div>' +
        '</div>' +
        basisBadge(fs.basis || 'calculated') +
        '</div>' +
        gapsHtml;
    }

    // 4. Four Separate Results (NEVER one blended score)
    var fr = data.four_results || {};
    var vq = fr.visual_quality || {};
    var bf = fr.brand_fit || {};
    var nmi = fr.name_intelligence || {};
    var ta = fr.traditional_alignment || {};
    var fourGrid = document.getElementById('fourSeparateResultsGrid');
    if (fourGrid) {
      var phon = nmi.phonetic_profile || {};
      var recPal = ta.reconciled_palette || {};
      var excl = Array.isArray(ta.excluded_enemy_families) && ta.excluded_enemy_families.length
        ? ta.excluded_enemy_families.join(', ')
        : 'None excluded';

      fourGrid.innerHTML =
        // Card 1: Visual Quality
        '<div class="studio-card" style="margin-bottom:0; padding:22px;">' +
        '<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:10px;">' +
        '<h3 style="font-family:\'Cormorant Garamond\',serif; font-size:1.35rem; margin:0; color:#523E28;">1. Visual Quality</h3>' +
        basisBadge(vq.basis) +
        '</div>' +
        '<div style="font-size:0.86rem; color:#523E28; line-height:1.7;">' +
        '<div><strong>Status:</strong> ' + esc(vq.status) + ' (' + esc(vq.gates_passed) + ')</div>' +
        '<div><strong>WCAG Contrast:</strong> ' + esc(vq.contrast_ratio) + '</div>' +
        '<div><strong>Nothing Cut (Closed Outlines):</strong> ' + (vq.nothing_cut ? 'Pass' : 'Needs attention') + '</div>' +
        '<div><strong>Pure Clean SVG:</strong> ' + (vq.is_pure_vector ? 'Yes' : 'No (raster/script)') + '</div>' +
        '<div><strong>App-Icon Legibility &amp; Fonts:</strong> ' + (vq.app_icon_legible ? 'Legible' : 'Too small/dense') + ' · ' + esc(vq.font_count) + ' font(s)</div>' +
        '</div>' +
        '</div>' +
        // Card 2: Brand Fit
        '<div class="studio-card" style="margin-bottom:0; padding:22px;">' +
        '<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:10px;">' +
        '<h3 style="font-family:\'Cormorant Garamond\',serif; font-size:1.35rem; margin:0; color:#523E28;">2. Brand &amp; Category Fit</h3>' +
        basisBadge(bf.basis) +
        '</div>' +
        '<div style="font-size:0.86rem; color:#523E28; line-height:1.7;">' +
        '<div><strong>Category:</strong> ' + esc(bf.category_id) + ' (' + esc(bf.status) + ')</div>' +
        '<div><strong>Primary Colour Family:</strong> ' + esc(bf.active_primary_colour_family) + '</div>' +
        '<div><strong>Category Norms:</strong> ' + esc((bf.allowed_category_colour_families || []).join(', ') || 'Not configured') + '</div>' +
        '<div><strong>Shape &amp; Lightness Cue:</strong> ' + esc(bf.recommended_shape_family) + ' · ' + esc(bf.recommended_lightness) + '</div>' +
        '<div style="font-size:0.8rem; color:#7A654D; margin-top:4px;">' + esc(bf.startup_descriptiveness_note || '') + '</div>' +
        '</div>' +
        '</div>' +
        // Card 3: Name Intelligence
        '<div class="studio-card" style="margin-bottom:0; padding:22px;">' +
        '<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:10px;">' +
        '<h3 style="font-family:\'Cormorant Garamond\',serif; font-size:1.35rem; margin:0; color:#523E28;">3. Name Intelligence</h3>' +
        basisBadge(nmi.basis) +
        '</div>' +
        '<div style="font-size:0.86rem; color:#523E28; line-height:1.7;">' +
        '<div><strong>Wordmark:</strong> ' + esc(nmi.wordmark || 'Not supplied') + '</div>' +
        '<div><strong>Chaldean Compound &amp; Root:</strong> ' +
        (nmi.compound_number != null ? 'Compound ' + esc(nmi.compound_number) + ' → Root ' + esc(nmi.root_number) : 'Not configured') +
        '</div>' +
        '<div><strong>Ruling Archetype:</strong> ' + esc(nmi.ruling_planet || 'Not configured') + '</div>' +
        '<div><strong>Phonetic Sound Profile:</strong> ' + esc(phon.dominant_sound_cue || phon.summary || 'Not configured') + '</div>' +
        '</div>' +
        '</div>' +
        // Card 4: Traditional Alignment
        '<div class="studio-card" style="margin-bottom:0; padding:22px;">' +
        '<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px; margin-bottom:10px;">' +
        '<h3 style="font-family:\'Cormorant Garamond\',serif; font-size:1.35rem; margin:0; color:#523E28;">4. Traditional Alignment</h3>' +
        basisBadge(ta.basis) +
        '</div>' +
        '<div style="font-size:0.86rem; color:#523E28; line-height:1.7;">' +
        '<div><strong>Alignment Status:</strong> ' + esc(ta.status) + ' (' + esc(ta.partner_profiles_evaluated) + ' profile(s))</div>' +
        (ta.consultant_review_required
          ? '<div style="margin:4px 0; padding:6px 10px; border-radius:8px; background:rgba(201,162,39,0.12); color:#8B6914; font-weight:700;">Flagged for consultant review: ' +
            esc(ta.consultant_review_reason || 'More than 4 active partners supplied.') +
            '</div>'
          : '') +
        '<div><strong>Engine Checks:</strong> <strong>' + esc(ta.charm_basis_label) + '</strong></div>' +
        '<div><strong>Reconciled Palette:</strong> Main ' +
        esc(recPal.primary && recPal.primary.hex) +
        ' · Accent ' +
        esc(recPal.accent && recPal.accent.hex) +
        '</div>' +
        '<div><strong>Excluded Enemy Families:</strong> ' + esc(excl) + '</div>' +
        '<div><strong>Shukla Paksha (waxing lunar fortnight):</strong> ' + esc(ta.shukla_paksha_window) + '</div>' +
        '</div>' +
        '</div>';
    }

    // 5. All 9 Hard Gates
    var gatesWrap = document.getElementById('nineHardGatesList');
    if (gatesWrap && Array.isArray(data.hard_gates)) {
      gatesWrap.innerHTML = data.hard_gates
        .map(function (g) {
          var passColor = g.passed ? '#16835B' : '#9B2C2C';
          var passBg = g.passed ? '#EFF9F5' : '#FDF5F3';
          var passLabel = g.passed ? 'PASS' : 'FAIL';
          return (
            '<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; padding:12px 14px; border-radius:12px; background:#FFFDF7; border:1px solid rgba(201,162,39,0.28);">' +
            '<div style="flex:1 1 220px;">' +
            '<div style="font-weight:700; font-size:0.88rem; color:#523E28;">' + esc(g.name) + '</div>' +
            '<div style="font-size:0.81rem; color:#7A654D; margin-top:3px;">' + esc(g.measured_value) + '</div>' +
            '</div>' +
            '<div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">' +
            basisBadge(g.basis) +
            '<span style="padding:3px 10px; border-radius:999px; font-size:0.74rem; font-weight:700; background:' +
            passBg +
            '; color:' +
            passColor +
            ';">' +
            passLabel +
            '</span>' +
            '</div>' +
            '</div>'
          );
        })
        .join('');
    }

    // 6. Layer 5 Activation: 3 Shukla Paksha Dates + Ordered Balancing Steps
    var l5 = (data.layers && data.layers.layer5_activation) || {};
    var datesEl = document.getElementById('shuklaPakshaDatesBox');
    if (datesEl) {
      var dates = Array.isArray(l5.three_shukla_paksha_dates) ? l5.three_shukla_paksha_dates : [];
      datesEl.innerHTML = dates
        .map(function (d) {
          return (
            '<div style="padding:12px 14px; border-radius:12px; background:#FFFDF7; border:1px solid rgba(201,162,39,0.3);">' +
            '<div style="font-family:\'Cinzel\',serif; font-size:0.86rem; font-weight:700; color:#8B6914;">' +
            esc(d.date_iso || d.date) +
            ' (' +
            esc(d.weekday || '') +
            ')</div>' +
            '<div style="font-size:0.82rem; color:#523E28; margin-top:4px;">' +
            esc(d.tithi_label || 'Shukla Paksha (waxing lunar fortnight)') +
            (d.reason ? ' · ' + esc(d.reason) : '') +
            '</div>' +
            '</div>'
          );
        })
        .join('');
    }

    var remEl = document.getElementById('orderedRemediesBox');
    if (remEl) {
      var rems = Array.isArray(l5.ordered_remedies) ? l5.ordered_remedies : [];
      remEl.innerHTML = rems
        .map(function (r) {
          return (
            '<div style="padding:12px 16px; border-radius:12px; background:#FFFDF7; border-left:3px solid #C9A227;">' +
            '<div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">' +
            '<strong style="font-size:0.9rem; color:#523E28;">' + esc(r.title) + '</strong>' +
            basisBadge(r.basis) +
            '</div>' +
            '<p style="margin:6px 0 0; font-size:0.85rem; color:#7A654D; line-height:1.6;">' + esc(r.guidance) + '</p>' +
            '</div>'
          );
        })
        .join('');
    }

    // 7. Paid Tiers (Owner-Reviewed Delivery)
    renderPaidTiers(data.paid_tiers);
  }

  function renderPaidTiers(tiers) {
    var grid = document.getElementById('paidTiersGrid');
    if (!grid || !Array.isArray(tiers)) return;
    grid.innerHTML = tiers
      .map(function (t) {
        var inc = (t.includes || [])
          .map(function (line) {
            return '<li style="margin-bottom:5px;">' + esc(line) + '</li>';
          })
          .join('');
        var waitlistLabel = t.display_price_label || 'Coming soon, notify me';
        return (
          '<div style="background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.36); border-radius:16px; padding:20px; display:flex; flex-direction:column; justify-content:space-between;">' +
          '<div>' +
          '<div style="font-family:\'Cinzel\',serif; font-size:0.86rem; font-weight:700; color:#523E28;">' + esc(t.name) + '</div>' +
          '<div style="margin:10px 0;">' +
          '<span style="font-family:\'Cinzel\',serif; font-size:1.05rem; font-weight:700; color:var(--gold-dark, #8B6914);">' +
          esc(waitlistLabel) +
          '</span>' +
          '</div>' +
          '<ul style="padding-left:18px; margin:0 0 12px; font-size:0.82rem; color:#523E28; line-height:1.55;">' +
          inc +
          '</ul>' +
          '</div>' +
          '<div>' +
          '<div style="font-size:0.76rem; color:#7A654D; margin-bottom:10px; font-style:italic;">✦ ' +
          esc(t.delivery_note || 'Every paid output is reviewed by the owner before delivery.') +
          '</div>' +
          '<button type="button" class="btn-export" style="width:100%;" onclick="window.nvOpenTierInquiryModal(\'' +
          esc(t.tier_id) +
          '\', \'' +
          esc(t.name) +
          '\')">' +
          esc(waitlistLabel) +
          '</button>' +
          '</div>' +
          '</div>'
        );
      })
      .join('');
  }

  function openTierInquiryModal(tierId, tierName) {
    var modal = document.getElementById('logoLockModal');
    var heading = document.getElementById('logoModalHeading');
    var form = modal ? modal.querySelector('[data-nv-waitlist-form]') : null;
    if (heading) {
      heading.textContent = (tierName || 'Logo Intelligence Package') + ' — Owner-Reviewed Delivery';
    }
    if (form) {
      form.setAttribute('data-source-page', 'logo_tier_' + (tierId || 'inquiry'));
    }
    if (modal) modal.style.display = 'flex';
  }

  function closeTierInquiryModal() {
    var modal = document.getElementById('logoLockModal');
    if (modal) modal.style.display = 'none';
  }

  window.nvSwitchStudioMode = switchStudioMode;
  window.nvAddPartnerRow = addPartnerRow;
  window.nvSelectSymbol = selectSymbol;
  window.nvSelectPalette = selectPalette;
  window.nvSwitchVariant = switchVariant;
  window.nvRunLogoEvaluation = runEvaluation;
  window.nvOpenTierInquiryModal = openTierInquiryModal;
  window.nvCloseTierInquiryModal = closeTierInquiryModal;
})();
