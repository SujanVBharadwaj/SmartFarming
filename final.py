import sqlite3
import json
import datetime
import requests
from initdb import initialize_database
from weatherfinal import load_data, predict_weather_2025_q2_q3, recommend_crop

DB_PATH = "farm_data.db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def generate_yield_prompt(record, crop_type):
    return f"""
You are an agricultural advisor.

Based on the following farm data, estimate the crop yield in quintals/hectare and briefly explain your reasoning.

Soil Type: {record['soil_type']}
Crop Type: {crop_type}
Rainfall: {record['rainfall']} mm
Temperature: {record['temperature']} °C
Fertilizer Usage: {record['moisture']} kg/hectare

Respond in the format:
"Predicted Yield: XX quintals/hectare. Reason: ..."
"""

def call_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

def fetch_soil_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM soil_data")
    data = cursor.fetchall()
    conn.close()
    return data

def store_prediction(record_id, prediction):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ollama_predictions (farm_input_id, timestamp, prediction)
        VALUES (?, ?, ?)
    ''', (record_id, datetime.datetime.now().isoformat(), prediction))
    conn.commit()
    conn.close()

def store_crop_recommendation(city, crop):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO crop_recommendations (timestamp, crops, location)
        VALUES (?, ?, ?)
    ''', (datetime.datetime.now().isoformat(), crop, city))
    conn.commit()
    conn.close()

def main():
    initialize_database(DB_PATH)
    
    city = input("Enter city (bhopal, nagpur, ludhiana): ").strip().lower()

    try:
        data_2024, data_2025 = load_data(city)
        weather_pred = predict_weather_2025_q2_q3(data_2024, data_2025)

        print(f"\n📊 Predicted Weather for {city.title()} (Q2/Q3 2025):")
        print(json.dumps(weather_pred, indent=2))

        crop = recommend_crop(weather_pred)
        print(f"\n🌱 Recommended Crop: {crop}")
        store_crop_recommendation(city, crop)

        soil_data = fetch_soil_data()
        for record in soil_data:
            prompt = generate_yield_prompt(record, crop)
            print(f"\n🧠 Predicting Yield for Farm Input ID {record['id']}...")
            response = call_ollama(prompt)
            print(response)
            store_prediction(record['id'], response)

    except FileNotFoundError:
        print("❌ JSON weather files not found for the city.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
