# Shalini Bhakta ID: 74028480

# project3.py
# Project #3: Try Not to Breathe
# # ICS 32 Winter 2022
# Contains main module to run program. Takes inputs, creates
# three of six possible objects from classes for either file or API data
# and prints sensors that fit the input restrictions.

from api_classes import *
from file_classes import *
import narrow_sensors

def print_coordinates(lat: str, lon: str) -> None:
    '''Puts coordinates in printable format with cardinal directions.'''
    lat, lon = float(lat), float(lon)

    if lat >= 0:
        lat = str(lat) + '/N'
    else:
        lat = str(abs(lat)) + '/S'

    if lon >= 0:
        lon = str(lon) + '/E'
    else:
        lon = str(abs(lon)) + '/W'
        
    print(f'{lat} {lon}')
    

def _local_or_api(inp: str) -> bool:
    '''Returns True if the input asks for local files to be used.
    Returns False if input asks for API.'''
    command = inp.split()
    if command[1] == 'FILE' or command[1] == 'FILES':
        return True
    else:
        return False

def create_center_object(center: str) -> LocalFwd or NomFwd:
    '''Creates object LocalFwd or NomFwd for forward geocoding center location.'''
    if _local_or_api(center):
        c = center.split('FILE ')
        center = LocalFwd(c[1])
    else:
        c = center.split('NOMINATIM ')
        center = NomFwd(c[1])
    return center


def create_aqi_data_object(aqi_data: str) -> LocalAQI or NomAQI:
    '''Creates object LocalAQI or NomAQI for PurpleAir data.'''
    if _local_or_api(aqi_data):
        a = aqi_data.split('FILE ')
        aqi_data = LocalAQI(a[1])
    else:
        aqi_data = NomAQI()
    return aqi_data


def create_reverse_items(reverse: str, sensors: list) -> LocalReverse or NomReverse:
    '''Creates object LocalReverse or NomReverse for reverse geocoding.'''
    reverse_items = []
    if _local_or_api(reverse):
        r = reverse.split()
        for item in r[2:]:
            reverse_items.append(LocalReverse(item))
    else:
        for sensor in sensors:
            reverse_items.append(NomReverse(sensor[27], sensor[28]))
    return reverse_items
        
    
def run() -> None:
    '''Takes 6 inputs and runs program.'''
    center = input()
    radius = int(input()[6:])
    threshold = int(input()[9:])
    maxx = int(input()[4:]) 
    aqi_data = input()
    reverse = input()

    center = create_center_object(center)
    aqi_data = create_aqi_data_object(aqi_data)
    sensors = narrow_sensors.get_sensors(
        center, radius, threshold, maxx, aqi_data.get_data())
    reverse_items = create_reverse_items(reverse, sensors)

    lat, lon = center.fwd_geocode()
    print('CENTER ', end='')
    print_coordinates(lat, lon)
    index = 0
    for sensor in sensors:
        print(f'AQI {sensor[36]}')
        print_coordinates(sensor[27], sensor[28])
        print(reverse_items[index].rev_geocode())
        index += 1


if __name__ == '__main__':
    run()
