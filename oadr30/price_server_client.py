#Universal Devices
#MIT License
#Use this class to communicate with a price server that only sends 3.0 payloads

from .log import Oadr3LoggedException, oadr3_log_critical, oadr3_log_error
from .programs import Programs, Program
from .events import Events, Event
from .ven import VEN
from .config import OADR3Config 
import requests
import json
from datetime import datetime, timedelta
from typing import Literal

class PriceServerClient():
    '''
        Uses this class to communicate with the VTN that only sends payloads but does not follow any other OADR3 convention
    '''

    def __init__(self, base_url:str):
        '''
            Just the URL
        '''
        if base_url == None : 
            raise Oadr3LoggedException('critical', "error: base_url is mandatory", True)

        self.base_url=base_url

    def __get_default_headers(self, method:str):

        headers = {'accept': 'application/json'}
        if method == 'POST' or method == 'PUT':
            headers['Content-Type'] = 'application/json'

        return headers

    def __send_request__(self, method:Literal['POST', 'PUT', 'GET', 'DELETE'], url:str, body:str=None):
        if url == None or method == None:
            oadr3_log_error("url and method are mandatory ....", False)
            return None

        if (method == 'POST' or method == 'PUT') and body == None:
            oadr3_log_error("for post and put, body is mandatory ....", False)
            return None

        headers = self.__get_default_headers(method)
        if headers == None:
            oadr3_log_error("failed getting headers ....", False)
            return None

        try:
            response = None
            if method == 'POST':
                response = requests.post(url, data=body, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, data=body, headers=headers)
            elif method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers) 
            else:
                oadr3_log_error(f"invalid method {method}....", False)
                return None

            if response == None or response.status_code != 200:
                oadr3_log_error(f"[status code = {response.status_code} : failed executing {method} on {url},  {response.json()}....", False)

            return response
        except Exception as ex:
            oadr3_log_critical(f"failed sending {method} request to {url} ....")
            return None

    def getEvents(self):
        '''
            returns all events for the given program_id
        '''
        try:
            response = self.__send_request__('GET', self.base_url) 
            if response.status_code != 200:
                oadr3_log_error(f"failed getting events ...")
                return None
            events = Events(response.json())
            return events
        except Exception as ex:
            oadr3_log_critical(f"failed getting events ....")
            return None





