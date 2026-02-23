# SmolDocling Test Suite

A pytest test suite that validates [SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview)'s PDF-to-text extraction on mixed-content documents.

## Project Structure

```
├── conftest.py                    # Session-scoped model fixtures and extract_text helper
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
python fixtures/generate_images.py
```

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

1. **Synthetic images** are generated with Pillow — no external PDFs needed
2. **Session-scoped fixtures** load the SmolDocling model once, shared across all tests
3. **`extract_text` helper** runs inference and converts DocTags output to markdown via `docling-core`
4. **Property-based assertions** check for key phrases rather than exact output, making tests resilient to model variations

## Tech Stack

- **Model:** [ds4sd/SmolDocling-256M-preview](https://huggingface.co/ds4sd/SmolDocling-256M-preview)
- **Framework:** pytest with session-scoped fixtures
- **Dependencies:** torch, transformers, docling-core, Pillow
