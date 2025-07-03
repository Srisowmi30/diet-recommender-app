import streamlit as st
import pandas as pd

# Load dataset safely
try:
    food_df = pd.read_csv("food_data.csv")
except:
    st.error("❌ Could not load 'food_data.csv'. Please check the file.")
    st.stop()

# App title
st.title("🥗 Personalized Diet Recommender")

# User inputs
name = st.text_input("Enter your name:")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0)
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)

goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Weight Maintain"])
diet_type = st.selectbox("Diet Type", ["Veg", "Vegan", "Non-Veg"])

# Recommend meals only if all fields are filled
if name and age and weight and height:

    # Normalize diet type filtering
    filtered = food_df[food_df['Diet Type'].str.strip().str.lower() == diet_type.strip().lower()]

    # Goal-based calorie filtering
    if goal == "Weight Loss":
        goal_df = filtered[filtered["Calories"] < 250]
    elif goal == "Weight Gain":
        goal_df = filtered[filtered["Calories"] > 400]
    else:  # Weight Maintain
        goal_df = filtered[(filtered["Calories"] >= 250) & (filtered["Calories"] <= 400)]

    # Safe sampling
    if len(goal_df) >= 3:
        meals = goal_df.sample(3)
    elif len(goal_df) > 0:
        meals = goal_df
    else:
        meals = pd.DataFrame()

    # Display results
    if not meals.empty:
        st.subheader("🍽️ Recommended Meals:")
        st.table(meals.reset_index(drop=True))
    else:
        st.warning("⚠️ No matching meals found. Try changing your goal or diet type.")
