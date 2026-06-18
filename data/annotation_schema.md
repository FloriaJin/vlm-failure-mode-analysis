# Annotation Schema

After running the model, create `results/evaluated_outputs.csv` with the following columns:

| Column | Meaning |
|---|---|
| id | Test case ID |
| image_path | Path to image |
| category | Failure category |
| prompt | Prompt given to the VLM |
| expected_answer | Ground-truth answer |
| model_answer | Raw VLM output |
| is_correct | 1 if the answer is correct, 0 otherwise |
| failure_type | Main failure type if incorrect |
| confidence_style | `overconfident`, `uncertain`, `hedged`, or `corrected_false_premise` |
| notes | Short qualitative comment |

Suggested `failure_type` labels:

- `object_hallucination`
- `language_prior_override`
- `ocr_hallucination`
- `spatial_relation_error`
- `chart_reading_error`
- `unsupported_overconfidence`
- `none`
