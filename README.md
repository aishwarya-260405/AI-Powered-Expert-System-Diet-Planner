# 🥗 AI-Powered Expert System for Personalized Indian Diet Planning

An intelligent diet-planning web application that combines Machine Learning and a rule-based Expert System to generate personalized Indian diet recommendations based on user health information and dietary preferences.

## 📌 Project Overview

Maintaining a balanced diet is important for overall health and well-being. However, dietary requirements can vary depending on an individual's health condition, body measurements, activity level, and food preferences.

This project aims to provide personalized diet recommendations by integrating machine learning predictions with expert-defined dietary rules. The application uses a Flask-based web interface to collect user information and present relevant dietary suggestions.

## 🎯 Objectives

- Develop an intelligent system for personalized Indian diet planning.
- Apply machine learning to support diet classification and calorie prediction.
- Integrate a rule-based expert system for dietary recommendations.
- Consider dietary preferences and food restrictions when generating meal suggestions.
- Provide a simple and user-friendly web interface.
- Explore how AI techniques can support personalized nutrition planning.

## ✨ Key Features

- **Personalized Diet Planning:** Generates diet suggestions based on user-provided information.
- **Machine Learning Integration:** Uses trained models for diet classification and calorie prediction.
- **Rule-Based Expert System:** Applies predefined dietary rules to generate recommendations.
- **Health Information Processing:** Processes relevant health and lifestyle inputs.
- **Dietary Preferences:** Supports consideration of food preferences and restrictions.
- **Web-Based Interface:** Provides an interactive interface built using Flask, HTML, and CSS.
- **Health Insights:** Includes utilities for health scoring, water intake estimation, and nutritional recommendations.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Trained classification and regression models |
| Frontend | HTML, CSS |
| Data Processing | Feature Engineering, Data Preprocessing |
| Development Tools | Jupyter Notebook, Git, GitHub |

## 🧠 System Architecture

The application combines machine learning and expert-system components to generate dietary recommendations.

1. **User Input:** Collects relevant health information, lifestyle details, and dietary preferences.
2. **Data Preprocessing:** Processes user inputs into a format suitable for prediction.
3. **Feature Engineering:** Prepares relevant features for the trained models.
4. **Machine Learning Prediction:** Uses trained models to support diet classification and calorie prediction.
5. **Expert-System Reasoning:** Applies predefined rules to generate dietary recommendations.
6. **Personalized Output:** Presents the resulting diet suggestions through the Flask web application.

## 📂 Project Structure

```text
AI-Powered-Expert-System-Diet-Planner/
│
├── app.py
├── config.py
├── requirements.txt
│
├── core/
│   ├── feature_engineering.py
│   ├── health.py
│   ├── preprocess.py
│   └── utils.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── splits/
│   └── generate_dataset.py
│
├── expert/
│   ├── diet_rules.py
│   ├── explanation.py
│   └── inference_engine.py
│
├── ml/
│   ├── calorie_model.py
│   ├── diet_classifier.py
│   ├── evaluate_model.py
│   ├── predict.py
│   └── train_model.py
│
├── models/
│   ├── calorie_model.pkl
│   ├── diet_classifier.pkl
│   └── saved_objects/
│
├── notebooks/
│   └── Data analysis, preprocessing, and model development notebooks
│
├── reports/
│   ├── figures/
│   ├── insights/
│   └── metrics/
│
├── static/
│   ├── css/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── dietplanner.html
│   ├── result.html
│   ├── navbar.html
│   └── footer.html
│
└── utils/
    ├── explain.py
    ├── health_score.py
    └── recommendations.py
