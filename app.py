import streamlit as st
import pandas as pd

# Load dataset safely
try:
    food_df = pd.read_csv("food_data.csv")
except Exception as e:
    st.error("❌ Could not load 'food_data.csv'. Please check the file format and location.")
    st.exception(e)
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

# Proceed only if inputs are valid
if name and age and weight and height:

    # Filter by Diet Type (case-insensitive match)
    # Normalize column names
    # Normalize column names
# Normalize column names
    food_df.columns = food_df.columns.str.strip().str.title()

# Filter by Diet Type (your column is 'Type')
filtered_df = food_df[
    food_df["Type"].str.strip().str.lower() == diet_type.strip().lower()
]

# Debug info
st.write("✅ Filtered by Diet Type:", filtered_df.shape[0])

# Apply goal-based calorie filtering
if goal == "Weight Loss":
    goal_df = filtered_df[filtered_df["Calories"] < 250]
elif goal == "Weight Gain":
    goal_df = filtered_df[filtered_df["Calories"] > 400]
else:  # Maintain
    goal_df = filtered_df[(filtered_df["Calories"] >= 250) & (filtered_df["Calories"] <= 400)]

# Debug info
st.write("🎯 Meals after Goal filter:", goal_df.shape[0])

# Safely show meals
try:
    if goal_df.empty:
        st.warning("⚠️ No matching meals found for your selected diet and goal.")
    elif goal_df.shape[0] < 3:
        st.info(f"Only {goal_df.shape[0]} meals found. Showing all available meals.")
        st.subheader("🍽️ Recommended Meals:")
        st.table(goal_df.reset_index(drop=True))
    else:
        meals = goal_df.sample(n=3, random_state=42)
        st.subheader("🍽️ Recommended Meals:")
        st.table(meals.reset_index(drop=True))
except Exception as e:
    st.error("❌ Error while selecting meals.")
    st.exception(e)
