# ==========================================================
# AI DIET EXPERT SYSTEM
# Rule-Based Personalized Meal Database
# ==========================================================


DIET_RULES = {

    # ======================================================
    # BALANCED DIET
    # ======================================================

    "balanced diet": {

        "reason":
            "A balanced meal pattern was selected based on the predicted dietary requirement.",

        "meals": {

            "Breakfast":
                "Vegetable poha with sprouts, seasonal fruit and a protein source.",

            "Lunch":
                "2 whole-wheat rotis, dal, mixed vegetable curry, salad and curd.",

            "Dinner":
                "Vegetable khichdi with paneer/tofu and steamed vegetables."
        }
    },


    # ======================================================
    # LOW-CARB DIET
    # ======================================================

    "low-carb diet": {

        "reason":
            "The predicted meal category emphasizes controlled carbohydrate intake while maintaining adequate protein and vegetables.",

        "meals": {

            "Breakfast":
                "Vegetable omelette with sprouts, cucumber and unsweetened beverage.",

            "Lunch":
                "Grilled chicken/paneer with sautéed vegetables, leafy greens and salad.",

            "Dinner":
                "Grilled fish/tofu with broccoli, cucumber and vegetable soup."
        }
    },


    # ======================================================
    # LOW-FAT DIET
    # ======================================================

    "low-fat diet": {

        "reason":
            "The predicted meal category emphasizes lower-fat cooking methods and nutrient-dense foods.",

        "meals": {

            "Breakfast":
                "Vegetable oats or idli with sambar and fresh fruit.",

            "Lunch":
                "Steamed rice, dal, mixed vegetables and fresh salad.",

            "Dinner":
                "Vegetable soup with roti and grilled vegetables."
        }
    },


    # ======================================================
    # HIGH-PROTEIN DIET
    # ======================================================

    "high-protein diet": {

        "reason":
            "The predicted meal category emphasizes protein-rich food sources to support daily protein requirements.",

        "meals": {

            "Breakfast":
                "Egg omelette/paneer bhurji with sprouts and whole-grain toast.",

            "Lunch":
                "Grilled chicken/fish/paneer with dal, vegetables and salad.",

            "Dinner":
                "Chicken/fish/tofu with vegetables and a small serving of whole grains."
        }
    },


    # ======================================================
    # FALLBACK
    # ======================================================

    "none": {

        "reason":
            "A balanced meal pattern was generated because no specific dietary category was available.",

        "meals": {

            "Breakfast":
                "Vegetable poha or oats with seasonal fruit and sprouts.",

            "Lunch":
                "Roti, dal, vegetables, salad and a protein source.",

            "Dinner":
                "Light vegetable khichdi or soup with a suitable protein source."
        }
    }

}