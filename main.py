import os
import time
import logging
from dotenv import load_dotenv
from supabase import create_client
import requests

from utils.logging import setup_logging
from sources.adsbfi import fetch_adsbfi
from sources.opensky import fetch_opensky
from sources.flightradar import fetch_flightradar
from constants import SPECIAL_TARGETS
from constants import MIL_TANKER, MIL_COMBAT, MIL_ISR, MIL_VIP, MIL_UAV, MIL_HELO

from core.tracker import check_profile
from core.history import cleanup, flight_history
from core.routing import estimate_route
from services.geocode import geocode
from services.discord import send_strategic_alert
from config import CFG

setup_logging()
logger = logging.getLogger(__name__)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_mil_category(type_code):
    t = str(type_code).upper()
    if t in MIL_TANKER: return "tanker"
    if t in MIL_COMBAT: return "combat"
    if t in MIL_ISR: return "isr"
    if t in MIL_VIP: return "vip"
    if t in MIL_UAV: return "uav"
    if t in MIL_HELO: return "helicopter"
    return "transport"


def process_target(hex_code, plane):
    try:
        def safe_int(val, default=0):
            if val is None: return default
            if str(val).lower() == "ground": return 0
            try:
                return int(val)
            except (ValueError, TypeError):
                return default

        alt = safe_int(plane.get("alt"))
        hdg = safe_int(plane.get("hdg") or plane.get("track"))
        speed = safe_int(plane.get("speed") or plane.get("gspeed") or plane.get("gs"))
        v_speed = safe_int(plane.get("v_speed") or plane.get("vspeed") or plane.get("baro_rate"))

        lat = plane.get("lat")
        lon = plane.get("lon")

        callsign = str(plane.get("flight") or plane.get("callsign") or "N/A").strip()
        desc = str(plane.get("type") or "Unknown")
        reg = str(plane.get("reg") or "N/A")
        ownOp = str(plane.get("operator") or plane.get("ownOp") or "Military")
        squawk = str(plane.get("squawk") or "0000")
        source = str(plane.get("source") or "API")

        cat = get_mil_category(desc)
        location = f"{lat}, {lon}"
        emergency = "HIGH" if squawk in ["7700", "7600", "7500"] else "none"

    except Exception as e:
        logger.error(f"Error parsing plane data for {hex_code}: {e}")
        return

    db_data = {
        "hex_code": hex_code,
        "callsign": callsign,
        "lat": lat,
        "lon": lon,
        "alt": alt,
        "hdg": hdg,
        "speed": speed,
        "type": desc,
        "v_speed": v_speed,
        "operator": ownOp,
        "category": cat,
        "source": source
    }

    if lat is not None and lon is not None:
        try:
            supabase.table("sightings").insert(db_data).execute()
        except Exception as e:
            logger.error(f"DB Error for {hex_code}: {e}")

    profile_score = check_profile(hex_code, alt, hdg, lat, lon, plane)

    if profile_score:
        send_strategic_alert(
            callsign=callsign,
            hex_code=hex_code,
            full_desc=desc,
            location=location,
            alt=alt,
            speed=speed,
            heading=hdg,
            source=source,
            priority_tag="STANDARD",
            reg=reg,
            ownOp=ownOp,
            squawk=squawk,
            v_speed=v_speed,
            emergency=emergency,
            category=cat
        )
        logger.info(f"Sent alert for {callsign} ({hex_code})")


def main():
    logger.info("Tracker active. Polling every %d seconds", CFG.poll_interval_sec)

    while True:
        cleanup()

        adsbfi_planes = fetch_adsbfi()
        opensky_planes = fetch_opensky()
        fr24_planes = fetch_flightradar()

        planes = adsbfi_planes.copy()

        for hex_code, plane in opensky_planes.items():
            if hex_code not in planes:
                planes[hex_code] = plane
            elif planes[hex_code].get("lat") is None and plane.get("lat") is not None:
                planes[hex_code].update({
                    "lat": plane["lat"],
                    "lon": plane["lon"],
                    "source": planes[hex_code].get("source", "") + "+OpenSky"
                })

        for hex_code, plane in fr24_planes.items():
            if hex_code not in planes:
                planes[hex_code] = plane
            elif planes[hex_code].get("lat") is None and plane.get("lat") is not None:
                planes[hex_code].update({
                    "lat": plane["lat"],
                    "lon": plane["lon"],
                    "alt": planes[hex_code].get("alt") or plane.get("alt"),
                    "hdg": planes[hex_code].get("hdg") or plane.get("hdg"),
                    "source": planes[hex_code].get("source", "") + "+FR24"
                })

        logger.info(f"Fetched {len(planes)} planes total")
        for hex_code, plane in planes.items():
            process_target(hex_code, plane)

        time.sleep(CFG.poll_interval_sec)


if __name__ == "__main__":
    main()