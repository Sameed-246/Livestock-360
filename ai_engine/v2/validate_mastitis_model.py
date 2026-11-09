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
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )


def main():
    print("Loading mastitis dataset...")

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

    results = []

    for fold, (train_idx, test_idx) in enumerate(
        splitter.split(X, y, groups),
        start=1,
    ):
        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        train_cows = set(
            groups.iloc[train_idx]
        )

        test_cows = set(
            groups.iloc[test_idx]
        )

        overlap = train_cows & test_cows

        print(
            f"\nFold {fold}: "
            f"train={len(train_idx)}, "
            f"test={len(test_idx)}, "
            f"cow_overlap={len(overlap)}"
        )

        pipeline = build_model()

        pipeline.fit(
            X_train,
            y_train,
        )

        predictions = pipeline.predict(
            X_test
        )

        probabilities = pipeline.predict_proba(
            X_test
        )[:, 1]

        balanced_accuracy = (
            balanced_accuracy_score(
                y_test,
                predictions,
            )
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0,
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0,
        )

        roc_auc = roc_auc_score(
            y_test,
            probabilities,
        )

        print(
            f"  Balanced accuracy: "
            f"{balanced_accuracy:.4f}"
        )

        print(
            f"  Class-1 precision: "
            f"{precision:.4f}"
        )

        print(
            f"  Class-1 recall: "
            f"{recall:.4f}"
        )

        print(
            f"  ROC-AUC: "
            f"{roc_auc:.4f}"
        )

        results.append(
            {
                "fold": fold,
                "balanced_accuracy": balanced_accuracy,
                "precision": precision,
                "recall": recall,
                "roc_auc": roc_auc,
            }
        )

    results_df = pd.DataFrame(results)

    print("\n==============================")
    print("5-FOLD MASTITIS VALIDATION")
    print("==============================")

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\nMean:")
    print(
        results_df.mean(
            numeric_only=True
        ).to_string()
    )

    print("\nStandard deviation:")
    print(
        results_df.std(
            numeric_only=True
        ).to_string()
    )


if __name__ == "__main__":
    main()
    