import sqlite3

def initialize_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create soil data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS soil_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_type TEXT,
            moisture REAL,
            ph REAL,
            crop_type TEXT,
            timestamp TEXT,
            location TEXT
        );
    """)

    # Create weather forecast table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            rainfall REAL,
            timestamp TEXT,
            location TEXT
        );
    """)

    # Create crop recommendations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crop_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            crops TEXT,
            location TEXT
        );
    """)

    # Create ollama_predictions table (fix column name to 'prediction')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ollama_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farm_input_id INTEGER,
            prediction TEXT,
            timestamp TEXT
        );
    """)

    conn.commit()
    conn.close()