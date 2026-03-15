import requests
import logging
from constants import TARGET_TYPES
from dotenv import load_dotenv
import os

load_dotenv()


API_TOKEN = os.getenv("FR24_TOKEN")

logger = logging.getLogger(__name__)


def fetch_flightradar():
    planes = {}
    url = "https://fr24api.flightradar24.com/api/live/flight-positions/full"

    headers = {
        "Accept": "application/json",
        "Accept-Version": "v1",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    params = {
        "aircraft": ",".join(TARGET_TYPES)
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 402:
            logger.error("Credit limit reached! Check your FR24 Dashboard.")
            return planes

        response.raise_for_status()
        data = response.json()

        flights = data.get("data", [])

        for f in flights:
            raw_hex = f.get("hex")
            if not raw_hex or not isinstance(raw_hex, str):
                continue
            hex_code = raw_hex.lower()
            if not hex_code:
                continue

            planes[hex_code] = {
                "alt": f.get("alt", 0),
                "hdg": f.get("track", 0),
                "lat": f.get("lat"),
                "lon": f.get("lon"),
                "flight": f.get("callsign") or f.get("flight") or "N/A",
                "type": f.get("type", "Unknown"),
                "reg": f.get("reg", "N/A"),
                "speed": f.get("gspeed", 0),
                "v_speed": f.get("vspeed", 0),
                "squawk": f.get("squawk", "0000"),
                "orig": f.get("orig_icao", "???"),
                "dest": f.get("dest_icao", "???"),
                "operator": f.get("operating_as") or f.get("painted_as") or "Military",
                "source": f.get("source", "ADSB")
            }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching official FR24 API: {e}")

    return planes