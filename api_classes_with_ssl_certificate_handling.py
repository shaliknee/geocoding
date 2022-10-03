# Shalini Bhakta ID: 74028480

# api_classes.py
# All three classes that interact with Nominatim API for PurpleAir's sensor data,
# including three classes to catch errors.
# INCLUDES HANDLING FOR SSL CERTIFICATE ERROR

import urllib.parse
import urllib.request
import json
import time
import ssl #####

BASE_NOMINATIM_URL = 'https://nominatim.openstreetmap.org/'

class StatusCodeError(Exception):
    def __init__(self, status_code: int, url: str):
        '''Prints error message for status codes that are not 200,
        then ends program.'''
        print('FAILED')
        print(status_code, url)
        print('NOT 200')
        raise SystemExit()


class FormatError(Exception):
    def __init__(self, status_code: int, url: str):
        '''Prints error message for HTTP response with
        non-json format, then ends program.'''
        print('FAILED')
        print(status_code, url)
        print('FORMAT')
        raise SystemExit()
    

class NetworkError(Exception):
    def __init__(self, url: str):
        '''Prints error message for HTTP requests that
        could not be made, then ends program.'''
        print('FAILED')
        print(url)
        print('NETWORK')
        raise SystemExit()
    

class NomFwd: 
    def __init__(self, location_query: str) -> None:
        '''Initializes this NomFwd to have the location
        of the given location query and the API data of
        the given location.'''
        self._location = location_query
        self._data = self._download_data(location_query)
        time.sleep(1)

    def _download_data(self, location_query: str) -> dict:
        '''Open NOMINATIM SEARCH URL to location_query and
        return downloaded json formatted content in dictionary
        form. Return specified error messages if API request is
        not successful.'''
        
        ########
        cntx = ssl.create_default_context()
        cntx.check_hostname = False
        cntx.verify_mode = ssl.CERT_NONE
        ########
        
        url = self._build_search_url()
        headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/shalinjb'}
        try:
            request = urllib.request.Request(url, headers=headers)
        except:
            raise NetworkError(url)

        try:
            response = urllib.request.urlopen(request, context=cntx) ##########
        except urllib.error.HTTPError as k:
            status = k.code
            raise StatusCodeError(status, url)

        try:
            json_text = response.read().decode(encoding = 'utf-8')
            x = json.loads(json_text)
            if type(x[0]) == dict:
                x = x[0]
            return x
        except:
            raise FormatError(response.status, url)
        finally:
            response.close()
        
    def _build_search_url(self) -> str:
        '''Build search URL to Nominatim API.'''
        query_parameters = [('q', self._location), ('format', 'json')]
        encoded_parameters = urllib.parse.urlencode(query_parameters)
        
        return f'{BASE_NOMINATIM_URL}search?{encoded_parameters}'
    
    def fwd_geocode(self) -> tuple:
        '''Return coordinates of location_query.'''
        return self._data['lat'], self._data['lon']


class NomReverse:
    def __init__(self, lat: str, lon: str) -> None:
        '''Initializes this NomReverse to have the latitude
        and longitude of the given coordinates, and the API data
        based on the coordinates.'''
        self._lat = lat
        self._lon = lon
        self._data = self._download_data()
        time.sleep(1)
        
    def _download_data(self) -> dict:
        '''Open NOMINATIM REVERSE URL to location_query and return downloaded
        json formatted content in dictionary form. Return specified error
        messages if API request is not successful.'''

        #########
        cntx = ssl.create_default_context()
        cntx.check_hostname = False
        cntx.verify_mode = ssl.CERT_NONE
        ##########
        
        url = self._build_search_url()
        headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/shalinjb'}
        try:
            request = urllib.request.Request(url, headers=headers)
        except:
            raise NetworkError(url)
        
        try:
            response = urllib.request.urlopen(request, context=cntx) ########## REMOVE context=cntx
        except urllib.error.HTTPError as k:
            status = k.code
            raise StatusCodeError(status, url)
        
        try:
            json_text = response.read().decode(encoding = 'utf-8')
            x = json.loads(json_text)
            if type(x) == list:
                x = x[0]
            return x
        except:
            raise FormatError(response.status, url)
        finally:
            response.close()

    def _build_search_url(self) -> str:
        '''Build (reverse) search URL to Nominatim API.'''
        query_parameters = [('lat', self._lat), ('lon', self._lon), ('format', 'json')]
        encoded_parameters = urllib.parse.urlencode(query_parameters)
        
        return f'{BASE_NOMINATIM_URL}reverse?{encoded_parameters}'

    def rev_geocode(self) -> str:
        '''Reverse Geocodes: Returns location name of coordinates given.'''
        return self._data['display_name']


class NomAQI:
    def __init__(self) -> None:
         '''Initializes this NomAQI to have the
         API data of PurpleAir's sensor database.'''
         self._data = self._download_data()
         time.sleep(1)
        
    def _download_data(self) -> dict:
        '''Downloads PurpleAir data from Nominatim's experimental API.'''
        
        ########
        cntx = ssl.create_default_context()
        cntx.check_hostname = False
        cntx.verify_mode = ssl.CERT_NONE
        ########
        
        url = 'https://www.purpleair.com/data.json'
        headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/shalinjb'}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request, context=cntx) ##########

        try:
            json_text = response.read().decode(encoding = 'utf-8')
            return json.loads(json_text)
        finally:
            response.close()

    def get_data(self) -> list:
        '''Return list of sensors from PurpleAir database.'''
        return self._data['data']
    
