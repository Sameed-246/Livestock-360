from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "datasets"
    / "raw"
    / "mastitis"
    / "clinical_mastitis_cows_version1.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "mastitis_detection.csv"
)


FEATURES = [
    "Breed",
    "Months after giving birth",
    "Previous_Mastits_status",
    "IUFL",
    "EUFL",
    "IUFR",
    "EUFR",
    "IURL",
    "EURL",
    "IURR",
    "EURR",
    "Temperature",
    "Hardness",
    "Pain",
    "Milk_visibility",
]


def main():
    print("Loading mastitis dataset...")

    df = pd.read_csv(INPUT_PATH)

    print("Original rows:", len(df))
    print("Unique cows:", df["Cow_ID"].nunique())

    # Keep only the columns needed for the V2 model.
    df = df[
        ["Cow_ID", *FEATURES, "class1"]
    ].copy()

    # Normalize categorical column.
    df["Breed"] = df["Breed"].astype(str)

    # Convert remaining feature columns to numeric.
    numeric_features = [
        column
        for column in FEATURES
        if column != "Breed"
    ]

    for column in numeric_features:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Remove incomplete observations.
    df = df.dropna(
        subset=FEATURES + ["class1"]
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\nProcessed dataset saved:")
    print(OUTPUT_PATH)

    print("\nRows:", len(df))
    print(
        "Unique cows:",
        df["Cow_ID"].nunique()
    )

    print("\nTarget distribution:")
    print(
        df["class1"]
        .value_counts()
        .sort_index()
    )

    print("\nMissing values:")
    print(
        df.isna()
        .sum()
        .to_string()
    )


if __name__ == "__main__":
    main()