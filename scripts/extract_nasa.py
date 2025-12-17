import json
from pathlib import Path
from datetime import datetime
import requests

DATA_DIR=Path(__file__).resolve().parents[1] / "DATA"/"RAW"
DATA_DIR.mkdir(parents=True, exist_ok=True)

NASA_KEY="psseiwXHQenQfRswPrXmceFhmpYUW3umXMTgfu5h"

def extract_nasa_apod(api_key=NASA_KEY):
    url="https://api.nasa.gov/planetary/apod"
    params={
        "api_key": api_key
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    data = resp.json()

    filename = DATA_DIR / f"nasa_apod_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filename.write_text(json.dumps(data, indent=2)) 

    print (f"Extracted NASA APOD data saved to : {filename}")
    return data

if __name__ == "__main__":
    extract_nasa_apod()