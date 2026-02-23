# SmolDocling PDF Extractor

A command-line tool that extracts text, tables, and headings from PDF documents using [SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview). Outputs clean markdown with preserved document structure.

## Setup

```bash
pip install -r requirements.txt
pip install pdf2image
```

**Note:** `pdf2image` requires [poppler](https://github.com/oschwartz10612/poppler-windows/releases/). Download it, extract, and add the `bin/` folder to your PATH.

## Usage

```bash
# Extract PDFs to markdown files
python extract_pdfs.py file1.pdf file2.pdf -o output_dir

# Print extracted text to stdout
python extract_pdfs.py document.pdf

# Use higher DPI for better quality (default: 200)
python extract_pdfs.py document.pdf -o output_dir --dpi 300
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `files` | One or more PDF file paths | required |
| `-o`, `--output-dir` | Directory to save `.md` files | stdout |
| `--dpi` | DPI for PDF page rendering | 200 |

**Example:**

```bash
python extract_pdfs.py "C:/path/to/exam.pdf" "C:/path/to/report.pdf" -o extracted_output
```

This creates one `.md` file per PDF in `extracted_output/`, with full extracted text, tables, and headings in markdown format. Pages are separated by `---` dividers.

If a page fails the docling conversion (e.g. bounding box errors), the script automatically falls back to stripped plain text so extraction continues without crashing.

## How It Works

1. PDF pages are rendered to images using `pdf2image` + poppler
2. Each page image is passed to SmolDocling-256M-preview for inference
3. The model outputs DocTags, which are converted to markdown via `docling-core`
4. The model loads once and processes all pages/files in sequence

## Test Suite

The project includes a pytest test suite that validates SmolDocling's extraction accuracy using synthetic test images.

```bash
# Generate test images
python fixtures/generate_images.py

# Run all 11 tests
pytest tests/ -v
```

| Module | Tests | What's Validated |
|--------|-------|-----------------|
| `test_text_extraction` | 3 | Non-empty output, key phrase recognition, multi-sentence extraction |
| `test_table_extraction` | 3 | Table headers, cell values, document title |
| `test_mixed_content` | 5 | Headings, subheadings, paragraph content, embedded table values, heading order |

Tests use session-scoped fixtures to load the model once, and check for key phrases rather than exact output to stay resilient to model variations.

## Project Structure

```
├── extract_pdfs.py                # CLI tool for PDF-to-markdown extraction
├── conftest.py                    # Shared model fixtures and extract_text helper
├── requirements.txt               # Python dependencies
├── fixtures/
│   ├── generate_images.py         # Synthetic test image generator (Pillow)
│   └── images/                    # Generated test PNGs
└── tests/
    ├── test_text_extraction.py    # Plain text extraction tests
    ├── test_table_extraction.py   # Table content extraction tests
    └── test_mixed_content.py      # Mixed document extraction tests
```

## Tech Stack

- **Model:** [ds4sd/SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview)
- **Dependencies:** torch, transformers, docling-core, Pillow, pdf2image
