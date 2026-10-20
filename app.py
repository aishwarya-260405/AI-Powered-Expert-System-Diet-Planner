from utils.health_score import calculate_health_score

from utils.recommendations import (
    calculate_water,
    calculate_macros,
    daily_goals
)

from utils.explain import explain_prediction

from flask import Flask, render_template, request

from core.health import (
    compute_bmi,
    bmr_mifflin_st_jeor,
    activity_factor
)

from expert.diet_rules import DIET_RULES

from ml.predict import (
    predict_calories,
    predict_meal_plan
)

import threading
import webbrowser


# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def safe_lower(val):
    return str(val or "").strip().lower()


def get_optional_int(field_name):
    """
    Returns None when the user leaves an optional field blank.
    """
    value = request.form.get(field_name, "").strip()

    if value == "":
        return None

    try:
        return int(value)
    except ValueError:
        return None


def get_optional_float(field_name):
    """
    Returns None when the user leaves an optional field blank.
    """
    value = request.form.get(field_name, "").strip()

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


# ==========================================================
# DIET CONSTRAINTS
# ==========================================================
# ==========================================================
# PERSONALIZED DIET ENGINE
# ==========================================================

def apply_constraints(
    text,
    preference,
    allergies,
    dislikes,
    disease,
    medications
):
    """
    Applies the user's dietary preference, allergies,
    food avoidances and medication information to a meal.
    """

    t = str(text)

    pref = safe_lower(preference)
    alg = safe_lower(allergies)
    med = safe_lower(medications)

    # ------------------------------------------------------
    # VEGETARIAN
    # ------------------------------------------------------

    if pref == "vegetarian":
        t = (
            t.replace("chicken", "paneer")
             .replace("fish", "tofu")
             .replace("eggs", "paneer/tofu")
        )

    # ------------------------------------------------------
    # VEGAN
    # ------------------------------------------------------

    elif pref == "vegan":
        t = (
            t.replace("chicken", "tofu")
             .replace("fish", "tofu")
             .replace("eggs", "tofu")
             .replace("paneer", "tofu")
             .replace("curd", "plant-based curd")
             .replace("milk", "soy milk")
        )

    # ------------------------------------------------------
    # NON-VEGETARIAN
    # ------------------------------------------------------

    elif pref in (
        "non-vegetarian",
        "non vegetarian",
        "nonveg",
        "non-veg"
    ):
        t = (
            t.replace("paneer/tofu", "chicken/fish")
             .replace("tofu", "chicken/fish")
        )

    # ------------------------------------------------------
    # LACTOSE ALLERGY
    # ------------------------------------------------------

    if "lactose" in alg or "dairy" in alg:
        t = (
            t.replace("milk", "soy milk")
             .replace("curd", "plant-based curd")
             .replace("paneer", "tofu")
        )

    # ------------------------------------------------------
    # GLUTEN ALLERGY
    # ------------------------------------------------------

    if "gluten" in alg or "wheat" in alg:
        t = (
            t.replace("whole-wheat roti", "rice")
             .replace("whole-wheat", "gluten-free")
             .replace("wheat", "gluten-free alternative")
             .replace("roti", "rice")
        )

    # ------------------------------------------------------
    # NUT ALLERGY
    # ------------------------------------------------------

    if "nut" in alg or "nuts" in alg:
        t = (
            t.replace("nuts", "seeds")
             .replace("almonds", "seeds")
             .replace("cashews", "seeds")
        )

    # ------------------------------------------------------
    # MEDICATION
    # ------------------------------------------------------

    if "thyroxine" in med:
        t += (
            " Thyroxine should be taken separately on an "
            "empty stomach according to the prescribed instructions."
        )

    # ------------------------------------------------------
    # DIET CATEGORY EXPLANATION
    # ------------------------------------------------------

    if disease == "low-carb diet":
        t += " Lower-carbohydrate food selection."

    elif disease == "low-fat diet":
        t += " Prepared using lower-fat cooking methods."

    elif disease == "high-protein diet":
        t += " Includes a protein-rich food source."

    elif disease == "balanced diet":
        t += " Designed to provide a balanced meal pattern."

    # ------------------------------------------------------
    # FOOD AVOIDANCES
    # ------------------------------------------------------

    if dislikes:
        avoided_items = [
            item.strip().lower()
            for item in dislikes.split(",")
            if item.strip()
        ]

        for item in avoided_items:

            if item in t.lower():
                t += (
                    f" Avoid {item} and use a suitable alternative."
                )

    return t


