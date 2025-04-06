import sqlite3
from datetime import datetime
from initdb import initialize_database

class CropAdvisor:
    def __init__(self, db_path="farm_data.db"):
        initialize_database(db_path)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_soil_data(self, location):
        self.cursor.execute("SELECT * FROM soil_data WHERE location = ? ORDER BY timestamp DESC LIMIT 1;", (location,))
        return self.cursor.fetchone()

    def get_weather_forecast(self, location):
        self.cursor.execute("SELECT * FROM weather_forecast WHERE location = ? ORDER BY timestamp DESC LIMIT 1;", (location,))
        return self.cursor.fetchone()

    def recommend_crops(self, soil_data, weather_data):
        soil_type = soil_data[1]
        moisture = soil_data[2]
        temperature = weather_data[1]

        if soil_type == "Loamy" and moisture > 50 and 20 <= temperature <= 30:
            return ["Wheat", "Corn", "Rice"]
        elif soil_type == "Sandy" and moisture < 40:
            return ["Corn", "Soyabean"]
        else:
            return ["Rice", "Wheat"]

    def analyze(self, location="Bhopal"):
        soil = self.get_soil_data(location)
        weather = self.get_weather_forecast(location)
        if soil and weather:
            crops = self.recommend_crops(soil, weather)
            result = {
                "timestamp": datetime.now().isoformat(),
                "location": location,
                "recommended_crops": crops
            }
            self.store_recommendation(result)
            return result
        else:
            return {"error": f"Insufficient data to provide recommendation for {location}."}

    def store_recommendation(self, result):
        self.cursor.execute(
            "INSERT INTO crop_recommendations (timestamp, crops, location) VALUES (?, ?, ?)",
            (result["timestamp"], ", ".join(result["recommended_crops"]), result["location"])
        )
        self.conn.commit()

    def insert_sample_data(self):
        now = datetime.now().isoformat()
        samples = [
            ("Loamy", 60, now, "Bhopal"),
            ("Sandy", 30, now, "Nagpur"),
            ("Clay", 55, now, "Ludhiana")
        ]
        for soil_type, moisture, timestamp, loc in samples:
            self.cursor.execute(
                "INSERT INTO soil_data (soil_type, moisture, timestamp, location) VALUES (?, ?, ?, ?)",
                (soil_type, moisture, timestamp, loc)
            )
        forecasts = [
            (25.5, 10, now, "Bhopal"),
            (32.0, 5, now, "Nagpur"),
            (22.0, 12, now, "Ludhiana")
        ]
        for temp, rain, timestamp, loc in forecasts:
            self.cursor.execute(
                "INSERT INTO weather_forecast (temperature, rainfall, timestamp, location) VALUES (?, ?, ?, ?)",
                (temp, rain, timestamp, loc)
            )
        self.conn.commit()

    def print_all_data(self):
        print("🌱 Soil Data:")
        for row in self.cursor.execute("SELECT * FROM soil_data;"):
            print(row)

        print("\n☀️ Weather Data:")
        for row in self.cursor.execute("SELECT * FROM weather_forecast;"):
            print(row)

        print("\n📊 Recommendations:")
        for row in self.cursor.execute("SELECT * FROM crop_recommendations;"):
            print(row)

if __name__ == "__main__":
    advisor = CropAdvisor()
    advisor.insert_sample_data()

    for loc in ["Bhopal", "Nagpur", "Ludhiana"]:
        result = advisor.analyze(loc)
        print(f"\n🌾 Crop Recommendation for {loc}:")
        print(result)

    print("\n📋 Database Snapshot:")
    advisor.print_all_data()

def get_crop_yield_prediction(input_data):
    """
    Simulate a crop yield prediction based on soil type, moisture, and location.
    In a real application, this would call an AI model or use some logic.
    """
    soil = input_data.get("soil_type", "Unknown")
    moisture = input_data.get("moisture", 0)
    location = input_data.get("location", "Unknown")

    # Basic mock logic
    if moisture > 50:
        yield_estimate = "High"
    elif 30 <= moisture <= 50:
        yield_estimate = "Medium"
    else:
        yield_estimate = "Low"

    return f"Predicted yield for {soil} soil at {location} with {moisture}% moisture is {yield_estimate}."
