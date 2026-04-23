"""
cipherchain_platform.py
Core logic for CipherChain — register() and verify().
"""

import os
import time

from blockchain import Blockchain
from hasher import hash_file, safe_compare
from metadata_cleaner import clean_document

# Single shared blockchain instance
_blockchain = Blockchain()


def register(filepath: str) -> dict:
    print("\n" + "=" * 55)
    print("  CIPHERCHAIN — REGISTER")
    print("=" * 55)

    if not os.path.exists(filepath):
        return {"success": False, "error": f"File not found: {filepath}"}

    # Step 1 — Clean
    print(f"\n[1/4] Stripping metadata from: {filepath}")
    clean_path = clean_document(filepath)

    # Step 2 — Hash
    print(f"[2/4] Computing SHA-256 hash...")
    doc_hash = hash_file(clean_path)
    print(f"      Hash → {doc_hash}")

    # Step 3 — Check duplicate
    print(f"[3/4] Checking for existing registration...")
    existing = _blockchain.find_hash(doc_hash)

    if existing:
        print(f"      ⚠ Already registered in Block #{existing.index}")
        return {
            "success": False,
            "error": "Document already registered",
            "block_index": existing.index,
            "document_hash": doc_hash,
        }

    # Step 4 — Mine block
    print(f"[4/4] Mining block...")
    start = time.time()
    block = _blockchain.add_block(doc_hash)
    elapsed = time.time() - start

    print(f"\n  ✅ REGISTERED SUCCESSFULLY")
    print(f"     Block Index  : #{block.index}")
    print(f"     Document Hash: {doc_hash}")
    print(f"     Block Hash   : {block.hash}")
    print(f"     Nonce        : {block.nonce}")
    print(f"     Mined in     : {elapsed:.2f}s")
    print("=" * 55 + "\n")

    return {
        "success": True,
        "block_index": block.index,
        "document_hash": doc_hash,
        "block_hash": block.hash,
        "nonce": block.nonce,
        "clean_file": clean_path,
    }


def verify(filepath: str) -> dict:
    print("\n" + "=" * 55)
    print("  CIPHERCHAIN — VERIFY")
    print("=" * 55)

    if not os.path.exists(filepath):
        return {"authentic": False, "error": f"File not found: {filepath}"}

    # Step 1 — Clean
    print(f"\n[1/3] Stripping metadata from: {filepath}")
    clean_path = clean_document(filepath)

    # Step 2 — Hash
    print(f"[2/3] Computing SHA-256 hash...")
    doc_hash = hash_file(clean_path)
    print(f"      Hash → {doc_hash}")

    # Step 3 — Search blockchain
    print(f"[3/3] Searching blockchain...")
    block = _blockchain.find_hash(doc_hash)

    if block:
        registered_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(block.timestamp)
        )

        print(f"\n  ✅ STATUS: AUTHENTIC")
        print(f"     Confidence : HIGH")
        print(f"     Integrity  : VERIFIED")
        print(f"     Found in Block #{block.index}")
        print(f"     Registered : {registered_time}")
        print("=" * 55 + "\n")

        return {
            "authentic": True,
            "block_index": block.index,
            "document_hash": doc_hash,
        }

    else:
        print(f"\n  ❌ STATUS: NOT AUTHENTIC")
        print(f"     Integrity  : COMPROMISED")
        print("     Document has been altered or not registered")
        print("=" * 55 + "\n")

        return {
            "authentic": False,
            "document_hash": doc_hash,
        }


def chain_status():
    _blockchain.print_chain()
    return {
        "valid": _blockchain.is_valid(),
        "length": len(_blockchain.chain),
    }