import pytest
import torch
from pathlib import Path
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "images"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID = "ds4sd/SmolDocling-256M-preview"


@pytest.fixture(scope="session")
def model():
    """Load SmolDocling model once for all tests."""
    return AutoModelForVision2Seq.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        _attn_implementation="eager",
    ).to(DEVICE)


@pytest.fixture(scope="session")
def processor():
    """Load SmolDocling processor once for all tests."""
    return AutoProcessor.from_pretrained(MODEL_ID)


def extract_text(model, processor, image: Image.Image) -> str:
    """Run SmolDocling inference on an image and return markdown text."""
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
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    generated_ids = model.generate(**inputs, max_new_tokens=8192)
    prompt_length = inputs.input_ids.shape[1]
    trimmed_generated_ids = generated_ids[:, prompt_length:]
    doctags = processor.batch_decode(
        trimmed_generated_ids,
        skip_special_tokens=False,
    )[0].lstrip()

    # Convert DocTags to markdown
    doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
    doc = DoclingDocument.load_from_doctags(doctags_doc, document_name="test_doc")
    return doc.export_to_markdown()


@pytest.fixture(scope="session")
def simple_text_image():
    return Image.open(FIXTURES_DIR / "simple_text.png").convert("RGB")


@pytest.fixture(scope="session")
def table_image():
    return Image.open(FIXTURES_DIR / "table_doc.png").convert("RGB")


@pytest.fixture(scope="session")
def mixed_content_image():
    return Image.open(FIXTURES_DIR / "mixed_content.png").convert("RGB")
