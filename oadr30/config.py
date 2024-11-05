#Universal Devices
#MIT License
import typing
from typing import Literal


class OADR3Config:

    '''
        Use oadr3_scale to scale up/down the durations. i.e. 
        Scale=1/5, changes the duration to duration /= 5
        scale=5, changes the duration to duration *= 5
        Mostly used for test purposes
    '''
    duration_scale:float=1.0

    '''
       If you want to mock up the start time so that the events start now, 
       set this True 
    '''
    events_start_now=False

    '''
       Relative Path to ven peristence file
    '''
    ven_persistence_file="ven.json"

    '''
       Relative Path to programs peristence file
    '''
    programs_persistence_file="programs.json"

class VTNRefImpl:
    ''' 
        Some static information for the RI
    '''
    base_url = "http://localhost:8026/openadr3/3.0.1"
    auth_url = "/auth/token"  
    client_id="ven_client"
    client_secret="999"


class OlivinePriceServer:
    #Multiday Highly Dynamic Signals
    #- Summer 
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SummerHDP_MD/OpenADR3
    #- Fall
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/FallHDP_MD/OpenADR3
    #- Winter 
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/WinterHDP_MD/OpenADR3
    #- Spring 
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SpringHDP_MD/OpenADR3

    #Hourly Highly Dynamic Signals
    #- Summer
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SummerHDP/OpenADR3
    #- Fall
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/FallHDP/OpenADR3
    #- Winter
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/WinterHDP/OpenADR3
    #- Spring
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SpringHDP/OpenADR3

    #Multiday GHG Signals
    #- Summer 
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SummerHDP_MDg/OpenADR3
    #- Fall
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/FallHDP_MDg/OpenADR3
    #- Winter 
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/WinterHDP_MDg/OpenADR3
    #- Spring 
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SpringHDP_MDg/OpenADR3
    
    #Hourly GHG Signals
    #- Summer
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SummerHDPg/OpenADR3
    #- Fall
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/FallHDPg/OpenADR3
    #- Winter
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/WinterHDPg/OpenADR3
    #- Spring
        # https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SpringHDPg/OpenADR3

    base_url="https://api.olivineinc.com/i/lbnl/v1/prices/cfh"
    suffix="OpenADR3"

    seasons={
        'summer':'SummerHDP',
        'fall':'FallHDP',
        'winter':'WinterHDP',
        'spring':'SpringHDP'
    }

    @staticmethod
    def getUrl(duration: Literal['multiday','hourly'], season: Literal['summer', 'fall', 'winter', 'spring'], signal_type: Literal['price','ghg']):
        resource=OlivinePriceServer.seasons[season]
        if duration == 'multiday':
            resource=resource+'_MD'

        if signal_type == 'ghg':
            resource=resource+'g'

        return f"{OlivinePriceServer.base_url}/{resource}/{OlivinePriceServer.suffix}"


