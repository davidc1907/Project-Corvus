import requests
import logging
from config import CFG

logger = logging.getLogger(__name__)


def send_strategic_alert(callsign, hex_code, full_desc, location, route, alt, speed, heading, source,
                         is_priority=False):
    if not CFG.webhook_url:
        logger.warning("Discord Webhook URL is missing in config")
        return

    prefix = "⭐ **PRIORITY ALERT: VIP TARGET** ⭐" if is_priority else "🚨 **STRATEGIC ALERT** 🚨"
    map_link = f"https://globe.adsb.fi/?icao={hex_code}"

    message = (
        f"{prefix}\n"
        f"**Callsign:** {callsign}\n"
        f"**Type:** {full_desc} (Hex: {hex_code})\n"
        f"**Location:** 🗺️ {location}\n"
        f"**Route:** {route}\n"
        f"**Altitude:** `{alt} ft`\n"
        f"**Speed:** `{speed} kts`\n"
        f"**Heading:** `{heading}°`\n"
        f"**Source:** *{source}*\n"
        f"🌍 **Live Map:** {map_link}"
    )

    try:
        payload = {"content": message}
        response = requests.post(CFG.webhook_url, json=payload, timeout=5)
        response.raise_for_status()
    except Exception as e:
        logger.error("Failed to send Discord alert for %s: %s", hex_code, e)