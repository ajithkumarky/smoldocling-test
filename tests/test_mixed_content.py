import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import extract_text


class TestMixedContentExtraction:
    """Tests for documents with headings, paragraphs, and tables."""

    def test_extracts_heading(self, model, processor, mixed_content_image):
        """Model should extract the main heading."""
        result = extract_text(model, processor, mixed_content_image)
        assert "annual report" in result.lower(), (
            f"Expected 'annual report' heading. Output: {result[:300]}"
        )

    def test_extracts_subheadings(self, model, processor, mixed_content_image):
        """Model should extract subheadings."""
        result = extract_text(model, processor, mixed_content_image)
        result_lower = result.lower()
        subheadings = ["executive summary", "financial overview"]
        matches = [s for s in subheadings if s in result_lower]
        assert len(matches) >= 1, (
            f"Expected at least 1 subheading, found: {matches}. Output: {result[:300]}"
        )

    def test_extracts_paragraph_content(self, model, processor, mixed_content_image):
        """Model should extract paragraph text."""
        result = extract_text(model, processor, mixed_content_image)
        result_lower = result.lower()
        phrases = ["revenue", "15%", "new markets"]
        matches = [p for p in phrases if p in result_lower]
        assert len(matches) >= 1, (
            f"Expected at least 1 paragraph phrase, found: {matches}. Output: {result[:300]}"
        )

    def test_extracts_embedded_table_values(self, model, processor, mixed_content_image):
        """Model should extract table values from mixed content."""
        result = extract_text(model, processor, mixed_content_image)
        result_lower = result.lower()
        values = ["revenue", "profit", "$10m", "$2m"]
        matches = [v for v in values if v in result_lower]
        assert len(matches) >= 2, (
            f"Expected at least 2 table values, found: {matches}. Output: {result[:300]}"
        )

    def test_heading_before_paragraph(self, model, processor, mixed_content_image):
        """Headings should appear before their associated content."""
        result = extract_text(model, processor, mixed_content_image)
        result_lower = result.lower()
        heading_pos = result_lower.find("annual report")
        content_pos = result_lower.find("revenue")
        if heading_pos >= 0 and content_pos >= 0:
            assert heading_pos < content_pos, (
                "Expected heading to appear before paragraph content"
            )
