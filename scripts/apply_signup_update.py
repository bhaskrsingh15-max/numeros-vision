def update_signup_html():
    path = 'app/static/signup.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    target = """    /* DPDP & GDPR Unbundled Consent Box */
    .dpdp-box {
      background: #F7F3EA;
      border-radius: 14px;
      padding: 16px 18px;
      font-size: 0.8rem;
      color: #523E28;
      line-height: 1.55;
      margin-bottom: 22px;
      border: 1.5px solid rgba(201, 162, 39, 0.3);
    }
    .dpdp-box-header {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.15rem;
      color: #8B6914;
      font-weight: 700;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dpdp-consent-row {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(201, 162, 39, 0.25);
    }
    .dpdp-consent-row:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }
    .dpdp-consent-row input[type="checkbox"] {
      margin-top: 3px;
      width: 17px;
      height: 17px;
      accent-color: #8B6914;
      cursor: pointer;
      flex-shrink: 0;
    }
    .dpdp-consent-label {
      cursor: pointer;
      flex: 1;
    }
    .dpdp-consent-label strong {
      color: #8B6914;
    }
    .dpdp-consent-label a {
      color: #8B6914;
      text-decoration: underline;
    }
    .dpdp-safety-note {
      font-size: 0.72rem;
      color: #7A654D;
      background: rgba(255, 255, 255, 0.65);
      padding: 8px 12px;
      border-radius: 8px;
      margin-top: 10px;
      line-height: 1.45;
    }"""

    replacement = """    /* DPDP & GDPR Unbundled Consent Box */
    .dpdp-box {
      background: #F7F3EA;
      border-radius: 12px;
      padding: 12px 14px;
      font-size: 0.74rem;
      color: #523E28;
      line-height: 1.45;
      margin-bottom: 20px;
      border: 1.5px solid rgba(201, 162, 39, 0.3);
      box-sizing: border-box;
    }
    .dpdp-box-header {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.05rem;
      color: #8B6914;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dpdp-consent-row {
      display: flex;
      gap: 10px;
      align-items: flex-start;
      margin-bottom: 8px;
      padding-bottom: 8px;
      border-bottom: 1px dashed rgba(201, 162, 39, 0.25);
    }
    .dpdp-consent-row:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }
    .dpdp-consent-row input[type="checkbox"] {
      margin-top: 2px;
      width: 15px;
      height: 15px;
      accent-color: #8B6914;
      cursor: pointer;
      flex-shrink: 0;
    }
    .dpdp-consent-label {
      cursor: pointer;
      flex: 1;
      font-size: 0.74rem !important;
      line-height: 1.45 !important;
      color: #523E28 !important;
      text-transform: none !important;
      letter-spacing: normal !important;
      font-weight: 400 !important;
      margin-bottom: 0 !important;
    }
    .dpdp-consent-label strong {
      color: #8B6914;
      font-weight: 700;
    }
    .dpdp-consent-label a {
      color: #8B6914;
      text-decoration: underline;
    }
    .dpdp-safety-note {
      font-size: 0.70rem !important;
      color: #7A654D;
      background: rgba(255, 255, 255, 0.65);
      padding: 6px 10px;
      border-radius: 8px;
      margin-top: 8px;
      line-height: 1.4;
    }"""

    if target in content:
        content = content.replace(target, replacement)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("SUCCESS: signup.html DPDP styling updated.")
    else:
        print("ERROR: target block not found in signup.html")

if __name__ == '__main__':
    update_signup_html()
