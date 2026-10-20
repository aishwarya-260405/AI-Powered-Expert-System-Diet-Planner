import joblib
import pandas as pd


# ==============================
# LOAD SAVED OBJECTS
# ==============================

calorie_model = joblib.load("models/calorie_model.pkl")

diet_classifier = joblib.load("models/diet_classifier.pkl")

preprocessor = joblib.load("models/preprocessor.pkl")

encoder = joblib.load("models/encoder.pkl")


# ==============================
# PREPARE DATA
# ==============================

def prepare_input(user_data):

    df = pd.DataFrame([user_data])

    processed = preprocessor.transform(df)

    return processed


# ==============================
# CALORIE PREDICTION
# ==============================

def predict_calories(user_data):

    processed = prepare_input(user_data)

    prediction = calorie_model.predict(processed)

    return int(prediction[0])


# ==============================
# MEAL PLAN PREDICTION
# ==============================

def predict_meal_plan(user_data):

    processed = prepare_input(user_data)

    prediction = diet_classifier.predict(processed)

    meal_plan = encoder.inverse_transform(prediction)

    return meal_plan[0]