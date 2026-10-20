def calculate_health_score(
    bmi,
    disease,
    smoking,
    alcohol,
    sleep,
    exercise,
    steps
):
    score = 100

    if bmi < 18.5 or bmi > 30:
        score -= 15
    elif bmi >= 25:
        score -= 10

    if disease.lower() != "none":
        score -= 15

    if smoking.lower() == "yes":
        score -= 15

    if alcohol.lower() == "yes":
        score -= 5

    if sleep < 6:
        score -= 10

    if exercise < 3:
        score -= 10

    if steps < 5000:
        score -= 10

    score = max(score, 0)

    if score >= 90:
        status = "Excellent 🟢"
    elif score >= 75:
        status = "Good 🟢"
    elif score >= 60:
        status = "Moderate 🟡"
    elif score >= 40:
        status = "Poor 🟠"
    else:
        status = "High Risk 🔴"

    return score, status