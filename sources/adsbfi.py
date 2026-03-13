import requests
from constants import TARGET_TYPES

def fetch_adsbfi():

    planes = {}

    r = requests.get("https://opendata.adsb.fi/api/v2/mil", timeout=10)

    for ac in r.json().get("ac", []):

        hex_code = ac.get("hex")

        planes[hex_code] = {
            "alt": ac.get("alt_baro"),
            "hdg": ac.get("track"),
            "lat": ac.get("lat"),
            "lon": ac.get("lon"),
            "type": ac.get("t"),
            "desc": ac.get("desc"),
            "squawk": ac.get("squawk"),
            "ownOp": ac.get("ownOp"),
            "reg": ac.get("r"),
            "v_speed": ac.get("baro_rate"),
            "emergency": ac.get("emergency"),
            "category": ac.get("category"),
            "flight": ac.get("flight"),
            "gs": ac.get("gs"),
            "source": "adsb.fi"
        }

    return planes