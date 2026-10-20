# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    LabelEncoder
)

from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestClassifier
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report
)

print("=" * 60)
print("DIET EXPERT SYSTEM MODEL TRAINING")
print("=" * 60)


# ==========================================================
# CREATE MODEL DIRECTORY
# ==========================================================

os.makedirs("models", exist_ok=True)


# ==========================================================
# LOAD DATASET
# ==========================================================

print("\nLoading Dataset...")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_patient_dataset.csv"
)

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully.")
print("Shape :", df.shape)


# ==========================================================
# DEFINE TARGETS
# ==========================================================

X = df.drop(
    columns=[
        "Recommended_Calories",
        "Recommended_Protein",
        "Recommended_Carbs",
        "Recommended_Fats",
        "Recommended_Meal_Plan"
    ]
)

y_reg = df["Recommended_Calories"]

y_cls = df["Recommended_Meal_Plan"]


# ==========================================================
# NUMERICAL & CATEGORICAL FEATURES
# ==========================================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

print("\nNumerical Features :", len(numerical_features))
print("Categorical Features :", len(categorical_features))


# ==========================================================
# LABEL ENCODER
# ==========================================================

encoder = LabelEncoder()

y_cls_encoded = encoder.fit_transform(y_cls)


# ==========================================================
# PREPROCESSOR
# ==========================================================

preprocessor = ColumnTransformer(

    transformers=[

        (

            "num",

            StandardScaler(),

            numerical_features

        ),

        (

            "cat",

            OneHotEncoder(

                handle_unknown="ignore"

            ),

            categorical_features

        )

    ]

)


print("\nPreprocessor Created Successfully.")

# ==========================================================
# TRAIN / VALIDATION SPLIT
# ==========================================================

print("\nSplitting Dataset...")

X_train, X_test, y_reg_train, y_reg_test = train_test_split(
    X,
    y_reg,
    test_size=0.20,
    random_state=42
)

_, _, y_cls_train, y_cls_test = train_test_split(
    X,
    y_cls_encoded,
    test_size=0.20,
    random_state=42
)

print("Training Samples :", X_train.shape[0])
print("Testing Samples  :", X_test.shape[0])


# ==========================================================
# PREPROCESSING
# ==========================================================

print("\nApplying Preprocessing...")

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

print("Training Shape :", X_train_processed.shape)
print("Testing Shape  :", X_test_processed.shape)


# ==========================================================
# SAVE PREPROCESSOR
# ==========================================================

joblib.dump(
    preprocessor,
    "models/preprocessor.pkl"
)

print("\nPreprocessor Saved Successfully.")

# ==========================================================
# TRAIN REGRESSION MODEL
# ==========================================================

print("\n" + "=" * 60)
print("TRAINING CALORIE REGRESSION MODEL")
print("=" * 60)

regressor = GradientBoostingRegressor(
    random_state=42
)

regressor.fit(
    X_train_processed,
    y_reg_train
)

print("Regression Model Trained Successfully.")


# ==========================================================
# REGRESSION PREDICTIONS
# ==========================================================

y_reg_pred = regressor.predict(
    X_test_processed
)


# ==========================================================
# REGRESSION METRICS
# ==========================================================

mae = mean_absolute_error(
    y_reg_test,
    y_reg_pred
)

rmse = mean_squared_error(
    y_reg_test,
    y_reg_pred
) ** 0.5

r2 = r2_score(
    y_reg_test,
    y_reg_pred
)

print("\nRegression Performance")
print("----------------------------")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


# ==========================================================
# SAVE REGRESSION MODEL
# ==========================================================

joblib.dump(
    regressor,
    "models/calorie_model.pkl"
)

print("\ncalorie_model.pkl Saved Successfully.")


# ==========================================================
# TRAIN MEAL PLAN CLASSIFIER
# ==========================================================

print("\n" + "=" * 60)
print("TRAINING DIET CLASSIFIER")
print("=" * 60)

classifier = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

classifier.fit(
    X_train_processed,
    y_cls_train
)

print("Diet Classifier Trained Successfully.")


# ==========================================================
# CLASSIFICATION PREDICTIONS
# ==========================================================

y_cls_pred = classifier.predict(
    X_test_processed
)


# ==========================================================
# CLASSIFICATION METRICS
# ==========================================================

accuracy = accuracy_score(
    y_cls_test,
    y_cls_pred
)

print("\nClassification Performance")
print("----------------------------")
print(f"Accuracy : {accuracy:.4f}")

print("\nClassification Report")
print(classification_report(
    y_cls_test,
    y_cls_pred
))


# ==========================================================
# SAVE CLASSIFIER
# ==========================================================

joblib.dump(
    classifier,
    "models/diet_classifier.pkl"
)

print("\ndiet_classifier.pkl Saved Successfully.")

# ==========================================================
# SAVE LABEL ENCODER
# ==========================================================

joblib.dump(
    encoder,
    "models/encoder.pkl"
)

print("encoder.pkl Saved Successfully.")