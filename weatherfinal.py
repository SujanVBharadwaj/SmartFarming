import json

# Example thresholds for crops (very basic, tune as needed)
CROP_CONDITIONS = {
    'wheat':    {'tavg': (10, 25), 'prcp': (0, 100)},
    'rice':     {'tavg': (20, 35), 'prcp': (150, 500)},
    'soybean':  {'tavg': (20, 32), 'prcp': (75, 300)},
    'corn':     {'tavg': (18, 30), 'prcp': (50, 200)}
}

def load_data(city):
    with open(f"{city}_2024_avg.json") as f2024, open(f"{city}_avg_2025.json") as f2025:
        return json.load(f2024), json.load(f2025)

def predict_quarter_value(prev, curr):
    return curr + (curr - prev)

def predict_weather_2025_q2_q3(data_2024, data_2025):
    prediction = {}
    for key in ['tavg', 'prcp']:
        prev = data_2024.get(key)
        curr = data_2025.get(key)
        if prev is not None and curr is not None:
            prediction[key] = round(predict_quarter_value(prev, curr), 2)
        else:
            print(f"⚠️ Warning: Missing data for {key}")
    return prediction

def recommend_crop(predicted):
    t, r = predicted.get('tavg'), predicted.get('prcp')
    if t is None or r is None:
        return "Insufficient data"
    
    for crop, cond in CROP_CONDITIONS.items():
        if cond['tavg'][0] <= t <= cond['tavg'][1] and cond['prcp'][0] <= r <= cond['prcp'][1]:
            return crop
    return "No ideal crop found for given conditions."

def main():
    city = input("Enter city (bhopal, nagpur, ludhiana): ").strip().lower()
    try:
        data_2024, data_2025 = load_data(city)
        predicted = predict_weather_2025_q2_q3(data_2024, data_2025)

        print(f"\n📊 Predicted Q2/Q3 2025 weather for {city.title()}:")
        print(json.dumps(predicted, indent=2))

        crop = recommend_crop(predicted)
        print(f"\n🌾 Recommended crop: {crop.title() if crop and crop != 'Insufficient data' else crop}")

    except FileNotFoundError:
        print("❌ Missing JSON files for the selected city.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
