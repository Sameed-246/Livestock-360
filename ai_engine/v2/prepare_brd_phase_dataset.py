from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "datasets"
    / "raw"
    / "brd"
    / "Cantor_machineclean-opendepository.xlsx"
)

OUTPUT_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "brd_phase_detection.csv"
)

FEATURES = [
    "Temp",
    "Breath",
    "Temp_score",
    "Gender",
    "agefeeder",
    "Fecal",
    "Milk_Intake",
    "Lying_time",
    "Lying_bouts",
    "lying_daily",
]


def parse_lying_time(value):
    if pd.isna(value):
        return None

    try:
        h, m, s = map(int, str(value).split(":"))
        return h * 60 + m + s / 60
    except (ValueError, TypeError):
        return None


def main():
    df = pd.read_excel(INPUT_PATH)

    # Keep only observations with an explicit disease-timeline label.
    df = df[df["Pneuday"].notna()].copy()

    # Pre-diagnosis = 1
    # Diagnosed/post-diagnosis = 0
    df["brd_pre_diagnosis"] = (
        df["Pneuday"] < 0
    ).astype(int)

    selected = [
        "IdSeq",
        "Pneuday",
        *FEATURES,
        "brd_pre_diagnosis",
    ]

    df = df[selected].copy()

    df["Lying_time"] = df["Lying_time"].apply(
        parse_lying_time
    )

    numeric_columns = [
        "Temp",
        "Breath",
        "Temp_score",
        "Gender",
        "agefeeder",
        "Fecal",
        "Milk_Intake",
        "Lying_time",
        "Lying_bouts",
        "lying_daily",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Keep observations with the core physiological features.
    df = df.dropna(
        subset=[
            "Temp",
            "Breath",
            "Temp_score",
            "Gender",
            "agefeeder",
            "Fecal",
            "Lying_time",
            "Lying_bouts",
            "lying_daily",
        ]
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("Saved:", OUTPUT_PATH)
    print("Rows:", len(df))
    print("Animals:", df["IdSeq"].nunique())

    print("\nTarget distribution:")
    print(
        df["brd_pre_diagnosis"]
        .value_counts()
        .sort_index()
    )


if __name__ == "__main__":
    main()
    