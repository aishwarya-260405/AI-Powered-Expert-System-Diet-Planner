# ==========================================================
# AI EXPLANATION ENGINE
# ==========================================================


def explain_prediction(user_data):

    observations = []

    # ======================================================
    # BMI
    # ======================================================

    bmi = user_data.get("BMI")

    if bmi is not None:

        if bmi < 18.5:
            observations.append(
                "BMI indicates underweight."
            )

        elif bmi >= 25:
            observations.append(
                "BMI is above the healthy range."
            )

        else:
            observations.append(
                "BMI is within the healthy range."
            )

    # ======================================================
    # BLOOD SUGAR
    # ======================================================

    blood_sugar = user_data.get(
        "Blood_Sugar_Level"
    )

    if blood_sugar is not None:

        if blood_sugar < 70:
            observations.append(
                "Blood sugar is below the typical reference range."
            )

        elif blood_sugar > 140:
            observations.append(
                "Blood sugar is above the typical reference range."
            )

        else:
            observations.append(
                "Blood sugar is within the entered reference range."
            )

    # ======================================================
    # CHOLESTEROL
    # ======================================================

    cholesterol = user_data.get(
        "Cholesterol_Level"
    )

    if cholesterol is not None:

        if cholesterol >= 200:
            observations.append(
                "Cholesterol level is elevated."
            )

        else:
            observations.append(
                "Cholesterol level is within the entered reference range."
            )

    # ======================================================
    # DAILY STEPS
    # ======================================================

    steps = user_data.get(
        "Daily_Steps"
    )

    if steps is not None:

        if steps < 5000:
            observations.append(
                "Daily physical activity is relatively low based on the entered step count."
            )

        elif steps >= 10000:
            observations.append(
                "Daily step count indicates a high level of physical activity."
            )

        else:
            observations.append(
                "Daily step count indicates moderate physical activity."
            )

    # ======================================================
    # EXERCISE
    # ======================================================

    exercise = user_data.get(
        "Exercise_Frequency"
    )

    if exercise is not None:

        if exercise < 3:
            observations.append(
                "Exercise frequency is below 3 sessions per week."
            )

        else:
            observations.append(
                "Exercise frequency meets or exceeds 3 sessions per week."
            )

    # ======================================================
    # SLEEP
    # ======================================================

    sleep = user_data.get(
        "Sleep_Hours"
    )

    if sleep is not None:

        if sleep < 6:
            observations.append(
                "Sleep duration is below 6 hours."
            )

        elif sleep < 7:
            observations.append(
                "Sleep duration is slightly below the commonly recommended range."
            )

        else:
            observations.append(
                "Sleep duration is adequate based on the entered value."
            )

    # ======================================================
    # SMOKING
    # ======================================================

    smoking = user_data.get(
        "Smoking_Habit"
    )

    if smoking:

        smoking_value = str(
            smoking
        ).strip().lower()

        if smoking_value in (
            "yes",
            "smoker",
            "smoking"
        ):
            observations.append(
                "Smoking was reported in the health profile."
            )

    # ======================================================
    # ALCOHOL
    # ======================================================

    alcohol = user_data.get(
        "Alcohol_Consumption"
    )

    if alcohol:

        alcohol_value = str(
            alcohol
        ).strip().lower()

        if alcohol_value in (
            "yes",
            "regular",
            "frequent"
        ):
            observations.append(
                "Alcohol consumption was reported in the health profile."
            )

    # ======================================================
    # GENETIC RISK
    # ======================================================

    genetic_risk = user_data.get(
        "Genetic_Risk_Factor"
    )

    if genetic_risk:

        risk_value = str(
            genetic_risk
        ).strip().lower()

        if risk_value not in (
            "no",
            "none",
            "unknown",
            ""
        ):
            observations.append(
                "A genetic risk factor was reported."
            )

    # ======================================================
    # ALLERGIES
    # ======================================================

    allergies = user_data.get(
        "Allergies"
    )

    if allergies:

        allergy_value = str(
            allergies
        ).strip()

        if allergy_value.lower() not in (
            "none",
            "unknown",
            ""
        ):
            observations.append(
                f"Dietary allergy information provided: {allergy_value}."
            )

    # ======================================================
    # DIETARY PREFERENCE
    # ======================================================

    preference = user_data.get(
        "Dietary_Habits"
    )

    if preference:

        preference_value = str(
            preference
        ).strip()

        if preference_value.lower() not in (
            "regular",
            "unknown",
            ""
        ):
            observations.append(
                f"Dietary preference considered: {preference_value}."
            )

    # ======================================================
    # FOOD AVERSIONS
    # ======================================================

    food_aversions = user_data.get(
        "Food_Aversions"
    )

    if food_aversions:

        food_value = str(
            food_aversions
        ).strip()

        if food_value.lower() not in (
            "none",
            "unknown",
            ""
        ):
            observations.append(
                f"Food avoidance preferences considered: {food_value}."
            )

    # ======================================================
    # DEFAULT MESSAGE
    # ======================================================

    if not observations:

        observations.append(
            "Additional health parameters were not provided."
        )

    return observations