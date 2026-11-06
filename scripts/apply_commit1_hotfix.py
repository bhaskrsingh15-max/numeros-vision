import os
import re

WORKER_PATH = os.path.join("app", "static", "_worker.js")
LOGIN_PATH = os.path.join("app", "static", "login.html")
GW_PATH = os.path.join("app", "static", "js", "nv_payment_gateway.js")

def patch_payment_gateway_js():
    with open(GW_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    target = "const keyId = (orderData && (orderData.key_id || orderData.key)) || 'rzp_test_TwcQLlhj2djlqG';"
    replacement = "const keyId = orderData && (orderData.key_id || orderData.key);"
    if target in content:
        content = content.replace(target, replacement)
        with open(GW_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print("nv_payment_gateway.js: hardcoded key removed successfully!")
    else:
        print("nv_payment_gateway.js: key already cleaned.")

if __name__ == "__main__":
    patch_payment_gateway_js()

def patch_pdf_links():
    dash_path = os.path.join("app", "static", "dashboard.html")
    with open(dash_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = re.sub(
        r"['\"]/reports/Numeros_Vision_[^'\"]+\.pdf['\"]",
        "'/samples/Numeros_Vision_Sample_Dossier_Fictional.pdf'",
        text
    )
    text = re.sub(
        r"['\"]/static/reports/Numeros_Vision_[^'\"]+\.pdf['\"]",
        "'/samples/Numeros_Vision_Sample_Dossier_Fictional.pdf'",
        text
    )
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("dashboard.html: PDF links redirected to /samples/")

    gw_path = os.path.join("app", "static", "js", "nv_payment_gateway.js")
    with open(gw_path, "r", encoding="utf-8") as f:
        gw_text = f.read()

    gw_text = re.sub(
        r"['\"]/reports/Numeros_Vision_[^'\"]+\.pdf['\"]",
        "'/samples/Numeros_Vision_Sample_Dossier_Fictional.pdf'",
        gw_text
    )
    with open(gw_path, "w", encoding="utf-8") as f:
        f.write(gw_text)
    print("nv_payment_gateway.js: PDF links redirected to /samples/")

if __name__ == "__main__":
    patch_pdf_links()
