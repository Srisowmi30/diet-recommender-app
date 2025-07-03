import streamlit as st
import pandas as pd
import random

# 1. Load the CSV
try:
    food_df = pd.read_csv("food_data.csv")
except Exception as e:
    st.error("❌ Could not load the CSV file. Please check the file and its columns.")
    st.stop()

# 2. Clean columns
food_df.columns = food_df.columns.str.strip().str.title()

st.title("🥗 Personalized Diet Recommender")

# 3. User Inputs
name = st.text_input("Enter your name:")
age = st.number_input("Age", min_value=1, max_value=120)
weight = st.number_input("Weight (kg)", min_value=1.0)
height = st.number_input("Height (cm)", min_value=50.0)
goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Weight Maintain"])
diet_type = st.selectbox("Diet Type", ["Veg", "Vegan", "Non-Veg"])

# Proceed only if all fields are filled
if name and age and weight and height:
    # 4. Filter by Diet Type
    filtered_df = food_df[food_df["Type"].str.strip().str.lower() == diet_type.lower().strip()]

    # 5. Filter by goal
    if goal == "Weight Loss":
        goal_df = filtered_df[filtered_df["Calories"] < 250]
    elif goal == "Weight Gain":
        goal_df = filtered_df[filtered_df["Calories"] > 400]
    else:
        goal_df = filtered_df[
            (filtered_df["Calories"] >= 250) & (filtered_df["Calories"] <= 400)
        ]

    # 6. Convert DataFrame rows to list of dicts
    meals_list = goal_df.to_dict(orient="records")

    # 7. Safe sampling via Python
    st.subheader("🍽️ Recommended Meals:")
    if len(meals_list) == 0:
        st.warning("⚠️ No matching meals found. Try a different combination.")
    else:
        # Choose up to 3 meals
        selected = random.sample(meals_list, k=min(3, len(meals_list)))
        st.table(pd.DataFrame(selected))
