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

# Proceed only if user enters all info
if name and age and weight and height:

    # Filter by diet type (case-insensitive)
    filtered = food_df[food_df['Diet Type'].str.strip().str.lower() == diet_type.strip().lower()]

    # Apply goal-based calorie filtering
    if goal == "Weight Loss":
        goal_df = filtered[filtered["Calories"] < 250]
    elif goal == "Weight Gain":
        goal_df = filtered[filtered["Calories"] > 400]
    else:  # Weight Maintain
        goal_df = filtered[(filtered["Calories"] >= 250) & (filtered["Calories"] <= 400)]

    # Display based on how many results are available
    if goal_df.empty:
        st.warning("⚠️ No meals found. Try changing the goal or diet type.")
    else:
        try:
            meals = goal_df.sample(n=3) if len(goal_df) >= 3 else goal_df
            st.subheader("🍽️ Recommended Meals:")
            st.table(meals.reset_index(drop=True))
        except:
            st.error("⚠️ Error while sampling meals. Please check your data.")
