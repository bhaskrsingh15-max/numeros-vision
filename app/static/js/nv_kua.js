/**
 * NUMEROS VISION — CANONICAL BROWSER KUA ENGINE
 * ==============================================
 * Approved Formula:
 * 1. Sum all four digits of the calendar birth year, reduce to single digit = x.
 *    [Calendar birth year (1 Jan – 31 Dec) — CONFIRMED.]
 * 2. Male: 11 - x, then reduce to single digit.
 *    Female: 4 + x, then reduce to single digit.
 *    Same rule for every century; zero pre/post-2000 branching.
 * 3. Kua 5 maps to 2 for male and 8 for female [CONFIRMED].
 * 4. Derive element, trigram, and East/West group from the final Kua number.
 * 5. Missing or unrecognized gender returns display='Kua needs gender' — never guesses.
 */
/* global module */
(function (root, factory) {
  var api = factory();
  if (root) {
    root.NVKua = api;
    root.NVDigitRoot = api.digitRoot;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  } else if (typeof window === 'undefined' && root) {
    Object.keys(api).forEach(function (k) { root[k] = api[k]; });
  }
})(typeof globalThis !== 'undefined' ? globalThis : (typeof window !== 'undefined' ? window : this), function () {
  'use strict';

  var KUA_RULE_TEXT = 'Calculated from your birth year and gender';
  var KUA_NEEDS_GENDER_TEXT = 'Kua needs gender';

  var KUA_METADATA = {
    1: {
      element: 'Water',
      trigram: 'Kan',
      group: 'East Group',
      groupShort: 'East',
      elementGroup: 'Water · Kan (East Group)',
      directionSummary: 'Water · Kan (East Group · SE / E / S / N)',
      deskDirection: 'South-East',
      success: 'SE',
      health: 'E',
      relationship: 'S',
      stability: 'N'
    },
    2: {
      element: 'Earth',
      trigram: 'Kun',
      group: 'West Group',
      groupShort: 'West',
      elementGroup: 'Earth · Kun (West Group)',
      directionSummary: 'Earth · Kun (West Group · NE / W / NW / SW)',
      deskDirection: 'North-East',
      success: 'NE',
      health: 'W',
      relationship: 'NW',
      stability: 'SW'
    },
    3: {
      element: 'Wood',
      trigram: 'Zhen',
      group: 'East Group',
      groupShort: 'East',
      elementGroup: 'Wood · Zhen (East Group)',
      directionSummary: 'Wood · Zhen (East Group · S / N / SE / E)',
      deskDirection: 'South',
      success: 'S',
      health: 'N',
      relationship: 'SE',
      stability: 'E'
    },
    4: {
      element: 'Wood',
      trigram: 'Xun',
      group: 'East Group',
      groupShort: 'East',
      elementGroup: 'Wood · Xun (East Group)',
      directionSummary: 'Wood · Xun (East Group · N / S / E / SE)',
      deskDirection: 'North',
      success: 'N',
      health: 'S',
      relationship: 'E',
      stability: 'SE'
    },
    6: {
      element: 'Metal',
      trigram: 'Qian',
      group: 'West Group',
      groupShort: 'West',
      elementGroup: 'Metal · Qian (West Group)',
      directionSummary: 'Metal · Qian (West Group · W / NE / SW / NW)',
      deskDirection: 'West',
      success: 'W',
      health: 'NE',
      relationship: 'SW',
      stability: 'NW'
    },
    7: {
      element: 'Metal',
      trigram: 'Dui',
      group: 'West Group',
      groupShort: 'West',
      elementGroup: 'Metal · Dui (West Group)',
      directionSummary: 'Metal · Dui (West Group · NW / W / NE / SW)',
      deskDirection: 'North-West',
      success: 'NW',
      health: 'W',
      relationship: 'NE',
      stability: 'SW'
    },
    8: {
      element: 'Earth',
      trigram: 'Gen',
      group: 'West Group',
      groupShort: 'West',
      elementGroup: 'Earth · Gen (West Group)',
      directionSummary: 'Earth · Gen (West Group · SW / NW / W / NE)',
      deskDirection: 'South-West',
      success: 'SW',
      health: 'NW',
      relationship: 'W',
      stability: 'NE'
    },
    9: {
      element: 'Fire',
      trigram: 'Li',
      group: 'East Group',
      groupShort: 'East',
      elementGroup: 'Fire · Li (East Group)',
      directionSummary: 'Fire · Li (East Group · E / SE / N / S)',
      deskDirection: 'East',
      success: 'E',
      health: 'SE',
      relationship: 'N',
      stability: 'S'
    }
  };

  var CHALDEAN_MAP = {
    A: 1, I: 1, J: 1, Q: 1, Y: 1,
    B: 2, C: 2, K: 2, R: 2,
    G: 3, L: 3, S: 3,
    D: 4, M: 4, T: 4,
    E: 5, H: 5, N: 5, X: 5,
    U: 6, V: 6, W: 6,
    O: 7, Z: 7,
    F: 8, P: 8
  };

  var PYTHAGOREAN_MAP = {
    A: 1, J: 1, S: 1,
    B: 2, K: 2, T: 2,
    C: 3, L: 3, U: 3,
    D: 4, M: 4, V: 4,
    E: 5, N: 5, W: 5,
    F: 6, O: 6, X: 6,
    G: 7, P: 7, Y: 7,
    H: 8, Q: 8, Z: 8,
    I: 9, R: 9
  };

  /**
   * Canonical single-digit reduction:
   *   digitRoot(n) = 1 + (n - 1) % 9   for n > 0
   *   digitRoot(n) = 0                 for n <= 0
   * Master numbers (11, 22, 33) are NEVER preserved.
   */
  function digitRoot(num) {
    var val = Math.trunc(Number(num) || 0);
    return val > 0 ? 1 + ((val - 1) % 9) : 0;
  }

  function sumDigits(text) {
    var s = String(text === null || text === undefined ? '' : text);
    var total = 0;
    for (var i = 0; i < s.length; i++) {
      var code = s.charCodeAt(i);
      if (code >= 48 && code <= 57) {
        total += code - 48;
      }
    }
    return total;
  }

  function calcDriver(day) {
    return digitRoot(parseInt(day, 10) || 0);
  }

  function calcBhagyank(day, month, year) {
    var dStr = String(parseInt(day, 10) || 0).padStart(2, '0');
    var mStr = String(parseInt(month, 10) || 0).padStart(2, '0');
    var yStr = String(parseInt(year, 10) || 0).padStart(4, '0');
    return digitRoot(sumDigits(dStr + mStr + yStr));
  }

  function calcPersonalYear(day, month, targetYear) {
    var yr = targetYear ? (parseInt(targetYear, 10) || new Date().getFullYear()) : new Date().getFullYear();
    var dStr = String(parseInt(day, 10) || 0).padStart(2, '0');
    var mStr = String(parseInt(month, 10) || 0).padStart(2, '0');
    var yStr = String(yr).padStart(4, '0');
    return digitRoot(sumDigits(dStr + mStr + yStr));
  }

  function calcPersonalMonth(personalYear, calendarMonth) {
    return digitRoot((parseInt(personalYear, 10) || 0) + (parseInt(calendarMonth, 10) || 0));
  }

  function calcPersonalDay(personalYear, personalMonth, targetDay, targetMonth, targetYear) {
    var dStr = String(parseInt(targetDay, 10) || 0).padStart(2, '0');
    var mStr = String(parseInt(targetMonth, 10) || 0).padStart(2, '0');
    var yStr = String(parseInt(targetYear, 10) || 0).padStart(4, '0');
    return digitRoot((parseInt(personalYear, 10) || 0) + (parseInt(personalMonth, 10) || 0) + sumDigits(dStr + mStr + yStr));
  }

  function calcPersonalCyclesForDate(birthDay, birthMonth, targetDay, targetMonth, targetYear) {
    var py = calcPersonalYear(birthDay, birthMonth, targetYear);
    var pm = calcPersonalMonth(py, targetMonth);
    var pd = calcPersonalDay(py, pm, targetDay, targetMonth, targetYear);
    return {
      label: 'Personal Year / Month / Day',
      personalYear: py,
      personalMonth: pm,
      personalDay: pd
    };
  }

  function calcLoShuDobOnly(day, month, year) {
    var dobStr = String(parseInt(day, 10) || 0).padStart(2, '0')
      + String(parseInt(month, 10) || 0).padStart(2, '0')
      + String(parseInt(year, 10) || 0).padStart(4, '0');
    var counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 };
    for (var i = 0; i < dobStr.length; i++) {
      var ch = dobStr.charAt(i);
      if (ch >= '1' && ch <= '9') counts[parseInt(ch, 10)]++;
    }
    var present = [];
    var missing = [];
    var repeated = {};
    for (var d = 1; d <= 9; d++) {
      if (counts[d] > 0) present.push(d);
      else missing.push(d);
      if (counts[d] >= 2) repeated[d] = counts[d];
    }
    return { dobDigitsStr: dobStr, counts: counts, present: present, missing: missing, repeated: repeated };
  }

  function calcChaldeanNameNumber(name) {
    var s = String(name || '').toUpperCase();
    var compound = 0;
    for (var i = 0; i < s.length; i++) {
      var ch = s.charAt(i);
      if (CHALDEAN_MAP[ch]) compound += CHALDEAN_MAP[ch];
    }
    return { compound: compound, root: digitRoot(compound) };
  }

  function calcPythagoreanNameNumber(name) {
    var s = String(name || '').toUpperCase();
    var compound = 0;
    for (var i = 0; i < s.length; i++) {
      var ch = s.charAt(i);
      if (PYTHAGOREAN_MAP[ch]) compound += PYTHAGOREAN_MAP[ch];
    }
    return { compound: compound, root: digitRoot(compound) };
  }

  function reduceSingleDigit(num) {
    return digitRoot(Math.abs(parseInt(num, 10) || 0));
  }

  function normalizeGender(gender) {
    if (gender === null || gender === undefined) return null;
    var g = String(gender).trim().toLowerCase();
    if (g === 'male' || g === 'm') return 'male';
    if (g === 'female' || g === 'f') return 'female';
    return null;
  }

  function calculateKuaDetails(birthYear, gender) {
    var yr = parseInt(birthYear, 10);
    if (!yr || isNaN(yr)) {
      return {
        status: 'INVALID_YEAR',
        kuaNumber: null,
        kua_number: null,
        rawKua: null,
        raw_kua: null,
        remappedFromFive: false,
        yearDigitRoot: null,
        year_digit_sum: null,
        gender: normalizeGender(gender),
        display: KUA_NEEDS_GENDER_TEXT,
        display_text: KUA_NEEDS_GENDER_TEXT,
        element: null,
        trigram: null,
        group: null,
        groupShort: null,
        elementGroup: KUA_NEEDS_GENDER_TEXT,
        element_group_label: KUA_NEEDS_GENDER_TEXT,
        directionSummary: KUA_NEEDS_GENDER_TEXT,
        deskDirection: KUA_NEEDS_GENDER_TEXT,
        ruleNote: KUA_RULE_TEXT,
        rule_text: KUA_RULE_TEXT
      };
    }

    var yrStr = String(yr).padStart(4, '0');
    var sumDigits = 0;
    for (var i = 0; i < yrStr.length; i++) {
      var ch = yrStr.charAt(i);
      if (ch >= '0' && ch <= '9') {
        sumDigits += parseInt(ch, 10);
      }
    }
    var x = reduceSingleDigit(sumDigits);
    var normGender = normalizeGender(gender);

    if (!normGender) {
      return {
        status: 'NEEDS_GENDER',
        kuaNumber: null,
        kua_number: null,
        rawKua: null,
        raw_kua: null,
        remappedFromFive: false,
        yearDigitRoot: x,
        year_digit_sum: x,
        gender: null,
        display: KUA_NEEDS_GENDER_TEXT,
        display_text: KUA_NEEDS_GENDER_TEXT,
        element: null,
        trigram: null,
        group: null,
        groupShort: null,
        elementGroup: KUA_NEEDS_GENDER_TEXT,
        element_group_label: KUA_NEEDS_GENDER_TEXT,
        directionSummary: KUA_NEEDS_GENDER_TEXT,
        deskDirection: KUA_NEEDS_GENDER_TEXT,
        ruleNote: KUA_RULE_TEXT,
        rule_text: KUA_RULE_TEXT
      };
    }

    var rawKua = normGender === 'male'
      ? reduceSingleDigit(11 - x)
      : reduceSingleDigit(4 + x);
    var finalKua = rawKua === 5 ? (normGender === 'male' ? 2 : 8) : rawKua;
    var meta = KUA_METADATA[finalKua];

    return {
      status: 'OK',
      kuaNumber: finalKua,
      kua_number: finalKua,
      rawKua: rawKua,
      raw_kua: rawKua,
      remappedFromFive: rawKua === 5,
      yearDigitRoot: x,
      year_digit_sum: x,
      gender: normGender,
      display: String(finalKua),
      display_text: String(finalKua),
      element: meta.element,
      trigram: meta.trigram,
      group: meta.group,
      groupShort: meta.groupShort,
      elementGroup: meta.elementGroup,
      element_group_label: meta.elementGroup,
      directionSummary: meta.directionSummary,
      deskDirection: meta.deskDirection,
      success: meta.success,
      health: meta.health,
      relationship: meta.relationship,
      stability: meta.stability,
      ruleNote: KUA_RULE_TEXT,
      rule_text: KUA_RULE_TEXT
    };
  }

  function calculateKua(birthYear, gender) {
    var details = calculateKuaDetails(birthYear, gender);
    return details.kuaNumber !== null ? details.kuaNumber : KUA_NEEDS_GENDER_TEXT;
  }

  return {
    KUA_RULE_TEXT: KUA_RULE_TEXT,
    KUA_NEEDS_GENDER_TEXT: KUA_NEEDS_GENDER_TEXT,
    KUA_METADATA: KUA_METADATA,
    CHALDEAN_MAP: CHALDEAN_MAP,
    PYTHAGOREAN_MAP: PYTHAGOREAN_MAP,
    digitRoot: digitRoot,
    sumDigits: sumDigits,
    calcDriver: calcDriver,
    calcBhagyank: calcBhagyank,
    calcPersonalYear: calcPersonalYear,
    calcPersonalMonth: calcPersonalMonth,
    calcPersonalDay: calcPersonalDay,
    calcPersonalCyclesForDate: calcPersonalCyclesForDate,
    calcLoShuDobOnly: calcLoShuDobOnly,
    calcChaldeanNameNumber: calcChaldeanNameNumber,
    calcPythagoreanNameNumber: calcPythagoreanNameNumber,
    normalizeGender: normalizeGender,
    calculateKuaDetails: calculateKuaDetails,
    calculateKua: calculateKua
  };
});
