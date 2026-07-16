from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def info(msg):
    print(f"[INFO] {msg}")

def ok(msg):
    print(f"[ OK ] {msg}")

def fail(msg):
    print(f"[FAIL] {msg}")

def file_exists(path):
    return Path(path).exists()
