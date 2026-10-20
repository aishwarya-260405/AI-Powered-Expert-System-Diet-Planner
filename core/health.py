# core/health.py

print("health.py loaded successfully")

def compute_bmi(height_cm, weight_kg):
    try:
        h = float(height_cm) / 100.0
        w = float(weight_kg)
        if h <= 0 or w <= 0:
            return 0.0, "Unknown"
        bmi = round(w / (h ** 2), 1)
    except Exception:
        return 0.0, "Unknown"

    if bmi < 18.5:
        return bmi, "Underweight"
    elif bmi < 24.9:
        return bmi, "Normal"
    elif bmi < 29.9:
        return bmi, "Overweight"
    else:
        return bmi, "Obese"


def bmr_mifflin_st_jeor(age, gender, height_cm, weight_kg):
    try:
        age = int(age)
        h = float(height_cm)
        w = float(weight_kg)
    except Exception:
        return 0.0

    s = 5 if gender.lower() == "male" else -161
    return max(0.0, 10 * w + 6.25 * h - 5 * age + s)


def activity_factor(level):
    level = (level or "").lower()
    if level == "sedentary":
        return 1.2
    elif level == "moderate":
        return 1.5
    elif level == "active":
        return 1.75
    return 1.3
