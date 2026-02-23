import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import extract_text


class TestTableExtraction:
    """Tests for extracting table content from document images."""

    def test_extracts_table_header_values(self, model, processor, table_image):
        """Model should extract table header text."""
        result = extract_text(model, processor, table_image)
        result_lower = result.lower()
        headers = ["product", "price", "quantity"]
        matches = [h for h in headers if h in result_lower]
        assert len(matches) >= 2, (
            f"Expected at least 2 table headers, found: {matches}. Output: {result[:300]}"
        )

    def test_extracts_table_cell_values(self, model, processor, table_image):
        """Model should extract cell values from the table."""
        result = extract_text(model, processor, table_image)
        result_lower = result.lower()
        cell_values = ["apple", "banana", "cherry"]
        matches = [v for v in cell_values if v in result_lower]
        assert len(matches) >= 2, (
            f"Expected at least 2 cell values, found: {matches}. Output: {result[:300]}"
        )

    def test_extracts_title(self, model, processor, table_image):
        """Model should extract the document title above the table."""
        result = extract_text(model, processor, table_image)
        assert "price list" in result.lower(), (
            f"Expected 'price list' in output. Output: {result[:300]}"
        )
