import subprocess, sys, time, urllib.request, os

sys.stdout.reconfigure(encoding='utf-8')
env = dict(os.environ)
env['PYTHONPATH'] = os.getcwd()

print("Starting local uvicorn server on http://127.0.0.1:8000 ...")
server_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

server_ready = False
start_time = time.time()
while time.time() - start_time < 20:
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/health", headers={"User-Agent": "HealthCheck"})
        with urllib.request.urlopen(req, timeout=1) as resp:
            if resp.status in (200, 404):
                server_ready = True
                print(f"Server ready in {round(time.time() - start_time, 2)}s!")
                break
    except Exception:
        # Also try root
        try:
            req = urllib.request.Request("http://127.0.0.1:8000/", headers={"User-Agent": "HealthCheck"})
            with urllib.request.urlopen(req, timeout=1) as resp:
                server_ready = True
                print(f"Server ready in {round(time.time() - start_time, 2)}s!")
                break
        except Exception:
            pass
    time.sleep(0.5)

if not server_ready:
    print("Failed to start server within 20s. Exiting.")
    server_proc.kill()
    sys.exit(1)

print("\n--- RUNNING test_api_cyber_security_suite.py ---")
test_proc = subprocess.run(
    [sys.executable, "tests/test_api_cyber_security_suite.py"],
    env=env,
    capture_output=True,
    text=True,
    errors='ignore'
)

print(test_proc.stdout)
if test_proc.stderr:
    print(test_proc.stderr)

print(f"\nTest finished with exit code: {test_proc.returncode}")

print("Terminating server...")
server_proc.terminate()
try:
    server_proc.wait(timeout=3)
except subprocess.TimeoutExpired:
    server_proc.kill()

sys.exit(test_proc.returncode)
