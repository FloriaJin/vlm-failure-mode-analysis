"""Create an annotation template from raw model outputs.

This script does not automatically judge correctness. It prepares a CSV file for
manual annotation, which is often more reliable for a small qualitative analysis.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "results" / "raw_outputs.csv"
EVAL_PATH = ROOT / "results" / "evaluated_outputs.csv"


def main() -> None:
    df = pd.read_csv(RAW_PATH)
    df["is_correct"] = ""
    df["failure_type"] = ""
    df["confidence_style"] = ""
    df["notes"] = ""
    df.to_csv(EVAL_PATH, index=False)
    print(f"Created annotation template: {EVAL_PATH}")


if __name__ == "__main__":
    main()
