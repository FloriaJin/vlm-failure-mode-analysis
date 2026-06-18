# Failure Mode Report

## 1. Project Goal

This project analyzes whether a vision-language model follows visual evidence or misleading language priors when the two conflict.

## 2. Model

- Model: Qwen/Qwen2.5-VL-3B-Instruct
- Decoding: greedy decoding, max_new_tokens=64
- Evaluation style: controlled synthetic images + manual annotation

## 3. Evaluation Categories

1. Object absence / false presupposition
2. OCR conflict
3. Spatial relation error
4. Chart reading under misleading premise

## 4. Results Summary

To be filled after running `scripts/summarize_results.py`.

| Category | Cases | Accuracy | Error rate | Main failure type |
|---|---:|---:|---:|---|
| object_absence | TBD | TBD | TBD | TBD |
| ocr_conflict | TBD | TBD | TBD | TBD |
| spatial_relation | TBD | TBD | TBD | TBD |
| chart_reading | TBD | TBD | TBD | TBD |

## 5. Qualitative Case Studies

### Case 1: False presupposition

- Image: TBD
- Prompt: TBD
- Model answer: TBD
- Expected answer: TBD
- Failure mode: TBD
- Interpretation: TBD

### Case 2: OCR conflict

- Image: TBD
- Prompt: TBD
- Model answer: TBD
- Expected answer: TBD
- Failure mode: TBD
- Interpretation: TBD

## 6. Preliminary Takeaway

The model's failures can be interpreted as conflicts between visual grounding and language priors. This suggests that even small controlled perturbation sets can reveal meaningful VLM reliability issues.
