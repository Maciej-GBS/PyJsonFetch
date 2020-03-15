import math

def _hav(a, b):
    return math.pow(math.sin(0.5 * (b - a)), 2.0)

class Geo:
    """
    Geographical location object\n
    R: Earth radius\n
    lat_degree/lon_degree: latitude, longtitude in degrees\n
    lat/lon: latitude, longtitude in radians
    """
    R = 6371000
    def __init__(self, lat, lon, degrees=True):
        if degrees:
            self.lat_degree = lat
            self.lon_degree = lon
        else:
            self.lat = lat
            self.lon = lon

    @property
    def lon_degree(self):
        return math.degrees(self._lon)
    @lon_degree.setter
    def lon_degree(self, v):
        self._lon = math.radians(v)
    @property
    def lon(self):
        return self._lon
    @lon.setter
    def lon(self, v):
        self._lon = v

    @property
    def lat_degree(self):
        return math.degrees(self._lat)
    @lat_degree.setter
    def lat_degree(self, v):
        self._lat = math.radians(v)
    @property
    def lat(self):
        return self._lat
    @lat.setter
    def lat(self, v):
        self._lat = v

    def distance(self, other):
        prod = math.cos(self.lat) * math.cos(other.lat) * _hav(self.lon, other.lon)
        sqrt = math.sqrt(_hav(self.lat, other.lat) + prod)
        return 2 * self.R * math.asin(sqrt)

    def __repr__(self):
        return str((round(self.lat_degree, 2), round(self.lon_degree, 2)))
