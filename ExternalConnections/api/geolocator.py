#TODO colocar como dependencia geocoder
import geocoder
from geopy.geocoders import Nominatim

class Geolocator:

    @staticmethod
    def get_coordinates():

        location = geocoder.ipinfo().latlng

        if location:
            latitude, longitude = location
            return tuple([latitude, longitude])
        else:
            print('Unable to retrieve location information.')

    @staticmethod
    def get_current_location():
        tuple = Geolocator.get_coordinates()
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse((tuple[0], tuple[1]), exactly_one=True)
            address = location.raw['address']
            city = address.get('city', '')
            if not city:  # sometimes city is not available then try some other keys
                city = address.get('town', '')
            if not city:
                city = address.get('village', '')
            return city
        except Exception as e:
            print(f"Error: {e}")
            return None
        
if __name__ == '__main__':
    print(Geolocator.get_current_location())
