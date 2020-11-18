import math


def merge(serialized_data, post_data):
    merged_data = post_data.copy()
    for key in serialized_data:
        if merged_data.get(key) is None:
            merged_data[key] = serialized_data[key]
    return merged_data


def haversine_distance(lat1, long1, lat2, long2):
    r = 6371.0710  # radius of earth in km
    rad_lat1 = lat1 * math.pi / 180
    rad_lat2 = lat2 * math.pi / 180
    lat_diff = rad_lat2 - rad_lat1
    long_diff = (long2 - long1) * math.pi / 180
    distance = 2 * r * math.asin(
        math.sqrt(
            math.sin(lat_diff / 2) * math.sin(lat_diff / 2) +
            math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(long_diff / 2) * math.sin(long_diff / 2)
        )
    )
    return distance


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def to_coordinates(value):
    if len(value.split(",")) != 2:
        return None
    lat = value.split(",")[0]
    long = value.split(",")[-1]
    if not is_float(long) or not is_float(lat):
        return None
    lat = float(lat)
    long = float(long)

    if (-180 <= long <= 180) and (-90 <= lat <= 90):
        return lat, long
    else:
        return None