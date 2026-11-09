from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    balanced_accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "mastitis_detection.csv"
)

TARGET = "class1"
GROUP = "Cow_ID"

CATEGORICAL_FEATURES = [
    "Breed",
]

NUMERIC_FEATURES = [
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


def build_model():
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline(
                    steps=[
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="most_frequent"
                            ),
                        ),
                        (
                            "encoder",
                            OneHotEncoder(
                                handle_unknown="ignore"
                            ),
                        ),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                SimpleImputer(
                    strategy="median"
                ),
                NUMERIC_FEATURES,
            ),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def main():
    df = pd.read_csv(DATA_PATH)

    X = df[
        CATEGORICAL_FEATURES
        + NUMERIC_FEATURES
    ]

    y = df[TARGET]
    groups = df[GROUP]

    splitter = StratifiedGroupKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    all_actual = []
    all_probability = []

    for fold, (train_idx, test_idx) in enumerate(
        splitter.split(X, y, groups),
        start=1,
    ):
        model = build_model()

        model.fit(
            X.iloc[train_idx],
            y.iloc[train_idx],
        )

        probabilities = model.predict_proba(
            X.iloc[test_idx]
        )[:, 1]

        all_actual.extend(
            y.iloc[test_idx].tolist()
        )

        all_probability.extend(
            probabilities.tolist()
        )

        print(f"Completed fold {fold}")

    actual = pd.Series(all_actual)
    probability = pd.Series(all_probability)

    print("\n==============================")
    print("MASTITIS THRESHOLD EVALUATION")
    print("==============================")

    print(
        "\nROC-AUC:",
        round(
            roc_auc_score(
                actual,
                probability,
            ),
            4,
        ),
    )

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
    ]

    print(
        "\nThreshold | Balanced Acc | "
        "Precision | Recall"
    )
    print("-" * 55)

    for threshold in thresholds:
        predicted = (
            probability >= threshold
        ).astype(int)

        balanced = balanced_accuracy_score(
            actual,
            predicted,
        )

        precision = precision_score(
            actual,
            predicted,
            zero_division=0,
        )

        recall = recall_score(
            actual,
            predicted,
            zero_division=0,
        )

        print(
            f"{threshold:9.2f} | "
            f"{balanced:13.4f} | "
            f"{precision:9.4f} | "
            f"{recall:6.4f}"
        )


if __name__ == "__main__":
    main()