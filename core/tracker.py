import time
from core.history import flight_history
from config import CFG

def check_profile(hex_code, alt, hdg):
    now = time.time()

    if CFG.training_mode:
        return True

    if hex_code not in flight_history:
        flight_history[hex_code] = {
            "alt": alt,
            "hdg": hdg,
            "time": now,
            "last_alert": 0
        }

        return False

    prev = flight_history[hex_code]

    if alt < CFG.min_alt_normal_ft:
        return False

    if not (CFG.hdg_min <= hdg <= CFG.hdg_max):
        return False

    if now - prev.get("last_alert", 0) > CFG.alert_cooldown_sec:
        prev["last_alert"] = now
        return True

    return False