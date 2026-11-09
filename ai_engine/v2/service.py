from .mastitis_predictor import predict_mastitis


def run_mastitis_assessment(data):
    """
    Run the V2 mastitis assessment.

    The V2 model is optional and should not affect
    the existing Livestock360 V1 prediction flow.
    """

    result = predict_mastitis(data)

    if not result.get("available"):
        return {
            "available": False,
            "condition": "Mastitis",
            "assessment": "Unavailable",
            "probability": None,
            "model_version": "V2",
        }

    probability = result.get("probability")

    if result.get("prediction") == 1:
        assessment = "Positive"
        recommendation = (
            "Clinical indicators are consistent with "
            "possible mastitis. Veterinary examination "
            "is recommended."
        )
    else:
        assessment = "Negative"
        recommendation = (
            "The V2 model did not identify a positive "
            "mastitis pattern from the supplied clinical data."
        )

    return {
        "available": True,
        "condition": "Mastitis",
        "assessment": assessment,
        "probability": probability,
        "threshold": result.get("threshold"),
        "model_version": result.get("model_version", "V2"),
        "recommendation": recommendation,
    }