import requests


def fetch_adsbfi():
    planes = {}
    try:
        r = requests.get("https://opendata.adsb.fi/api/v2/mil", timeout=10)
        if r.status_code != 200:
            return planes

        data = r.json().get("ac", [])
        for ac in data:
            raw_hex = ac.get("hex")
            if not raw_hex:
                continue

            hex_code = raw_hex.lower()
            planes[hex_code] = {
                "hex": hex_code,
                "lat": ac.get("lat"),
                "lon": ac.get("lon"),
                "alt": ac.get("alt_baro"),
                "hdg": ac.get("track"),
                "type": ac.get("t"),
                "reg": ac.get("r"),
                "v_speed": ac.get("baro_rate"),
                "squawk": ac.get("squawk"),
                "flight": str(ac.get("flight", "")).strip(),
                "operator": ac.get("ownOp"),
                "speed": ac.get("gs"),
                "source": "adsb.fi"
            }
    except Exception:
        pass
    return planes