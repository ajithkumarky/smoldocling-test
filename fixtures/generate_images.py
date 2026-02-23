from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys


def get_font(size=20):
    """Get a font, falling back to default if needed."""
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except OSError:
            return ImageFont.load_default()


def create_simple_text_image(output_path: Path):
    """Create an image with simple paragraph text."""
    img = Image.new("RGB", (800, 400), "white")
    draw = ImageDraw.Draw(img)
    font = get_font(20)

    text = (
        "The quick brown fox jumps over the lazy dog.\n"
        "This is a simple text document for testing.\n"
        "SmolDocling should extract this text accurately.\n"
        "Python is a popular programming language."
    )
    draw.text((50, 50), text, fill="black", font=font)
    img.save(output_path)


def create_table_image(output_path: Path):
    """Create an image with a simple table."""
    img = Image.new("RGB", (800, 400), "white")
    draw = ImageDraw.Draw(img)
    font = get_font(18)

    # Title
    draw.text((50, 30), "Product Price List", fill="black", font=get_font(24))

    # Draw table grid
    headers = ["Product", "Price", "Quantity"]
    rows = [
        ["Apple", "$1.50", "100"],
        ["Banana", "$0.75", "200"],
        ["Cherry", "$3.00", "50"],
    ]

    x_start, y_start = 50, 80
    col_width, row_height = 200, 35

    # Draw headers
    for i, header in enumerate(headers):
        x = x_start + i * col_width
        draw.rectangle([x, y_start, x + col_width, y_start + row_height], outline="black")
        draw.text((x + 10, y_start + 8), header, fill="black", font=font)

    # Draw rows
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            x = x_start + c * col_width
            y = y_start + (r + 1) * row_height
            draw.rectangle([x, y, x + col_width, y + row_height], outline="black")
            draw.text((x + 10, y + 8), cell, fill="black", font=font)

    img.save(output_path)


def create_mixed_content_image(output_path: Path):
    """Create an image with headings, text, and a small table."""
    img = Image.new("RGB", (800, 600), "white")
    draw = ImageDraw.Draw(img)

    # Heading
    draw.text((50, 30), "Annual Report 2025", fill="black", font=get_font(28))

    # Subheading
    draw.text((50, 80), "Executive Summary", fill="black", font=get_font(22))

    # Paragraph
    para = (
        "Revenue increased by 15% compared to the previous year.\n"
        "The company expanded into three new markets."
    )
    draw.text((50, 120), para, fill="black", font=get_font(18))

    # Another subheading
    draw.text((50, 220), "Financial Overview", fill="black", font=get_font(22))

    # Small table
    headers = ["Metric", "Value"]
    rows = [["Revenue", "$10M"], ["Profit", "$2M"]]

    x_start, y_start = 50, 270
    col_width, row_height = 200, 35
    font = get_font(18)

    for i, header in enumerate(headers):
        x = x_start + i * col_width
        draw.rectangle([x, y_start, x + col_width, y_start + row_height], outline="black")
        draw.text((x + 10, y_start + 8), header, fill="black", font=font)

    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            x = x_start + c * col_width
            y = y_start + (r + 1) * row_height
            draw.rectangle([x, y, x + col_width, y + row_height], outline="black")
            draw.text((x + 10, y + 8), cell, fill="black", font=font)

    img.save(output_path)


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "images"
    output_dir.mkdir(exist_ok=True)

    create_simple_text_image(output_dir / "simple_text.png")
    create_table_image(output_dir / "table_doc.png")
    create_mixed_content_image(output_dir / "mixed_content.png")
    print(f"Generated 3 test images in {output_dir}")
