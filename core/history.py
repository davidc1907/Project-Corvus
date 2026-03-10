import time
from config import CFG

flight_history = {}

def cleanup():

    now = time.time()

    stale = [
        k for k,v in flight_history.items()
        if now - v["time"] > CFG.history_ttl_sec
    ]

    for k in stale:
        del flight_history[k]