# ==========================================================
# GENERATE PERSONALIZED INDIAN DIET
# ==========================================================

def generate_indian_diet(
    disease,
    meals_per_day,
    preference,
    allergies,
    dislikes,
    medications
):

    meal_plan = safe_lower(disease)

    pref = safe_lower(preference)

    # ------------------------------------------------------
    # FALLBACK DIET CATEGORY
    # ------------------------------------------------------

    if meal_plan not in DIET_RULES:
        meal_plan = "none"

    rules = DIET_RULES[meal_plan]

    meal_rules = rules["meals"]

    reason = rules.get(
        "reason",
        "A personalized balanced meal pattern was generated."
    )

    # ------------------------------------------------------
    # BASE MEALS
    # ------------------------------------------------------

    base = [
        ("Breakfast", "Vegetable poha or oats with seasonal fruit."),
        ("Lunch", "Roti, dal, vegetables and salad."),
        ("Dinner", "Light vegetable khichdi or soup.")
    ]

    # ------------------------------------------------------
    # GET REQUESTED NUMBER OF MEALS
    # ------------------------------------------------------

    try:
        number_of_meals = int(meals_per_day)
    except (ValueError, TypeError):
        number_of_meals = 3

    number_of_meals = max(3, min(number_of_meals, 5))

    # ------------------------------------------------------
    # GENERATE MAIN MEALS
    # ------------------------------------------------------

    plan = []

    for meal, default in base[:3]:

        text = meal_rules.get(
            meal,
            default
        )

        text = apply_constraints(
            text,
            preference,
            allergies,
            dislikes,
            meal_plan,
            medications
        )

        plan.append(
            f"{meal}: {text}"
        )

    # ------------------------------------------------------
    # ADDITIONAL SNACKS
    # ------------------------------------------------------

    if number_of_meals >= 4:

        snack_1 = (
            "Mid-Morning Snack: Fresh fruit with "
            "roasted seeds or sprouts."
        )

        snack_1 = apply_constraints(
            snack_1,
            preference,
            allergies,
            dislikes,
            meal_plan,
            medications
        )

        plan.insert(1, snack_1)

    if number_of_meals >= 5:

        snack_2 = (
            "Evening Snack: Roasted chana, sprouts "
            "or a suitable protein-rich snack."
        )

        snack_2 = apply_constraints(
            snack_2,
            preference,
            allergies,
            dislikes,
            meal_plan,
            medications
        )

        plan.insert(-1, snack_2)

    # ------------------------------------------------------
    # PERSONALIZATION MESSAGE
    # ------------------------------------------------------

    personalization = []

    if pref:
        personalization.append(
            f"Diet preference: {preference.title()}"
        )

    if allergies:
        personalization.append(
            f"Allergy restrictions applied: {allergies.title()}"
        )

    if dislikes:
        personalization.append(
            f"Food avoidances considered: {dislikes}"
        )

    if medications:
        personalization.append(
            "Medication-related dietary instructions considered."
        )

    if personalization:

        reason += " " + " ".join(personalization) + "."

    return plan, reason

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# DIET PLANNER
# ==========================================================

@app.route("/dietplanner")
def dietplanner():

    return render_template(
        "dietplanner.html"
    )


# ==========================================================
# RESULT
# ==========================================================

