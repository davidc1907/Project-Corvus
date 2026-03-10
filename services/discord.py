import requests
import logging
from config import CFG

logger = logging.getLogger(__name__)

def send_discord_alert(message: str):
    if not CFG.webhook_url:
        logger.warning("Webhook not configured")
        return

    try:
        r = requests.post(CFG.webhook_url, json={"content": message}, timeout=5)
        r.raise_for_status()
    except Exception as e:
        logger.error("Discord alert failed: %s", e)