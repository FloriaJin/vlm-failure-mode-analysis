"""Run Qwen2.5-VL on the synthetic evaluation set.

Note: This requires a GPU-backed environment for practical use.
If you cannot run the model locally, use this script as a template and run it
in Colab/Kaggle, then save the outputs to `results/raw_outputs.csv`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import torch
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"


def load_model():
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype="auto",
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    return model, processor


def ask_vlm(model, processor, image_path: Path, prompt: str) -> str:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": str(image_path)},
                {
                    "type": "text",
                    "text": (
                        prompt
                        + "\nAnswer briefly. If the answer is not visible in the image, say 'Not visible.'"
                    ),
                },
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
        )

    generated_ids_trimmed = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
    ]

    return processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0].strip()


def main() -> None:
    prompt_path = ROOT / "data" / "prompts.csv"
    output_path = ROOT / "results" / "raw_outputs.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(prompt_path)
    model, processor = load_model()

    rows = []
    for _, row in df.iterrows():
        image_path = ROOT / row["image_path"]
        answer = ask_vlm(model, processor, image_path, row["prompt"])
        print(row["id"], "=>", answer)
        rows.append({
            "id": row["id"],
            "image_path": row["image_path"],
            "category": row["category"],
            "prompt": row["prompt"],
            "expected_answer": row["expected_answer"],
            "model_answer": answer,
        })

    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Saved raw outputs to {output_path}")


if __name__ == "__main__":
    main()
