import sqlite3
import requests
import datetime
import json

DB_PATH = "farm_data.db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def fetch_input_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM soil_data WHERE crop_type IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    columns = ["id", "soil_type", "moisture", "ph", "crop_type", "timestamp", "location"]
    data = [dict(zip(columns, row)) for row in rows]
    return data


def call_ollama(prompt):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response")
    except Exception as e:
        return f"❌ Error: {e}"


def store_ollama_output(record_id, response_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO ollama_predictions (farm_input_id, timestamp, prediction)
        VALUES (?, ?, ?)
    ''', (
        record_id,
        datetime.datetime.now().isoformat(),
        response_text
    ))

    conn.commit()
    conn.close()


def run_yield_predictor():
    input_data = fetch_input_data()

    for record in input_data:
        prompt = (
            f"Based on the following soil data:\n"
            f"Soil Type: {record['soil_type']}\n"
            f"Moisture: {record['moisture']}\n"
            f"pH: {record['ph']}\n"
            f"Crop Type: {record['crop_type']}\n"
            f"Location: {record['location']}\n"
            f"Suggest ways to improve yield."
        )

        print(f"\nGenerated Prompt:\n{prompt}")
        response = call_ollama(prompt)
        print(f"\nOllama Response:\n{response}")

        if response.startswith("❌ Error"):
            print(f"Error while calling Ollama: {response}")
        else:
            store_ollama_output(record['id'], response)


if __name__ == "__main__":
    run_yield_predictor()
