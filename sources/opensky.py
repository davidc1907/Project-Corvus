from opensky_api import OpenSkyApi
from constants import KNOWN_ICAO_HEX
from config import CFG

api = OpenSkyApi(CFG.opensky_user, CFG.opensky_pass)

def fetch_opensky():

    planes = {}

    states = api.get_states(bbox=CFG.bbox_atlantic)

    if not states:
        return planes

    for s in states.states:

        if s.icao24 not in KNOWN_ICAO_HEX:
            continue

        planes[s.icao24] = {
            "alt": s.baro_altitude * 3.28084,
            "hdg": s.true_track,
            "lat": s.latitude,
            "lon": s.longitude,
            "flight": s.callsign,
            "source": "opensky"
        }

    return planes