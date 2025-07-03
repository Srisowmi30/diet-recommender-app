import streamlit as st
import pandas as pd

# Load the dataset
try:
    food_df = pd.read_csv("food_data.csv")
except Exception as e:
    st.error("❌ Could not load 'food_data.csv'. Please check the file format.")
    st.stop()

# Clean column names
food_df.columns = food_df.columns.str.strip().str.title()

st.title("🥗 Personalized Diet Recommender")

# Inputs
name = st.text_input("Enter your name:")
age = st.number_input("Age", min_value=1, max_value=120)
weight = st.number_input("Weight (kg)", min_value=1.0)
height = st.number_input("Height (cm)", min_value=50.0)

goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Weight Maintain"])
diet_type = st.selectbox("Diet Type", ["Veg", "Vegan", "Non-Veg"])

# Proceed only if inputs are filled
if name and age and weight and height:

    # Filter by diet type (your CSV uses 'Type' column)
    filtered_df = food_df[
        food_df["Type"].str.strip().str.lower() == diet_type.strip().lower()
    ]

    # Apply calorie filter based on goal
    if goal == "Weight Loss":
        goal_df = filtered_df[filtered_df["Calories"] < 250]
    elif goal == "Weight Gain":
        goal_df = filtered_df[filtered_df["Calories"] > 400]
    else:
        goal_df = filtered_df[
            (filtered_df["Calories"] >= 250) & (filtered_df["Calories"] <= 400)
        ]

    # Show meal suggestions
    st.subheader("🍽️ Recommended Meals:")

    if goal_df.empty:
        st.warning("⚠️ No meals match your selection. Try changing your goal or diet type.")
    else:
        if len(goal_df) >= 3:
            st.table(goal_df.sample(3, random_state=1).reset_index(drop=True))
        else:
            st.info(f"Only {len(goal_df)} meals available. Showing all.")
            st.table(goal_df.reset_index(drop=True))
