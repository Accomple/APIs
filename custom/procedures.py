
def merge(serialized_data, post_data):
    merged_data = post_data.copy()
    for key in serialized_data:
        if merged_data.get(key) is None:
            merged_data[key] = serialized_data[key]
    return merged_data