@app.route("/result", methods=["POST"])
def result():

    # ======================================================
    # BASIC INFORMATION
    # ======================================================

    name = request.form.get(
        "name",
        "User"
    ).strip()

    age = request.form.get(
        "age"
    )

    gender = request.form.get(
        "gender"
    )

    height = request.form.get(
        "height"
    )

    weight = request.form.get(
        "weight"
    )

    goal = request.form.get(
        "goal",
        ""
    )

    # ======================================================
    # MEDICAL INFORMATION
    # ======================================================

    disease = safe_lower(
        request.form.get("disease")
    )

    allergies = safe_lower(
        request.form.get("allergies")
    )

    medications = safe_lower(
        request.form.get("medications")
    )

    # ======================================================
    # FOOD INFORMATION
    # ======================================================

    preference = safe_lower(
        request.form.get("preference")
    )

    dislikes = request.form.get(
        "food_avoid",
        ""
    ).strip()

    meals_per_day = request.form.get(
        "meals_per_day",
        "3"
    )

    # ======================================================
    # LIFESTYLE
    # ======================================================

    activity_level = safe_lower(
        request.form.get("activity_level")
    )

    smoking = request.form.get(
        "smoking",
        "No"
    )

    alcohol = request.form.get(
        "alcohol",
        "No"
    )

    # ======================================================
    # OPTIONAL MEDICAL VALUES
    # ======================================================

    bp_systolic = get_optional_int(
        "bp_systolic"
    )

    bp_diastolic = get_optional_int(
        "bp_diastolic"
    )

    blood_sugar = get_optional_int(
        "blood_sugar"
    )

    cholesterol = get_optional_int(
        "cholesterol"
    )

    genetic_risk = request.form.get(
        "genetic_risk",
        "No"
    )

    # ======================================================
    # OPTIONAL LIFESTYLE VALUES
    # ======================================================

    daily_steps = get_optional_int(
        "steps"
    )

    exercise = get_optional_int(
        "exercise"
    )

    sleep = get_optional_float(
        "sleep"
    )

    # ======================================================
    # VALIDATE REQUIRED INFORMATION
    # ======================================================

    if not age or not height or not weight:

        return (
            "Please provide Age, Height and Weight.",
            400
        )

    try:

        age_value = int(age)
        height_value = float(height)
        weight_value = float(weight)

    except ValueError:

        return (
            "Please enter valid Age, Height and Weight values.",
            400
        )

    # ======================================================
    # HEALTH CALCULATIONS
    # ======================================================

    bmi, bmi_category = compute_bmi(
        height_value,
        weight_value
    )

    bmr = bmr_mifflin_st_jeor(
        age_value,
        gender,
        height_value,
        weight_value
    )

    # If no activity level was selected,
    # use a neutral activity factor only for calculation.

    activity_for_calculation = (
        activity_level
        if activity_level
        else "moderately active"
    )

    tdee = int(
        bmr *
        activity_factor(
            activity_for_calculation
        )
    )

    # ======================================================
    # VALUES FOR ML MODEL
    # ======================================================
    #
    # The trained model requires numerical columns.
    # Blank optional values are represented as 0 for the
    # prediction input only.
    #
    # IMPORTANT:
    # These values are NOT presented to the user as actual
    # measurements.
    # ======================================================

    ml_bp_systolic = (
        bp_systolic
        if bp_systolic is not None
        else 0
    )

    ml_bp_diastolic = (
        bp_diastolic
        if bp_diastolic is not None
        else 0
    )

    ml_blood_sugar = (
        blood_sugar
        if blood_sugar is not None
        else 0
    )

    ml_cholesterol = (
        cholesterol
        if cholesterol is not None
        else 0
    )

    ml_steps = (
        daily_steps
        if daily_steps is not None
        else 0
    )

    ml_exercise = (
        exercise
        if exercise is not None
        else 0
    )

    ml_sleep = (
        sleep
        if sleep is not None
        else 0
    )

    # ======================================================
    # ML INPUT DICTIONARY
    # ======================================================

    user_data = {

        "Age": age_value,

        "Gender": gender,

        "Height_cm": height_value,

        "Weight_kg": weight_value,

        "BMI": bmi,

        "Chronic_Disease":
            disease.title()
            if disease and disease != "none"
            else "No Disease",

        "Blood_Pressure_Systolic":
            ml_bp_systolic,

        "Blood_Pressure_Diastolic":
            ml_bp_diastolic,

        "Cholesterol_Level":
            ml_cholesterol,

        "Blood_Sugar_Level":
            ml_blood_sugar,

        "Genetic_Risk_Factor":
            genetic_risk
            if genetic_risk
            else "Unknown",

        "Allergies":
            allergies.title()
            if allergies
            else "None",

        "Daily_Steps":
            ml_steps,

        "Exercise_Frequency":
            ml_exercise,

        "Sleep_Hours":
            ml_sleep,

        "Alcohol_Consumption":
            alcohol
            if alcohol
            else "Unknown",

        "Smoking_Habit":
            smoking
            if smoking
            else "Unknown",

        "Dietary_Habits":
            preference.title()
            if preference
            else "Regular",

        "Preferred_Cuisine":
            "Indian",

        "Food_Aversions":
            dislikes
            if dislikes
            else "None",

        "Caloric_Intake":
            tdee,

        "Protein_Intake":
            75,

        "Carbohydrate_Intake":
            250,

        "Fat_Intake":
            70
    }

    # ======================================================
    # MACHINE LEARNING PREDICTION
    # ======================================================

    predicted_calories = predict_calories(
        user_data
    )

    # ------------------------------------------------------
    # Macronutrients based on predicted calories
    # ------------------------------------------------------

    protein = round(
        (predicted_calories * 0.25) / 4
    )

    carbs = round(
        (predicted_calories * 0.50) / 4
    )

    fat = round(
        (predicted_calories * 0.25) / 9
    )

    # ------------------------------------------------------
    # Meal plan prediction
    # ------------------------------------------------------

    predicted_meal_plan = predict_meal_plan(
        user_data
    )

    # ------------------------------------------------------
    # AI explanation
    # ------------------------------------------------------

    # ======================================================
