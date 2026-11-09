from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "ai_engine"
    / "v2"
    / "mastitis_model.pkl"
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
    pipeline = joblib.load(MODEL_PATH)

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = preprocessor.get_feature_names_out()

    importances = model.feature_importances_

    result = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    ).sort_values(
        "importance",
        ascending=False,
    )

    print("\nMASTITIS V2 FEATURE IMPORTANCE")
    print("==============================\n")

    print(
        result.head(20).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()