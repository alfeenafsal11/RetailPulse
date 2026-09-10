"""Reproducibility test: generate twice and compare MD5 hashes."""
import hashlib
import os
import subprocess
import sys


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
    files = ["customers.csv", "products.csv", "transactions.csv"]

    # Record first-run hashes
    print("Recording hashes from current files...")
    hashes_before = {}
    for f in files:
        p = os.path.join(data_dir, f)
        hashes_before[f] = md5(p)
        print(f"  Run 1 - {f}: {hashes_before[f]}")

    # Re-run generator
    print("\nRe-generating with seed=42...")
    gen_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "data_generator.py")
    result = subprocess.run(
        [sys.executable, gen_script],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        print("FAIL: Generator returned non-zero")
        print(result.stderr)
        return False

    # Check hashes again
    print("\nComparing hashes...")
    all_match = True
    for f in files:
        p = os.path.join(data_dir, f)
        h = md5(p)
        match = h == hashes_before[f]
        status = "MATCH" if match else "MISMATCH"
        print(f"  Run 2 - {f}: {h} [{status}]")
        if not match:
            all_match = False

    result_str = "PASS" if all_match else "FAIL"
    print(f"\nReproducibility: {result_str}")
    return all_match


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
