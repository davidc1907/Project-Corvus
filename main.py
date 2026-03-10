import time
import logging
from sys import prefix

from utils.logging import setup_logging
from sources.adsbfi import fetch_adsbfi
from services.geocode import geocode
from sources.opensky import fetch_opensky
from constants import SPECIAL_TARGETS

from core.tracker import check_profile
from core.history import cleanup, flight_history
from core.routing import estimate_route

from services.discord import send_discord_alert

from config import CFG

setup_logging()

logger = logging.getLogger(__name__)

def main():

    logger.info("Tracker started Polling every %d seconds", CFG.poll_interval_sec)

    while True:

        cleanup()

        planes = {}
        planes.update(fetch_adsbfi())
        planes.update(fetch_opensky())

        for hex_code, plane in planes.items():

            is_deploying = check_profile(hex_code, plane["alt"], plane["hdg"])

            is_special = hex_code in SPECIAL_TARGETS
            current_time = time.time()
            current_time = time.time()
            last_vip_alert = flight_history.get(hex_code, {}).get("last_alert", 0)
            vip_cooldown_ok = (current_time - last_vip_alert) > CFG.alert_cooldown_sec

            if is_deploying or (is_special and vip_cooldown_ok):
                route_info = estimate_route(plane.get("lon"), plane.get("hdg"))
                location_info = geocode(plane.get("lat"), plane.get("lon"))
                flight_raw = plane.get("flight") or "N/A"
                callsign = str(flight_raw).strip() or "N/A"
                full_desc = plane.get("desc", plane.get("type", "Unknown Type"))
                map_link = f"https://globe.adsb.fi/?icao={hex_code}"

                if is_special:

                    if hex_code not in flight_history:
                        flight_history[hex_code] = {"time": current_time}
                    flight_history[hex_code]["last_alert"] = current_time
                    prefix = f"⭐ **PRIORITY ALERT: {SPECIAL_TARGETS[hex_code]}** ⭐"

                else:
                    prefix = "🚨 **STRATEGIC ALERT** 🚨"

                msg = (
                    f"{prefix}\n"
                    f"**Callsign:** `{callsign}`\n"
                    f"**Type:** {full_desc} (Hex: `{hex_code}`)\n"
                    f"**Location:** 🗺️ {location_info}\n"
                    f"**Route:** {route_info}\n"
                    f"**Altitude:** `{int(plane['alt'])} ft`\n"
                    f"**Source:** *{plane['source']}*\n"
                    f"🌍 **Live Map:** {map_link}"
                )

                logger.info("Sending Discord Alert: %s", hex_code)
                send_discord_alert(msg)

        time.sleep(CFG.poll_interval_sec)


if __name__ == "__main__":
    main()