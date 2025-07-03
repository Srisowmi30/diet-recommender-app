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
    food_df.columns = food_df.columns.str.strip().str.title()

# Filter by Diet Type (column is actually 'Type' in your CSV)
filtered_df = food_df[food_df['Type'].str.strip().str.lower() == diet_type.strip().lower()]

# Show debug info
st.write("🔍 Filtered rows:", filtered_df.shape[0])

# Filter based on goal
if goal == "Weight Loss":
    goal_df = filtered_df[filtered_df["Calories"] < 250]
elif goal == "Weight Gain":
    goal_df = filtered_df[filtered_df["Calories"] > 400]
else:
    goal_df = filtered_df[(filtered_df["Calories"] >= 250) & (filtered_df["Calories"] <= 400)]

st.write("🎯 Rows after goal filter:", goal_df.shape[0])

# Safe meal sampling
try:
    if goal_df.empty or goal_df.shape[0] == 0:
        st.warning("⚠️ No meals found. Try changing your goal or diet type.")
    elif goal_df.shape[0] < 3:
        st.info(f"Only {goal_df.shape[0]} meals found. Showing all available meals.")
        st.subheader("🍽️ Recommended Meals:")
        st.table(goal_df.reset_index(drop=True))
    else:
        meals = goal_df.sample(n=3, replace=False, random_state=42)
        st.subheader("🍽️ Recommended Meals:")
        st.table(meals.reset_index(drop=True))
except Exception as e:
    st.error("❌ An error occurred while selecting meals.")
    st.exception(e)
