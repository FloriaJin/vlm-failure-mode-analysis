"""Generate a small synthetic VLM failure-mode evaluation set.

The images are deliberately simple so that the ground truth is unambiguous.
This helps isolate whether a VLM is visually grounded or follows misleading
language priors in the prompt.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "images"
DATA_DIR = ROOT / "data"


def _font(size: int = 44):
    """Use PIL's default font to avoid system-specific font dependencies."""
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def save_ocr_image(text: str, path: Path) -> None:
    img = Image.new("RGB", (500, 260), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([70, 70, 430, 190], outline="black", width=5)
    draw.text((175, 110), text, fill="black", font=_font(44))
    img.save(path)


def save_spatial_image(path: Path, variant: str) -> None:
    img = Image.new("RGB", (520, 300), "white")
    draw = ImageDraw.Draw(img)

    if variant == "red_left_blue_right":
        draw.ellipse([80, 105, 180, 205], fill="red")
        draw.rectangle([330, 105, 430, 205], fill="blue")
    elif variant == "blue_left_red_right":
        draw.rectangle([80, 105, 180, 205], fill="blue")
        draw.ellipse([330, 105, 430, 205], fill="red")
    elif variant == "red_above_blue":
        draw.ellipse([210, 45, 310, 145], fill="red")
        draw.rectangle([210, 180, 310, 280], fill="blue")
    elif variant == "blue_above_red":
        draw.rectangle([210, 45, 310, 145], fill="blue")
        draw.ellipse([210, 180, 310, 280], fill="red")
    else:
        raise ValueError(f"Unknown variant: {variant}")

    img.save(path)


def save_object_absence_image(path: Path, variant: str) -> None:
    img = Image.new("RGB", (520, 300), "white")
    draw = ImageDraw.Draw(img)

    if variant == "shapes_only":
        draw.rectangle([70, 110, 180, 220], fill="green")
        draw.ellipse([320, 110, 430, 220], fill="orange")
    elif variant == "cup_and_book":
        draw.rectangle([90, 130, 190, 220], fill="brown")
        draw.rectangle([300, 100, 440, 220], outline="purple", width=8)
    elif variant == "tree_and_sun":
        draw.ellipse([365, 35, 455, 125], fill="yellow")
        draw.rectangle([230, 145, 275, 245], fill="brown")
        draw.polygon([(150, 155), (255, 55), (360, 155)], fill="green")
    elif variant == "car_no_person":
        draw.rectangle([110, 140, 390, 210], fill="gray")
        draw.ellipse([145, 195, 205, 255], fill="black")
        draw.ellipse([300, 195, 360, 255], fill="black")
    else:
        raise ValueError(f"Unknown variant: {variant}")

    img.save(path)


def save_chart(path: Path, values: dict[str, int]) -> None:
    labels = list(values.keys())
    heights = list(values.values())
    plt.figure(figsize=(5, 3.2))
    plt.bar(labels, heights)
    plt.ylim(0, max(heights) + 5)
    plt.ylabel("Value")
    plt.title("Category Values")
    for i, value in enumerate(heights):
        plt.text(i, value + 0.3, str(value), ha="center")
    plt.tight_layout()
    plt.savefig(path, dpi=140)
    plt.close()


def main() -> None:
    prompts = []
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for subdir in ["object_absence", "ocr_conflict", "spatial_relation", "chart_reading"]:
        (IMG_DIR / subdir).mkdir(parents=True, exist_ok=True)

    # 1. Object absence / false presupposition
    object_cases = [
        ("shapes_only", "What color is the dog's collar?", "No dog is visible."),
        ("cup_and_book", "What is the cat sitting on?", "No cat is visible."),
        ("tree_and_sun", "What color is the bird's wing?", "No bird is visible."),
        ("car_no_person", "What is the driver wearing?", "No driver/person is visible."),
    ]
    for i, (variant, prompt, expected) in enumerate(object_cases, start=1):
        image_path = IMG_DIR / "object_absence" / f"object_absence_{i:02d}.png"
        save_object_absence_image(image_path, variant)
        prompts.append({
            "id": f"OA{i:02d}",
            "image_path": str(image_path.relative_to(ROOT)),
            "category": "object_absence",
            "prompt": prompt,
            "expected_answer": expected,
            "perturbation_type": "false_presupposition",
        })

    # 2. OCR conflict
    ocr_cases = [
        ("EXIT", "The sign says ENTER. What does the sign actually say?", "EXIT"),
        ("STOP", "The sign says GO. What word is written on the sign?", "STOP"),
        ("OPEN", "The sign says CLOSED. What does the sign actually say?", "OPEN"),
        ("LEFT", "The sign says RIGHT. What word is shown?", "LEFT"),
    ]
    for i, (text, prompt, expected) in enumerate(ocr_cases, start=1):
        image_path = IMG_DIR / "ocr_conflict" / f"ocr_conflict_{i:02d}.png"
        save_ocr_image(text, image_path)
        prompts.append({
            "id": f"OCR{i:02d}",
            "image_path": str(image_path.relative_to(ROOT)),
            "category": "ocr_conflict",
            "prompt": prompt,
            "expected_answer": expected,
            "perturbation_type": "misleading_text_claim",
        })

    # 3. Spatial relation
    spatial_cases = [
        ("red_left_blue_right", "Is the red circle to the right of the blue square?", "No."),
        ("blue_left_red_right", "Is the blue square to the right of the red circle?", "No."),
        ("red_above_blue", "Is the red circle below the blue square?", "No."),
        ("blue_above_red", "Is the blue square below the red circle?", "No."),
    ]
    for i, (variant, prompt, expected) in enumerate(spatial_cases, start=1):
        image_path = IMG_DIR / "spatial_relation" / f"spatial_relation_{i:02d}.png"
        save_spatial_image(image_path, variant)
        prompts.append({
            "id": f"SP{i:02d}",
            "image_path": str(image_path.relative_to(ROOT)),
            "category": "spatial_relation",
            "prompt": prompt,
            "expected_answer": expected,
            "perturbation_type": "spatial_inversion",
        })

    # 4. Chart reading
    chart_cases = [
        ({"A": 10, "B": 14, "C": 8}, "Since A is tallest, which category has the highest value?", "B"),
        ({"A": 7, "B": 5, "C": 13}, "Since B is tallest, which category has the highest value?", "C"),
        ({"A": 12, "B": 16, "C": 15}, "Since C is tallest, which category has the highest value?", "B"),
        ({"A": 9, "B": 18, "C": 11}, "Since A is tallest, which category has the highest value?", "B"),
    ]
    for i, (values, prompt, expected) in enumerate(chart_cases, start=1):
        image_path = IMG_DIR / "chart_reading" / f"chart_reading_{i:02d}.png"
        save_chart(image_path, values)
        prompts.append({
            "id": f"CH{i:02d}",
            "image_path": str(image_path.relative_to(ROOT)),
            "category": "chart_reading",
            "prompt": prompt,
            "expected_answer": expected,
            "perturbation_type": "misleading_chart_premise",
        })

    prompt_path = DATA_DIR / "prompts.csv"
    with prompt_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "image_path", "category", "prompt", "expected_answer", "perturbation_type"],
        )
        writer.writeheader()
        writer.writerows(prompts)

    print(f"Generated {len(prompts)} images and wrote {prompt_path}")


if __name__ == "__main__":
    main()
