import time
from core.history import flight_history
from config import CFG

def check_profile(hex_code, alt, hdg):

    now = time.time()

    if alt == "ground" or alt is None or hdg is None:
        return False

    if hex_code not in flight_history:

        flight_history[hex_code] = {
            "alt": alt,
            "hdg": hdg,
            "time": now,
            "last_alert": 0
        }

        return False

    prev = flight_history[hex_code]

    min_alt = CFG.min_alt_training_ft if CFG.training_mode else CFG.min_alt_normal_ft

    if alt < min_alt:
        return False

    if not CFG.training_mode:
        if not (CFG.hdg_min <= hdg <= CFG.hdg_max):
            return False

    if not (CFG.hdg_min <= hdg <= CFG.hdg_max):
        return False

    if now - prev["last_alert"] > CFG.alert_cooldown_sec:
        prev["last_alert"] = now
        return True

    return False