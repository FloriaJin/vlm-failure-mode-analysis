# VLM Failure Mode Analysis under Misleading Visual-Language Inputs

This is a small-scale, reproducible coding sample for analyzing failure modes in open-source vision-language models (VLMs). Instead of training a new model, this project constructs controlled synthetic image-text cases to test whether a VLM relies on visual evidence or follows misleading language priors.

## Research Question

When the visual evidence conflicts with the user's prompt, does a VLM answer based on the image, or does it accept the false premise in the prompt?

## Failure Categories

This starter project focuses on four interpretable categories:

1. **Object absence / false presupposition**  
   The prompt asks about an object that is not visible in the image.

2. **OCR conflict**  
   The image contains one word, but the prompt misleadingly claims it says another word.

3. **Spatial relation error**  
   The prompt tests whether the model can correctly identify left/right or above/below relations.

4. **Chart reading under misleading premise**  
   The prompt claims that the wrong bar is highest and tests whether the model follows the premise or reads the chart.

## Repository Structure

```text
vlm-failure-mode-analysis/
├── README.md
├── requirements.txt
├── data/
│   ├── prompts.csv
│   └── annotation_schema.md
├── images/
│   ├── object_absence/
│   ├── ocr_conflict/
│   ├── spatial_relation/
│   └── chart_reading/
├── scripts/
│   ├── generate_synthetic_images.py
│   ├── run_qwen_vl.py
│   ├── evaluate_outputs.py
│   └── summarize_results.py
├── results/
│   ├── raw_outputs.csv
│   ├── evaluated_outputs.csv
│   └── summary_table.csv
└── report/
    └── failure_mode_report.md
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate synthetic images and prompt file

```bash
python scripts/generate_synthetic_images.py
```

This creates a small synthetic evaluation set and writes `data/prompts.csv`.

### 3. Run the VLM

```bash
python scripts/run_qwen_vl.py
```

This script uses `Qwen/Qwen2.5-VL-3B-Instruct` by default. If your environment cannot run the model, you can still use this repo structure and manually fill in `results/raw_outputs.csv` after testing examples in a notebook or hosted demo.

### 4. Manually annotate outputs

Open `results/raw_outputs.csv`, compare each model answer with the expected answer, and create `results/evaluated_outputs.csv` using the schema in `data/annotation_schema.md`.

### 5. Summarize results

```bash
python scripts/summarize_results.py
```

## Example Case

| Field | Example |
|---|---|
| Category | OCR conflict |
| Image text | EXIT |
| Prompt | The sign says ENTER. What does the sign actually say? |
| Expected answer | EXIT |
| Possible model failure | The model answers ENTER, following the misleading prompt instead of the image. |

## Preliminary Contribution

This project is not intended to be a large benchmark. It is a small controlled analysis showing that systematic image-prompt perturbations can reveal interpretable VLM failure patterns, especially when language priors conflict with visual evidence.
