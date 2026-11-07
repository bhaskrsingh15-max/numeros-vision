import subprocess
import os
import re

PATTERNS = [
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z-_]{35}")),
    ("OpenAI API Key", re.compile(r"sk-[a-zA-Z0-9]{20,}")),
    ("Razorpay Key ID", re.compile(r"rzp_(?:test|live)_[a-zA-Z0-9]{14}")),
    ("Razorpay Secret Pattern", re.compile(r"(?:razorpay_key_secret|RZP_KEY_SECRET|key_secret)\s*[:=]\s*['\"]([a-zA-Z0-9]{20,})['\"]")),
    ("Web3Forms Access Key", re.compile(r"(?:web3forms|access_key).*?([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", re.IGNORECASE)),
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub Token", re.compile(r"gh[pousr]_[0-9a-zA-Z]{36}")),
    ("Private Key", re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH|PGP|ENCRYPTED)?\s*PRIVATE KEY-----")),
    ("Admin / Hardcoded Passwords", re.compile(r"(?:NumerosVisionAdmin2026!|AnveilCharm@2026!)")),
    ("Fast2SMS API Key", re.compile(r"(?:fast2sms_api_key|FAST2SMS_API_KEY)\s*[:=]\s*['\"]([a-zA-Z0-9]{30,})['\"]")),
    ("Generic High-Entropy Secret", re.compile(r"(?:secret_key|api_secret|auth_secret)\s*[:=]\s*['\"]([a-zA-Z0-9_-]{32,})['\"]", re.IGNORECASE)),
]

IGNORE_EXTENSIONS = {
    ".pyc", ".png", ".jpg", ".jpeg", ".ico", ".webp", ".svg", ".pdf",
    ".zip", ".tar", ".gz", ".woff", ".woff2", ".ttf", ".eot", ".lock"
}
IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist_cloudflare_pages"}

def scan_working_tree():
    findings = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in IGNORE_EXTENSIONS:
                continue
            fp = os.path.join(root, f)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    for line_no, line in enumerate(fh, 1):
                        for label, regex in PATTERNS:
                            m = regex.search(line)
                            if m:
                                # Mask the matched secret
                                raw_match = m.group(0)
                                if len(raw_match) > 12:
                                    masked = raw_match[:4] + "..." + raw_match[-4:]
                                else:
                                    masked = raw_match[:2] + "..."
                                findings.append({
                                    "source": "Working Tree",
                                    "file": fp,
                                    "line": line_no,
                                    "type": label,
                                    "preview": masked
                                })
            except Exception:
                pass
    return findings

def scan_git_history():
    findings = []
    try:
        proc = subprocess.run(
            ["git", "log", "--all", "-p", "--full-history"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        current_commit = "unknown"
        current_file = "unknown"
        for line in proc.stdout.splitlines():
            if line.startswith("commit "):
                current_commit = line.split()[1][:7]
            elif line.startswith("+++ b/"):
                current_file = line[6:]
            elif line.startswith("+") and not line.startswith("+++"):
                added_content = line[1:]
                for label, regex in PATTERNS:
                    m = regex.search(added_content)
                    if m:
                        raw_match = m.group(0)
                        masked = raw_match[:4] + "..." + raw_match[-4:] if len(raw_match) > 12 else raw_match[:2] + "..."
                        findings.append({
                            "source": f"Git Commit {current_commit}",
                            "file": current_file,
                            "type": label,
                            "preview": masked
                        })
    except Exception as e:
        print(f"Error scanning git history: {e}")
    return findings

if __name__ == "__main__":
    print("--- STARTING WORKSPACE & GIT HISTORY SECRETS SWEEP ---")
    tree_findings = scan_working_tree()
    print(f"Working tree scan finished: {len(tree_findings)} potential matches.")
    hist_findings = scan_git_history()
    print(f"Git history scan finished: {len(hist_findings)} potential matches.")

    print("\n--- WORKING TREE FINDINGS ---")
    for f in tree_findings:
        print(f"[{f['type']}] {f['file']}:{f['line']} -> {f['preview']}")

    print("\n--- GIT HISTORY FINDINGS ---")
    # Deduplicate history findings by commit+file+type
    seen = set()
    for f in hist_findings:
        key = (f['source'], f['file'], f['type'])
        if key not in seen:
            seen.add(key)
            print(f"[{f['type']}] {f['source']} in {f['file']} -> {f['preview']}")
