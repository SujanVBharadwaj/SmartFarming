import streamlit as st
import json
import os
from yieldpredictor import run_yield_predictor
from weatherfinal import load_data, predict_weather_2025_q2_q3, recommend_crop

st.set_page_config(page_title="Crop Advisor", layout="centered")

st.title("🌾 Crop Advisor Dashboard")
st.write("Get crop recommendations and yield predictions based on soil and weather data.")

# --- Weather Prediction Section ---
st.header("📍 Weather-Based Crop Recommendation")

city = st.selectbox("Select a city", ["bhopal", "nagpur", "ludhiana"])
predict_btn = st.button("Predict Weather & Recommend Crop")

if predict_btn:
    try:
        data_2024, data_2025 = load_data(city)
        predicted = predict_weather_2025_q2_q3(data_2024, data_2025)
        crop = recommend_crop(predicted)

        st.subheader("🔮 Predicted Weather (Q2/Q3 2025)")
        st.json(predicted)

        st.subheader("🌱 Recommended Crop")
        st.success(crop.title() if crop != "No ideal crop found for given conditions." else crop)

    except FileNotFoundError:
        st.error("❌ Missing JSON data files for the selected city.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

# --- Yield Prediction Section ---
st.header("📈 AI-Powered Yield Prediction")

if st.button("Run Yield Predictor"):
    with st.spinner("Calling Ollama and generating yield predictions..."):
        try:
            prediction, generated_prompt = run_yield_predictor("farm_data.db")
            st.success("✅ Yield predictions completed and stored.")

            st.subheader("🧠 Generated Prompt")
            st.code(generated_prompt, language="text")  # Display prompt like in your screenshot

            st.subheader("🤖 Ollama Response")
            st.write(prediction)

        except Exception as e:
            st.error(f"❌ An error occurred during prediction: {e}")

st.caption("Powered by OpenAI, Ollama, and Streamlit.")
