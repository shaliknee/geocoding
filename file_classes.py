# Shalini Bhakta ID: 74028480

# file_classes.py
# All three classes that interact with locally stored files for PurpleAir's sensor
# data, including three classes to catch errors.

import json
from pathlib import Path

class FileNotExistError(Exception):
    '''Prints error message for if file
    given does not exist, then ends program.'''
    def __init__(self, file_path: str):
        print('FAILED')
        print(file_path)
        print('MISSING')
        raise SystemExit()

    
class FileFormatError(Exception):
    '''Prints error message for files with inorrect
    format, then ends program.'''
    def __init__(self, file_path: str):
        print('FAILED')
        print(file_path)
        print('FORMAT')
        raise SystemExit()


class LocalFwd:
    def __init__(self, file: str) -> None:
        '''Initializes this LocalFwd to have
        the content of the center json file given.'''
        self._data = self._download_data(file)


    def _download_data(self, file_path: str) -> dict:
        '''Download data from json file to dictionary.'''
        try:
            file = open(file_path)
            f = file.read()
            if f[0] == '[':
                string = f[1:-1]
            else:
                string = f

            try:
                json_text = string.encode(encoding = 'utf-8')
                return json.loads(json_text)
            except:
                raise FileFormatError(file_path)
            finally:
                file.close()
        except:
            raise FileNotExistError(file_path)


    def fwd_geocode(self) -> tuple:
        '''Forward Geocodes: Returns coordiantes in file.'''
        return self._data['lat'], self._data['lon']   
        

class LocalReverse:
    def __init__(self, file: str) -> None:
        '''Initializes this LocalReverse to have
        the content of the json files given.'''
        self._data = self._download_data(file)

    def _download_data(self, file_path: str) -> dict:
        '''Download data from json file to dictionary.'''
        try:
            file = open(file_path)
            f = file.read()
            if f[0] == '[':
                string = f[1:-1]
            else:
                string = f
                
            try:
                json_text = string.encode(encoding = 'utf-8')
                return json.loads(json_text)
            except:
                raise FileFormatError(file_path)
            finally:
                file.close()
        except:
            raise FileNotExistError(file_path)

    def rev_geocode(self) -> str:
        '''Reverse Geocodes: Returns location name in file.'''
        return self._data['display_name']
    

class LocalAQI:
    def __init__(self, file: str) -> None:
        '''Initializes this LocalAQI to have the content
        of the json file given as the PurpleAir database.'''
        self._data = self._download_data(file)

    def _download_data(self, file_path: str) -> dict:
        '''Downloads PurpleAir data from json file to dictionary.'''
        try:
            p = Path(file_path)
            file = p.open(encoding = 'utf-8')
            f = file.read()
            if f[0] == '[':
                string = f[1:-1]
            else:
                string = f
                
            try:
                json_text = string.encode(encoding = 'utf-8')
                return json.loads(json_text)
            except:
                raise FileFormatError(file_path)
            finally:
                file.close()
        except:
            raise FileNotExistError(file_path)

    def get_data(self) -> list:
        '''Returns list of sensors from PurpleAir AQI content.'''
        return self._data['data']


