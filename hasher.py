# hasher.py

import hashlib
import hmac


# =========================
# HASH FUNCTION (FILE)
# =========================
def hash_file(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:
        while chunk := f.read(65536):  # 64 KB chunks
            sha256.update(chunk)

    return sha256.hexdigest()


# =========================
# HASH FUNCTION (BYTES) ✅ ADDED
# =========================
def hash_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()


# =========================
# SAFE COMPARISON
# =========================
def safe_compare(hash_a, hash_b):
    return hmac.compare_digest(
        hash_a.encode("utf-8"),
        hash_b.encode("utf-8")
    )