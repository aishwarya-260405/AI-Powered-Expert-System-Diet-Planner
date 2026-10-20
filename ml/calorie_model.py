# ml/calorie_model.py

def ml_adjust_calories(bmi, activity_level, disease):
    """
    Simple ML-inspired personalization logic.
    (Rule-based approximation of ML behavior)
    """

    adjustment = 1.0

    if bmi >= 25:
        adjustment -= 0.1
    elif bmi < 18.5:
        adjustment += 0.1

    if activity_level == "active":
        adjustment += 0.1
    elif activity_level == "sedentary":
        adjustment -= 0.05

    if disease in ["diabetes", "pcos"]:
        adjustment -= 0.05

    return adjustment
