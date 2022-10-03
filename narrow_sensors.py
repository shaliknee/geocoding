# Shalini Bhakta ID: 74028480

# narrow_sensors.py
# Contains get_sensors function and all helper functions that narrow
# down sensors from PurpleAir database to the restrictions given (Range, Threshold, Max).

from api_classes import *
from file_classes import *
import math
from collections import namedtuple

AQIProp = namedtuple("AQIProp", "lower_pm upper_pm lower_aqi upper_aqi")


def get_sensors(center: LocalFwd or NomFwd, radius: int, threshold: int, maxx: int, aqi_data: LocalAQI or NomAQI) -> list:
    '''Narrows down all sensors to the given range and AQI threshold.'''
    valid_sensors = _invalidate_sensors(aqi_data)
    sensors_in_range = _get_sensors_in_range(center, radius, valid_sensors)
    threshold_sensors = _get_sensors_in_threshold(sensors_in_range, threshold)
    sensors = _max_sensors(threshold_sensors, maxx)
    return sensors


def _invalidate_sensors(aqi_data: LocalAQI or NomAQI) -> list:
    '''Returns a list of sensors with valid values in [1],[4],[25],[27],28].'''
    valid_sensors = []
    for sensor in aqi_data:
        if _check_age(sensor) or _check_type(sensor) or _check_else(sensor):
            pass
        else:
            valid_sensors.append(sensor)
    return valid_sensors


def _get_sensors_in_range(center: LocalFwd or NomFwd, radius: int, valid_sensors: list) -> list:
    '''Given sensors, return a list of sensors that are in the range of the radius given.'''
    sensors_in_range = []
    for sensor in valid_sensors:
        lat1, lon1 = center.fwd_geocode()
        lat1, lon1 = float(lat1), float(lon1)
        lat2, lon2 = sensor[27], sensor[28]
        dist = _calc_equirec(lat1, lon1, lat2, lon2)
        if dist <= radius:
            sensors_in_range.append(sensor)
    return sensors_in_range


def _get_sensors_in_threshold(sensors: list, threshold: int) -> list:
    '''Given sensors within a certain range, return a list of sensors
    whose AQI is at or above the threshold.'''
    threshold_sensors = []
    for sensor in sensors:
        aqi = _calc_aqi_value(sensor[1])
        if aqi >= threshold:
            sensor.append(aqi)
            threshold_sensors.append(sensor)
    return threshold_sensors


def _max_sensors(sensors: list, maxx: int) -> list:
    '''Return list of maxx sensors with the worst AQIs,
    ordered worst to best.'''
    reverse_order = sorted(sensors, key=lambda x: x[36], reverse=True)
    new = []
    if len(reverse_order) < maxx:
        return reverse_order
    else:
        for x in range(maxx):
            new.append(reverse_order[x])
        return new


def _calc_equirec(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    '''Calculate equirectangular approximation of distance between two coordinates.'''
    dlat = math.radians(abs(lat1 - lat2))
    dlon = math.radians(abs(lon1 - lon2))
    alat = math.radians((lat1 + lat2) / 2)
    x = dlon * math.cos(alat)
    distance = math.sqrt(math.pow(x, 2) + math.pow(dlat, 2)) * 3958.8
    return distance


def _calc_aqi_value(pm: int) -> int:
    '''Return AQI value given a pm.'''
    if pm >= 500.5:
        aqi = 501
    else:
        props = _get_aqi_range(pm)
        pm_range = props.upper_pm - props.lower_pm
        pm_as_aqi = pm - props.lower_pm
        aqi_range = props.upper_aqi - props.lower_aqi
        aqi = int(props.lower_aqi + (pm_as_aqi * (aqi_range) / pm_range) + 0.5)
    return aqi


def _get_aqi_range(pm: int) -> AQIProp:
    '''Get the PM and AQI Ranges for a given PM.'''
    if 0.0 <= pm < 12.1:
        proportions = AQIProp(0.0, 12.0, 0, 50)
    elif 12.1 <= pm < 35.5:
        proportions = AQIProp(12.1, 35.4, 51, 100)
    elif 35.5 <= pm < 55.5:
        proportions = AQIProp(35.5, 55.4, 101, 150)
    elif 55.5 <= pm < 150.5:
        proportions = AQIProp(55.5, 150.4, 151, 200)
    elif 150.5 <= pm < 250.5:
        proportions = AQIProp(150.5, 250.4, 201, 300)
    elif 250.5 <= pm < 350.5:
        proportions = AQIProp(250.5, 350.4, 301, 400)
    elif 350.5 <= pm < 500.5:
        proportions = AQIProp(350.5, 500.4, 401, 500)
    return proportions


def _check_age(sensor: list) ->  bool:
    '''Return True if sensor has not been updated int the last hour.'''
    if int(sensor[4]) > 3600 or sensor[4] == 'null':
        return True
    else:
        return False
        

def _check_type(sensor: list) -> bool:
    '''Return True if sensor type is Indoor.'''
    if int(sensor[25]) == 1 or sensor[25] == 'null':
        return True
    else:
        return False
        

def _check_else(sensor: list) -> bool:
    '''Return True is sensor does not have a pm, Latitude, or Longitude.'''
    if sensor[1] is None or sensor[27] is None or sensor[28] is None:
        return True
    else:
        return False