# AI EXPLANATION INPUT
# ======================================================
# Do NOT use ML fallback zeros for explanation.
# Explanation should only use values actually entered
# by the user.

    explanation_data = user_data.copy()

    explanation_data["Blood_Pressure_Systolic"] = bp_systolic
    explanation_data["Blood_Pressure_Diastolic"] = bp_diastolic
    explanation_data["Blood_Sugar_Level"] = blood_sugar
    explanation_data["Cholesterol_Level"] = cholesterol
    explanation_data["Daily_Steps"] = daily_steps
    explanation_data["Exercise_Frequency"] = exercise
    explanation_data["Sleep_Hours"] = sleep

    explanation = explain_prediction(
        explanation_data
    )
    # ======================================================
    # EXPERT SYSTEM CALCULATIONS
    # ======================================================

    # Only calculate the lifestyle health score when
    # the required lifestyle information is actually given.

    lifestyle_complete = (
        daily_steps is not None
        and exercise is not None
        and sleep is not None
    )

    if lifestyle_complete:

        health_score, health_status = (
            calculate_health_score(
                bmi,
                disease,
                smoking,
                alcohol,
                sleep,
                exercise,
                daily_steps
            )
        )

    else:

        health_score = None

        health_status = (
            "Insufficient lifestyle data"
        )

    # ======================================================
    # WATER
    # ======================================================

    water = calculate_water(
        weight_value
    )

    # ======================================================
    # MACRONUTRIENTS
    # ======================================================

    protein_g, carbs_g, fat_g = (
        calculate_macros(
            predicted_calories
        )
    )

    # ======================================================
    # DAILY GOALS
    # ======================================================

    goals = daily_goals(
        activity_for_calculation
    )

    # ======================================================
    # EXPERT SYSTEM DIET
    # ======================================================

    diet, expert_reason = (
        generate_indian_diet(

            predicted_meal_plan,

            meals_per_day,

            preference,

            allergies,

            dislikes,

            medications
        )
    )

    # ======================================================
    # HEALTH SUMMARY
    # ======================================================

    reasoning = (

        f"BMI : {bmi:.2f} "
        f"({bmi_category})<br>"

        f"BMR : {int(bmr)} kcal/day<br>"

        f"TDEE : {tdee} kcal/day<br>"

        f"AI Predicted Calories : "
        f"{predicted_calories} kcal/day<br>"

        f"AI Recommended Meal Plan : "
        f"{predicted_meal_plan}"

    )

    # ======================================================
    # OPTIONAL PARAMETER MESSAGES
    # ======================================================

    parameter_messages = []

    if bp_systolic is None or bp_diastolic is None:

        parameter_messages.append(
            "Blood pressure was not provided."
        )

    if blood_sugar is None:

        parameter_messages.append(
            "Blood sugar level was not provided."
        )

    if cholesterol is None:

        parameter_messages.append(
            "Cholesterol level was not provided."
        )

    if daily_steps is None:

        parameter_messages.append(
            "Average daily steps were not provided."
        )

    if exercise is None:

        parameter_messages.append(
            "Exercise frequency was not provided."
        )

    if sleep is None:

        parameter_messages.append(
            "Average sleep duration was not provided."
        )

    # ======================================================
    # RESULT PAGE
    # ======================================================

    return render_template(

        "result.html",

        name=name,

        bmi=bmi,

        bmi_cat=bmi_category,

        bmr=int(bmr),

        tdee=tdee,

        calories=predicted_calories,

        meal_plan=predicted_meal_plan,

        diet=diet,

        expert_reason=expert_reason,

        reasoning=reasoning,

        explanation=explanation,

        macro={

            "protein": protein_g,

            "carbs": carbs_g,

            "fat": fat_g
        },

        health_score=health_score,

        health_status=health_status,

        water=water,

        goals=goals,

        parameter_messages=parameter_messages

    )


# ==========================================================
# OPEN BROWSER
# ==========================================================

def open_browser():

    webbrowser.open_new(
        "http://127.0.0.1:5000/"
    )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    threading.Timer(
        1.2,
        open_browser
    ).start()

    app.run(
        debug=True,
        use_reloader=False
    )