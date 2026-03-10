import time
import logging

from utils.logging import setup_logging
from sources.adsbfi import fetch_adsbfi
from sources.opensky import fetch_opensky
from constants import SPECIAL_TARGETS

from core.tracker import check_profile
from core.history import cleanup, flight_history
from core.routing import estimate_route
from services.geocode import geocode
from services.discord import send_strategic_alert
from config import CFG

setup_logging()
logger = logging.getLogger(__name__)


def process_target(hex_code, plane):
    try:
        raw_alt = plane.get("alt", 0)
        alt = int(raw_alt) if str(raw_alt).isdigit() else 0
        hdg = int(plane.get("hdg") or plane.get("track") or 0)
    except (ValueError, TypeError):
        return

    is_deploying = check_profile(hex_code, alt, hdg)
    is_special = hex_code in SPECIAL_TARGETS

    current_time = time.time()
    last_vip_alert = flight_history.get(hex_code, {}).get("last_alert", 0)
    vip_cooldown_ok = (current_time - last_vip_alert) > CFG.alert_cooldown_sec

    if is_deploying or (is_special and vip_cooldown_ok):
        location = geocode(plane.get("lat"), plane.get("lon"))
        route = estimate_route(plane.get("lon"), hdg)

        callsign = str(plane.get("flight") or plane.get("callsign") or "N/A").strip()
        speed = plane.get("gs") or plane.get("speed") or "N/A"
        desc = plane.get("desc") or plane.get("t") or "Unknown Aircraft"

        if is_special:
            if hex_code not in flight_history:
                flight_history[hex_code] = {"time": current_time}
            flight_history[hex_code]["last_alert"] = current_time

        send_strategic_alert(
            callsign=callsign,
            hex_code=hex_code,
            full_desc=desc,
            location=location,
            route=route,
            alt=alt,
            speed=speed,
            heading=hdg,
            source=plane.get("source", "API"),
            is_priority=is_special
        )
        logger.info("Alert dispatched for %s (%s)", callsign, hex_code)


def main():
    logger.info("Tracker active. Polling every %d seconds", CFG.poll_interval_sec)

    while True:
        cleanup()

        planes = {}
        planes.update(fetch_adsbfi())
        planes.update(fetch_opensky())
        logger.info(f"Fetched {len(planes)} planes total")
        for hex_code, plane in planes.items():
            process_target(hex_code, plane)

        for hex_code, plane in planes.items():
            process_target(hex_code, plane)

        time.sleep(CFG.poll_interval_sec)


if __name__ == "__main__":
    main()