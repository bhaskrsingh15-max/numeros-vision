"""
Update marketing-analytics.js with Android GTM v5 bridge
and update app/main.py assetlinks endpoint
"""
import os

MAIN_PY = os.path.join("app", "main.py")
with open(MAIN_PY, "r", encoding="utf-8") as f:
    main_code = f.read()

old_assetlinks = '''@app.get("/.well-known/assetlinks.json", include_in_schema=False)
def asset_links():
    # UPDATE: Replace sha256_cert_fingerprints with your actual keystore fingerprint
    # Generate with: keytool -list -v -keystore your-key.jks
    return JSONResponse([{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.numerosvision.app",
            "sha256_cert_fingerprints": [
                "REPLACE_WITH_YOUR_KEYSTORE_SHA256_FINGERPRINT"
            ]
        }
    }])'''

new_assetlinks = '''@app.get("/.well-known/assetlinks.json", include_in_schema=False)
def asset_links():
    path = os.path.join(STATIC_DIR, ".well-known", "assetlinks.json")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return JSONResponse([{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.numerosvision.app",
            "sha256_cert_fingerprints": [
                "14:6D:E9:01:07:52:07:71:02:85:63:F6:44:9F:65:4F:92:49:EE:12:12:F1:C7:A7:F3:33:43:24:B9:4C:6D:8F"
            ]
        }
    }])'''

if "STATIC_DIR, \".well-known\", \"assetlinks.json\"" not in main_code:
    main_code = main_code.replace(old_assetlinks, new_assetlinks)
    with open(MAIN_PY, "w", encoding="utf-8") as f:
        f.write(main_code)
    print("Updated app/main.py assetlinks endpoint.")

# Update marketing-analytics.js
ANALYTICS_JS = os.path.join("app", "static", "js", "marketing-analytics.js")
with open(ANALYTICS_JS, "r", encoding="utf-8") as f:
    js_code = f.read()

bridge_snippet = '''  // Google Tag Manager (v5) Android App Native Bridge
  // Forwards web dataLayer events to Android app TagManagerAnalyticsBridge
  const originalDataLayerPush = window.dataLayer.push.bind(window.dataLayer);
  window.dataLayer.push = function() {
    for (let i = 0; i < arguments.length; i++) {
      const item = arguments[i];
      if (item && typeof item === 'object') {
        const eventName = item.event || item[0] || 'dataLayer_push';
        if (window.AndroidBridge && typeof window.AndroidBridge.logEvent === 'function') {
          try {
            window.AndroidBridge.logEvent(String(eventName), JSON.stringify(item));
          } catch (e) {
            console.debug('[AndroidBridge] GTM event forward error:', e);
          }
        }
      }
    }
    return originalDataLayerPush.apply(window.dataLayer, arguments);
  };'''

if "Google Tag Manager (v5) Android App Native Bridge" not in js_code:
    js_code = js_code.replace(
        "window.dataLayer = window.dataLayer || [];",
        "window.dataLayer = window.dataLayer || [];\n" + bridge_snippet
    )
    with open(ANALYTICS_JS, "w", encoding="utf-8") as f:
        f.write(js_code)
    print("Updated app/static/js/marketing-analytics.js with AndroidBridge forwarder.")
else:
    print("marketing-analytics.js already contains Android GTM bridge.")
