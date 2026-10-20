import random
import pandas as pd

def generate_dataset(n=5000):
    data = []

    for _ in range(n):
        age = random.randint(18, 65)
        gender = random.choice(["Male", "Female"])
        height = random.randint(145, 190)
        weight = random.randint(45, 120)

        activity = random.choice(["sedentary", "moderate", "active"])
        disease = random.choice(["none", "diabetes", "hypertension", "pcos"])

        # BMI
        bmi = weight / ((height / 100) ** 2)

        # Base calorie (rough physiological baseline)
        if gender == "Male":
            base_cal = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            base_cal = 10 * weight + 6.25 * height - 5 * age - 161

        # Activity multiplier
        activity_factor = {
            "sedentary": 1.2,
            "moderate": 1.5,
            "active": 1.75
        }[activity]

        calories = base_cal * activity_factor

        # Disease adjustments (population trends)
        if disease in ["diabetes", "pcos"]:
            calories *= 0.9
        if bmi >= 30:
            calories *= 0.85
        if bmi < 18.5:
            calories *= 1.1

        calories = int(calories)

        data.append([
            age, gender, height, weight, bmi, activity, disease, calories
        ])

    df = pd.DataFrame(
        data,
        columns=[
            "age", "gender", "height", "weight",
            "bmi", "activity", "disease", "calories"
        ]
    )

    return df


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("diet_calorie_dataset.csv", index=False)
    print("Dataset generated: diet_calorie_dataset.csv")
