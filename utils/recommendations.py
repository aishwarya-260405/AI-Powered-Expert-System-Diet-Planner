def calculate_water(weight):
    """
    Recommended water intake (Litres/day)
    Formula: 35 ml per kg body weight
    """
    water = (weight * 35) / 1000
    return round(water, 1)


def calculate_macros(calories):
    """
    Macro Distribution
    Protein = 25%
    Carbs = 50%
    Fat = 25%
    """

    protein = round((calories * 0.25) / 4)
    carbs = round((calories * 0.50) / 4)
    fat = round((calories * 0.25) / 9)

    return protein, carbs, fat


def daily_goals(activity_level):
    """
    Generates personalized daily goals.
    """

    goals = []

    if activity_level.lower() == "active":
        goals.append("🚶 Walk at least 10,000 steps")
        goals.append("🏋 Exercise for 45–60 minutes")
    elif activity_level.lower() == "moderate":
        goals.append("🚶 Walk at least 8,000 steps")
        goals.append("🏃 Exercise for 30–45 minutes")
    else:
        goals.append("🚶 Walk at least 6,000 steps")
        goals.append("🧘 Light physical activity for 20–30 minutes")

    goals.append("💧 Drink sufficient water")
    goals.append("😴 Sleep 7–8 hours")
    goals.append("🥗 Include vegetables in every meal")

    return goals