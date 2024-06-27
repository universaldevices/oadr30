#Universal Devices
#MIT License
from .log import Oadr3LoggedException, oadr3_log_critical, oadr3_log_error
import requests
import json
from datetime import datetime, timedelta
from typing import Literal

OADR3_EVENT_BASE_URL = '/events'
OADR3_PROGRAM_BASE_URL = '/programs'
OADR3_AUTH_URL = '/auth/token'

class VTNOps():
    '''
        Uses this class to communicate with the VTN
    '''

    def __init__(self, base_url:str, client_id:str, client_secret:str, auth_url=OADR3_AUTH_URL, auth_token_url_is_json:bool=False):
        '''
            Make sure you provide the client_id and client_secret because they are needed for subsequent authorization operations.
            @auth_token_url_is_json - do not touch unless you want to be outside of RFC
        '''
        if base_url == None or client_id == None or client_secret == None: 
            raise Oadr3LoggedException('critical', "error: base_url is mandatory", True)

        self.base_url=base_url
        self.auth_url=self.base_url + auth_url
        self.client_id = client_id
        self.client_secret= client_secret
        self.token = None
        self.auth_token_url_is_json = auth_token_url_is_json


    def __refresh_token__(self)->bool:

        # Set headers to specify JSON content type
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        # Set the body
        postBody = f"client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials&scope=read_all"
        if self.auth_token_url_is_json:
            # Set headers to specify JSON content type
            headers = { "Content-Type": "application/json" }
            # Set the body
            postBody = {'clientID': self.client_id, 'clientSecret': self.client_secret, 'grant_type': 'client_credentials', 'scope': 'read_all'}
            # Convert the dictionary to a JSON string
            postBody = json.dumps(postBody)

        try:
            response = requests.post(self.auth_url, data=postBody, headers=headers)
            if response == None:
                return False
            if response.status_code != 200:
                oadr3_log_error(f'failed getting authentication token - status = {response.status_code}')
                self.token = None
                return False

            self.token = response.json()
            self.token['received'] = datetime.now()
            return True
        except Exception as ex:
            oadr3_log_critical(f"failed processing auth request")
            self.token == None
            return False

    def __has_token_expired__(self):
        if self.token == None:
            return True
        if not 'expires_in' in self.token:
            return False
        try:
            # Calculate the expiration time
            expire_time = self.token['received'] + (timedelta(seconds=self.token['expires_in']) - timedelta(seconds=10))
    
            # Compare the current time with the expiration time
            return datetime.now() >= expire_time 
        except Exception as ex:
            oadr3_log_error("failed calculating token expiration time", True)

    def __get_token__(self):
        '''
            returns the token if we already have one or asks for one if we don't
        '''
        if self.__has_token_expired__():
            self.__refresh_token__()
        return self.token

    def __get_default_headers(self):
        if self.__get_token__() == None:
            return None
        access_token = self.token['access_token']
        return {'accept': 'application/json', 'Authorization': f'Bearer {access_token}'}

    def __send_request__(self, method:Literal['POST', 'PUT', 'GET', 'DELETE'], url:str, body:str):
        if url == None or method == None:
            oadr3_log_error("url and method are mandatory ....", False)
            return None

        if (method == 'POST' or method == 'PUT') and body == None:
            oadr3_log_error("for post and put, body is mandatory ....", False)
            return None

        headers = self.__get_default_headers()
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
                oadr3_log_error(f"failed executing {method} on {url}....", False)

            return response
        except Exception as ex:
            oadr3_log_critical(f"failed sending {method} request to {url} ....")
            return None
        
    def get_programs(self):
        '''
            returns all programs 
        '''
        return None

    def get_program(self, program_id:str):
        '''
            returns a specific program
        '''

    def get_events(self, program_id:str):
        '''
            returns all events for the given program_id
        '''

