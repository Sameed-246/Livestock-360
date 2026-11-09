from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "ai_engine"
    / "v2"
    / "brd_phase_model.pkl"
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


def main():
    model = joblib.load(MODEL_PATH)

    classifier = model.named_steps["model"]

    importances = classifier.feature_importances_

    result = pd.DataFrame(
        {
            "feature": FEATURES,
            "importance": importances,
        }
    )

    result = result.sort_values(
        "importance",
        ascending=False,
    )

    print("\nBRD V2 FEATURE IMPORTANCE")
    print("=========================\n")

    for _, row in result.iterrows():
        print(
            f"{row['feature']:<15} "
            f"{row['importance']:.4f}"
        )


if __name__ == "__main__":
    main()