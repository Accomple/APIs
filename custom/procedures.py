
def merge(serialized_data, post_data):
    merged_data = post_data.copy()
    for key in serialized_data:
        if merged_data.get(key) is None:
            merged_data[key] = serialized_data[key]
    return merged_data

'''
function haversine_distance(x1,y1,x2,y2) {
      var R = 6371.0710; // Radius of the Earth in miles
      var rlat1 = x1 * (Math.PI/180); // Convert degrees to radians
      var rlat2 = x2 * (Math.PI/180); // Convert degrees to radians
      var difflat = rlat2-rlat1; // Radian difference (latitudes)
      var difflon = (y2-y1) * (Math.PI/180); // Radian difference (longitudes)

      var d = 2 * R * Math.asin(Math.sqrt(Math.sin(difflat/2)*Math.sin(difflat/2)+Math.cos(rlat1)*Math.cos(rlat2)*Math.sin(difflon/2)*Math.sin(difflon/2)));
      return d;
    }
'''