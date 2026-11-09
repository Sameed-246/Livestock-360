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

OUTPUT_DIR = BASE_DIR / "datasets" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "brd_early_warning.csv"


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
    """Convert HH:MM:SS-like values into minutes."""
    if pd.isna(value):
        return None

    try:
        parts = str(value).split(":")
        if len(parts) != 3:
            return None

        hours, minutes, seconds = map(int, parts)
        return hours * 60 + minutes + seconds / 60
    except (ValueError, TypeError):
        return None


def main():
    print("Loading BRD dataset...")
    df = pd.read_excel(INPUT_PATH)

    print("Original shape:", df.shape)

    # Keep only the features that are available before diagnosis.
    selected_columns = ["IdSeq", "Pneuday"] + FEATURES
    df = df[selected_columns].copy()

    # ---------------------------------------------------------
    # Target definition:
    # -14 to -1  -> pre-sick / early warning positive
    # NaN        -> no recorded BRD event in this dataset
    # 0+         -> diagnosed/positive period, excluded
    # ---------------------------------------------------------

    pre_sick_mask = df["Pneuday"].between(-14, -1, inclusive="both")
    negative_mask = df["Pneuday"].isna()
    keep_mask = pre_sick_mask | negative_mask

    df = df.loc[keep_mask].copy()

    df["brd_early_warning"] = pre_sick_mask.loc[df.index].astype(int)

    # Convert time column to numeric minutes.
    df["Lying_time"] = df["Lying_time"].apply(parse_lying_time)

    # Convert numeric columns.
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

    # Remove rows with no useful predictor information.
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

    # Remove identifier/target source column from final features.
    df = df[
        FEATURES + ["brd_early_warning", "IdSeq"]
    ]

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\nProcessed dataset saved:")
    print(OUTPUT_PATH)

    print("\nShape:", df.shape)

    print("\nTarget distribution:")
    print(
        df["brd_early_warning"]
        .value_counts()
        .sort_index()
    )

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nUnique animals:")
    print(df["IdSeq"].nunique())


if __name__ == "__main__":
    main()