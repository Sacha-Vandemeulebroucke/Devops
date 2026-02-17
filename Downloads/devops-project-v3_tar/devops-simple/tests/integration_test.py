"""
Tests d'intégration — lancer avec : python tests/integration_test.py
La stack doit être démarrée : docker compose up -d
"""
import urllib.request
import urllib.error
import json
import sys
import time

BASE = "http://localhost:8080"

def get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=5) as r:
            return r.status, json.loads(r.read())
    except Exception as e:
        return None, str(e)

def wait_ready(retries=20):
    print("Attente de l'API...", end="", flush=True)
    for _ in range(retries):
        status, _ = get("/health")
        if status == 200:
            print(" OK")
            return True
        print(".", end="", flush=True)
        time.sleep(2)
    print(" TIMEOUT")
    return False

def test(name, path, expected_key):
    status, data = get(path)
    ok = status == 200 and expected_key in data
    print(f"  {'✓' if ok else '✗'} {name}")
    if not ok:
        print(f"    → status={status}, data={data}")
    return ok

if not wait_ready():
    sys.exit(1)

print("\nTests:")
results = [
    test("GET /health",   "/health", "status"),
    test("GET /",         "/",       "message"),
]

passed = sum(results)
print(f"\n{passed}/{len(results)} tests réussis")
sys.exit(0 if all(results) else 1)
