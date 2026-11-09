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

MASTITIS_THRESHOLD = 0.35

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


def load_mastitis_model():
    """Load the V2 mastitis model."""
    if not MODEL_PATH.exists():
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception as exc:
        print(
            f"Warning: Failed to load V2 mastitis model: {exc}"
        )
        return None


def prepare_input(data):
    """Build one model-ready DataFrame row."""

    def to_float(value, default=0.0):
        try:
            if value in (None, ""):
                return default
            return float(value)
        except (ValueError, TypeError):
            return default

    def to_int(value, default=0):
        try:
            if value in (None, ""):
                return default
            return int(value)
        except (ValueError, TypeError):
            return default

    row = {
        "Breed": str(
            data.get("Breed", "Unknown")
        ),
        "Months after giving birth": to_float(
            data.get("Months after giving birth")
        ),
        "Previous_Mastits_status": to_int(
            data.get("Previous_Mastits_status")
        ),
        "IUFL": to_float(data.get("IUFL")),
        "EUFL": to_float(data.get("EUFL")),
        "IUFR": to_float(data.get("IUFR")),
        "EUFR": to_float(data.get("EUFR")),
        "IURL": to_float(data.get("IURL")),
        "EURL": to_float(data.get("EURL")),
        "IURR": to_float(data.get("IURR")),
        "EURR": to_float(data.get("EURR")),
        "Temperature": to_float(
            data.get("Temperature")
        ),
        "Hardness": to_int(
            data.get("Hardness")
        ),
        "Pain": to_int(
            data.get("Pain")
        ),
        "Milk_visibility": to_int(
            data.get("Milk_visibility")
        ),
    }

    return pd.DataFrame(
        [row],
        columns=FEATURES,
    )


def predict_mastitis(data):
    """
    Run the V2 mastitis prediction.

    Uses a 0.35 probability threshold for the
    class-1 screening decision.
    """

    model = load_mastitis_model()

    if model is None:
        return {
            "available": False,
            "prediction": None,
            "probability": None,
            "model_version": "V2",
        }

    try:
        input_data = prepare_input(data)

        probability = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(
                input_data
            )[0]

            classes = model.classes_

            probability_map = dict(
                zip(
                    classes,
                    probabilities,
                )
            )

            probability = round(
                float(
                    probability_map.get(1, 0.0)
                )
                * 100,
                2,
            )

            prediction = int(
                probability >= (
                    MASTITIS_THRESHOLD * 100
                )
            )

        else:
            prediction = int(
                model.predict(input_data)[0]
            )

        return {
            "available": True,
            "prediction": prediction,
            "probability": probability,
            "model_version": "V2",
            "threshold": MASTITIS_THRESHOLD,
        }

    except Exception as exc:
        print(
            "Warning: V2 mastitis prediction failed:",
            exc,
        )

        return {
            "available": False,
            "prediction": None,
            "probability": None,
            "model_version": "V2",
            "threshold": MASTITIS_THRESHOLD,
        }