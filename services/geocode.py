import reverse_geocode


def geocode(lat, lon):
    if lat is None or lon is None:
        return "Unknown Location"

    coordinates = (lat, lon)

    try:
        geo_result = reverse_geocode.get(coordinates)

        if geo_result:
            return geo_result.get('country', 'Unknown')

    except Exception as e:
        print(f"Error in geocode: {e}")

    return "Unknown Location"