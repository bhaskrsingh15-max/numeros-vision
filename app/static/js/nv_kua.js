/**
 * NUMEROS VISION — CANONICAL BROWSER KUA ENGINE
 * ==============================================
 * Approved Formula:
 * 1. Sum all four digits of the calendar birth year, reduce to single digit = x.
 *    [Calendar birth year — PENDING CONFIRMATION on early-year births.]
 * 2. Male: 11 - x, then reduce to single digit.
 *    Female: 4 + x, then reduce to single digit.
 *    Same rule for every century; zero pre/post-2000 branching.
 * 3. Kua 5 maps to 2 for male and 8 for female [PENDING CONFIRMATION].
 * 4. Derive element, trigram, and East/West group from the final Kua number.
 * 5. Missing or unrecognized gender returns display='Kua needs gender' — never guesses.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.NVKua = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
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

  function reduceSingleDigit(num) {
    var n = Math.abs(parseInt(num, 10) || 0);
    while (n > 9) {
      var sum = 0;
      var s = String(n);
      for (var i = 0; i < s.length; i++) {
        sum += parseInt(s.charAt(i), 10) || 0;
      }
      n = sum;
    }
    return n;
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
    normalizeGender: normalizeGender,
    calculateKuaDetails: calculateKuaDetails,
    calculateKua: calculateKua
  };
});
