#TODO colocar como dependencia geocoder
import geocoder

class Geolocator:
    def __init__(self):
        self.geoloc = geocoder.ipinfo()

    def get_current_location(self):

        location = self.geoloc.latlng

        if location:
            latitude, longitude = location
            return tuple([latitude, longitude])
        else:
            print('Unable to retrieve location information.')