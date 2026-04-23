from PIL import Image   # Pillow — opens images
import pypdf            # reads and writes PDFs
import os               # file path tools (built-in)


# =========================
# IMAGE CLEANER
# =========================
def clean_image(src, dst):
    try:
        img = Image.open(src)

        # Convert incompatible modes
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Copy pixel data only (removes EXIF)
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))

        clean.save(dst)
        print(f"[CLEAN] Image → {dst}")

    except Exception as e:
        print(f"[ERROR] Image failed: {src} | {e}")


# =========================
# PDF CLEANER
# =========================
def clean_pdf(src, dst):
    try:
        reader = pypdf.PdfReader(src)
        writer = pypdf.PdfWriter()

        # Handle encrypted PDFs
        if reader.is_encrypted:
            reader.decrypt("")

        # Copy pages
        for page in reader.pages:
            writer.add_page(page)

        # FIX 1: Explicitly blank every known metadata field
        # (passing an empty dict {} doesn't reliably clear existing fields
        # in all pypdf versions — setting each key to "" does)
        writer.add_metadata({
            "/Author":   "",
            "/Creator":  "",
            "/Producer": "",
            "/Title":    "",
            "/Subject":  "",
            "/Keywords": "",
        })

        with open(dst, "wb") as f:
            writer.write(f)

        print(f"[CLEAN] PDF → {dst}")

    except Exception as e:
        print(f"[ERROR] PDF failed: {src} | {e}")


# =========================
# DISPATCHER
# =========================
def clean_document(src, dst=None):
    # FIX 2: Validate that the source file actually exists before doing anything
    if not os.path.exists(src):
        print(f"[ERROR] File not found: {src}")
        return None

    if dst is None:
        root, ext = os.path.splitext(src)
        dst = f"{root}_clean{ext}"

    ext = os.path.splitext(src)[1].lower()

    if ext in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"):
        clean_image(src, dst)

    elif ext == ".pdf":
        clean_pdf(src, dst)

    else:
        # Unknown type → safe copy
        try:
            with open(src, "rb") as f:
                data = f.read()
            with open(dst, "wb") as f:
                f.write(data)

            print(f"[WARN] Unknown type copied → {dst}")

        except Exception as e:
            print(f"[ERROR] Copy failed: {src} | {e}")

    return dst


# =========================
# BATCH PROCESSOR
# =========================
def process_folder(src_folder, dst_folder):
    if not os.path.exists(src_folder):
        print(f"[ERROR] Source folder not found: {src_folder}")
        return

    os.makedirs(dst_folder, exist_ok=True)

    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

    if not files:
        print(f"[WARN] No files found in: {src_folder}")
        return

    print(f"[INFO] Found {len(files)} file(s) to process.")

    for file in files:
        src_path = os.path.join(src_folder, file)
        dst_path = os.path.join(dst_folder, "clean_" + file)
        clean_document(src_path, dst_path)


# =========================
# ENTRY POINT (TEST / RUN)
# =========================
if __name__ == "__main__":

    # === YOUR FOLDERS (RAW STRINGS) ===
    SRC_FOLDER = r"C:\Users\valla\OneDrive - BENNETT UNIVERSITY\Desktop\CipherChain\newdoc"
    DST_FOLDER = r"C:\Users\valla\OneDrive - BENNETT UNIVERSITY\Desktop\CipherChain\cleandocs"

    print("\n[INFO] Starting batch cleaning...\n")

    process_folder(SRC_FOLDER, DST_FOLDER)

    print("\n[INFO] Cleaning complete.\n")