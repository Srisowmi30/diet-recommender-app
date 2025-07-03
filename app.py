import streamlit as st
import pandas as pd
from utils.helpers import calculate_bmi

st.set_page_config(page_title="Personalized Diet Recommender", page_icon="🍽️")

st.title("🍽️ Personalized Diet Recommender")

# User inputs
name = st.text_input("Enter your name:")
age = st.number_input("Age", min_value=10, max_value=100)
weight = st.number_input("Weight (kg)", min_value=30.0)
height = st.number_input("Height (cm)", min_value=100.0)
goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Maintain"])
diet_type = st.selectbox("Diet Type", ["Veg", "Non-Veg", "Vegan"])

import os

# Load dataset
try:
    food_df = pd.read_csv("food_data.csv")
except:
    st.error("❌ Could not load 'food_data.csv'. Please check the file.")

# Button to generate plan
if st.button("Generate Plan"):
    if name and height and weight:
        bmi = calculate_bmi(weight, height)
        st.success(f"Hello {name}, your BMI is {bmi:.2f} 💪")

        st.subheader("🍱 Recommended Meals:")
        # Simple filtering based on diet type
        filtered = food_df[food_df['Diet Type'].str.strip().str.lower() == diet_type.strip().lower()]

        if goal == "Weight Loss":
            meals = filtered[filtered['Calories'] < 250].sample(3)
        elif goal == "Weight Gain":
            meals = filtered[filtered['Calories'] > 300].sample(3)
        else:
            meals = filtered[(filtered['Calories'] >= 250) & (filtered['Calories'] <= 300)].sample(3)

        st.dataframe(meals.reset_index(drop=True))
    else:
        st.warning("⚠️ Please fill in all the required fields.")
