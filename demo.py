"""
demo.py
Whistleblower simulation:
Generate hash → store original → also show tampered hash for testing
"""

import os

# RESET BLOCKCHAIN BEFORE IMPORT
if os.path.exists("chain.json"):
    os.remove("chain.json")

from blockchain import Blockchain
from metadata_cleaner import clean_document
from hasher import hash_file


# =========================
# FILE PATHS
# =========================
ORIGINAL = r"C:\Users\valla\OneDrive - BENNETT UNIVERSITY\Desktop\CipherChain\original.txt"
TAMPERED = r"C:\Users\valla\OneDrive - BENNETT UNIVERSITY\Desktop\CipherChain\tampered.txt"


def main():

    chain = Blockchain()

    print("\n" + "█" * 60)
    print("  CIPHERCHAIN — Whistleblower Simulation")
    print("█" * 60)

    # STEP 1 — Clean + hash ORIGINAL
    print("\n[STEP 1] Processing ORIGINAL document...")
    clean_original = clean_document(ORIGINAL)
    original_hash = hash_file(clean_original)

    print("\n  Original Document Hash:")
    print(f"  {original_hash}")

    # STEP 2 — Store ONLY original hash
    print("\n[STEP 2] Publishing ORIGINAL hash to blockchain...")
    block = chain.add_block(original_hash)
    print(f"  Stored in Block #{block.index}")

    # STEP 3 — Generate TAMPERED hash (NOT stored)
    print("\n[STEP 3] Processing TAMPERED document (for testing only)...")
    clean_tampered = clean_document(TAMPERED)
    tampered_hash = hash_file(clean_tampered)

    print("\n  Tampered Document Hash:")
    print(f"  {tampered_hash}")

    # STEP 4 — Create journalist packet
    print("\n[STEP 4] Creating journalist packet...")

    output_file = "journalist_packet.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("CIPHERCHAIN — JOURNALIST PACKET\n")
        f.write("=" * 50 + "\n\n")

        f.write("DOCUMENT PATH (ORIGINAL):\n")
        f.write(f"{ORIGINAL}\n\n")

        f.write("VALID HASH (BLOCKCHAIN):\n")
        f.write(f"{original_hash}\n\n")

        f.write("TEST HASH (TAMPERED FILE):\n")
        f.write(f"{tampered_hash}\n\n")

        f.write("INSTRUCTIONS:\n")
        f.write("1. Open CipherChain UI\n")
        f.write("2. Paste VALID HASH → should show AUTHENTIC\n")
        f.write("3. Paste TEST HASH → should show NOT AUTHENTIC\n")

    print(f"  📄 Packet created: {output_file}")

    # Auto-open file (Windows)
    try:
        os.startfile(output_file)
    except:
        print("  (Could not auto-open file)")

    # FINAL OUTPUT
    print("\n" + "━" * 60)
    print("  DATA SENT TO JOURNALIST")
    print("━" * 60)

    print(f"\n  📄 Original Document:")
    print(f"  {ORIGINAL}")

    print(f"\n  🔐 Valid Hash (stored on blockchain):")
    print(f"  {original_hash}")

    print(f"\n  ⚠️ Tampered Hash (NOT stored):")
    print(f"  {tampered_hash}")

    print("\n" + "█" * 60)
    print("  NEXT STEP: Use UI to verify both hashes")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    main()