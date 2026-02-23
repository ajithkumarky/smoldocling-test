# SmolDocling Test Suite

A pytest test suite that validates [SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview)'s PDF-to-text extraction on mixed-content documents, plus a CLI tool for extracting text from real PDFs.

## Project Structure

```
├── conftest.py                    # Session-scoped model fixtures and extract_text helper
├── extract_pdfs.py                # CLI tool for extracting text from PDF files
├── requirements.txt               # Python dependencies
├── fixtures/
│   ├── generate_images.py         # Synthetic test image generator (Pillow)
│   └── images/                    # Generated test PNGs
│       ├── simple_text.png        # Plain paragraph text
│       ├── table_doc.png          # Table with headers and rows
│       └── mixed_content.png      # Headings, paragraphs, and an embedded table
└── tests/
    ├── test_text_extraction.py    # 3 tests — plain text extraction
    ├── test_table_extraction.py   # 3 tests — table content extraction
    └── test_mixed_content.py      # 5 tests — mixed document extraction
```

## Setup

```bash
pip install -r requirements.txt
pip install pdf2image
python fixtures/generate_images.py
```

**Note:** `pdf2image` requires [poppler](https://github.com/oschwartz10612/poppler-windows/releases/). Download it, extract, and add the `bin/` folder to your PATH.

## Extracting Text from PDFs

Use `extract_pdfs.py` to convert PDF files to markdown using SmolDocling:

```bash
# Extract one or more PDFs, save as markdown files
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
python extract_pdfs.py "C:/Users/ajith/scioly/downloaded_tests/06_PA_Exam_phys.pdf" -o extracted_output
```

This creates `extracted_output/06_PA_Exam_phys.md` with the full extracted text, tables, and headings in markdown format. Each page is separated by a `---` divider.

If a page fails the docling conversion (e.g. bounding box errors), the script automatically falls back to stripped plain text so extraction continues without crashing.

## Running Tests

```bash
# Full suite (11 tests)
pytest tests/ -v

# Individual modules
pytest tests/test_text_extraction.py -v
pytest tests/test_table_extraction.py -v
pytest tests/test_mixed_content.py -v
```

## Test Coverage

| Module | Tests | What's Validated |
|--------|-------|-----------------|
| `test_text_extraction` | 3 | Non-empty output, key phrase recognition, multi-sentence extraction |
| `test_table_extraction` | 3 | Table headers, cell values, document title |
| `test_mixed_content` | 5 | Headings, subheadings, paragraph content, embedded table values, heading order |

## How It Works

1. **Synthetic images** are generated with Pillow — no external PDFs needed for tests
2. **Session-scoped fixtures** load the SmolDocling model once, shared across all tests
3. **`extract_text` helper** runs inference and converts DocTags output to markdown via `docling-core`
4. **Property-based assertions** check for key phrases rather than exact output, making tests resilient to model variations
5. **`extract_pdfs.py`** converts PDF pages to images with `pdf2image`, then runs the same inference pipeline on each page

## Tech Stack

- **Model:** [ds4sd/SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview)
- **Framework:** pytest with session-scoped fixtures
- **Dependencies:** torch, transformers, docling-core, Pillow, pdf2image
