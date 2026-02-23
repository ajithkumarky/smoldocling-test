import sys
from pathlib import Path

# Ensure root is on path so conftest is found
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import extract_text


class TestSimpleTextExtraction:
    """Tests for extracting plain text from document images."""

    def test_extracts_nonempty_text(self, model, processor, simple_text_image):
        """Model should produce non-empty output for a text image."""
        result = extract_text(model, processor, simple_text_image)
        assert len(result.strip()) > 0, "Expected non-empty extracted text"

    def test_contains_key_phrases(self, model, processor, simple_text_image):
        """Model should extract recognizable phrases from the image."""
        result = extract_text(model, processor, simple_text_image)
        result_lower = result.lower()
        # At least some of these phrases should appear
        key_phrases = ["quick brown fox", "simple text", "programming language"]
        matches = [p for p in key_phrases if p in result_lower]
        assert len(matches) >= 1, (
            f"Expected at least 1 key phrase in output, found none. Output: {result[:200]}"
        )

    def test_output_has_multiple_sentences(self, model, processor, simple_text_image):
        """Multi-sentence input should produce output with multiple sentences."""
        result = extract_text(model, processor, simple_text_image)
        # Model may merge lines into a paragraph; check for multiple sentences
        sentences = [s.strip() for s in result.strip().split(".") if s.strip()]
        assert len(sentences) >= 2, f"Expected multiple sentences, got {len(sentences)}"
