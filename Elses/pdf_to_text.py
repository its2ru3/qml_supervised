### Not Useful, not reliable 

import fitz  # pymupdf
import os
from pathlib import Path

INPUT_FILE = "paper_main.pdf" # first copy the pdf to this directory
OUTPUT_DIR = "converted"

# Create directories
Path(OUTPUT_DIR).mkdir(exist_ok=True)
Path(f"{OUTPUT_DIR}/images").mkdir(exist_ok=True)
Path(f"{OUTPUT_DIR}/pages").mkdir(exist_ok=True)
Path(f"{OUTPUT_DIR}/chunks").mkdir(exist_ok=True)


def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    chunk_size = 1000  # characters
    chunk_buffer = ""
    chunk_id = 0

    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        full_text += text + "\n"

        # Save page-wise text
        with open(f"{OUTPUT_DIR}/pages/page_{page_num}.txt", "w", encoding="utf-8") as f:
            f.write(text)

        # Extract images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            if pix.n < 5:
                pix.save(f"{OUTPUT_DIR}/images/page{page_num}_{img_index}.png")
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(f"{OUTPUT_DIR}/images/page{page_num}_{img_index}.png")

        # Chunking logic
        chunk_buffer += text
        while len(chunk_buffer) >= chunk_size:
            chunk = chunk_buffer[:chunk_size]
            chunk_buffer = chunk_buffer[chunk_size:]

            with open(f"{OUTPUT_DIR}/chunks/chunk_{chunk_id}.txt", "w", encoding="utf-8") as f:
                f.write(chunk)

            chunk_id += 1

    # Save remaining chunk
    if chunk_buffer:
        with open(f"{OUTPUT_DIR}/chunks/chunk_{chunk_id}.txt", "w", encoding="utf-8") as f:
            f.write(chunk_buffer)

    # Save full text
    with open(f"{OUTPUT_DIR}/full_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("✅ Extraction complete!")
    print(f"📂 Output saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    extract_pdf(INPUT_FILE)