"""Summarize manually evaluated VLM outputs by category."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EVAL_PATH = ROOT / "results" / "evaluated_outputs.csv"
SUMMARY_PATH = ROOT / "results" / "summary_table.csv"


def main() -> None:
    df = pd.read_csv(EVAL_PATH)
    if "is_correct" not in df.columns:
        raise ValueError("evaluated_outputs.csv must contain an is_correct column.")

    df["is_correct"] = pd.to_numeric(df["is_correct"], errors="coerce")
    summary = (
        df.groupby("category")
        .agg(
            cases=("id", "count"),
            accuracy=("is_correct", "mean"),
            errors=("is_correct", lambda x: int((x == 0).sum())),
        )
        .reset_index()
    )
    summary["error_rate"] = 1 - summary["accuracy"]
    summary.to_csv(SUMMARY_PATH, index=False)
    print(summary)
    print(f"Saved summary to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
