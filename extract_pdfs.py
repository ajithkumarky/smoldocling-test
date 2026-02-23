"""Extract text from PDF files using SmolDocling."""

import argparse
import re
import torch
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
from transformers import AutoProcessor, AutoModelForVision2Seq
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID = "ds4sd/SmolDocling-256M-preview"


def extract_doctags(model, processor, image: Image.Image) -> str:
    """Run SmolDocling inference and return raw doctags string."""
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Convert this page to docling."},
            ],
        },
    ]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt").to(DEVICE)

    generated_ids = model.generate(**inputs, max_new_tokens=8192)
    prompt_length = inputs.input_ids.shape[1]
    trimmed_ids = generated_ids[:, prompt_length:]
    return processor.batch_decode(trimmed_ids, skip_special_tokens=False)[0].lstrip()


def doctags_to_markdown(doctags: str, image: Image.Image) -> str:
    """Convert doctags to markdown via docling-core."""
    doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
    doc = DoclingDocument.load_from_doctags(doctags_doc, document_name="doc")
    return doc.export_to_markdown()


def strip_tags(doctags: str) -> str:
    """Fallback: strip XML-like tags from doctags to get plain text."""
    text = re.sub(r"<[^>]+>", " ", doctags)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_page(model, processor, image: Image.Image) -> str:
    """Extract text from a single page image, with fallback on error."""
    doctags = extract_doctags(model, processor, image)
    try:
        return doctags_to_markdown(doctags, image)
    except Exception:
        return strip_tags(doctags)


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDFs using SmolDocling")
    parser.add_argument("files", nargs="+", help="PDF file paths to process")
    parser.add_argument("--dpi", type=int, default=200, help="DPI for PDF rendering (default: 200)")
    parser.add_argument("--output-dir", "-o", type=str, default=None,
                        help="Directory to save .md files (default: print to stdout)")
    args = parser.parse_args()

    print(f"Loading model on {DEVICE}...")
    model = AutoModelForVision2Seq.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        _attn_implementation="eager",
    ).to(DEVICE)
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    print("Model loaded.\n")

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in args.files:
        pdf_path = Path(filepath)
        if not pdf_path.exists():
            print(f"Skipping {filepath}: file not found")
            continue

        print(f"Processing: {pdf_path.name}")
        pages = convert_from_path(str(pdf_path), dpi=args.dpi)
        full_text = []

        for i, page in enumerate(pages):
            print(f"  Page {i + 1}/{len(pages)}...")
            text = extract_page(model, processor, page.convert("RGB"))
            full_text.append(f"## Page {i + 1}\n\n{text}")

        result = "\n\n---\n\n".join(full_text)

        if args.output_dir:
            out_file = output_dir / f"{pdf_path.stem}.md"
            out_file.write_text(result, encoding="utf-8")
            print(f"  Saved to {out_file}\n")
        else:
            print(f"\n{'='*60}")
            print(f" {pdf_path.name}")
            print(f"{'='*60}\n")
            print(result)
            print()


if __name__ == "__main__":
    main()
