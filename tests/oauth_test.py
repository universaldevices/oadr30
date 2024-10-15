
#POST https://authorization-server.com/token
#client_id	    j3CziWgbG1xyvWBcfGAiGris
#client_secret	AcOWNGc7x1SPfjH-ZhLlJVSqA-xP_gGHkPfIDU5Wdo7yQhxg
#User Account
#https://oauth.com
#login	    kind-quoll@example.com
#password	Quaint-Curlew-99

from oadr30.vtn import VTNOps
from oadr30.log import oadr3_log_critical
from oadr30.price_server_client import PriceServerClient
from oadr30.config import OADR3Config 
from oadr30.scheduler import EventScheduler
from oadr30.values_map import ValuesMap
import json


#isyp_base_url = "https://dev.isy.io"
#isyp_auth_url = "/o2/token"  
#isyp_client_id="isyportal-o2-unsubscribe"
#isyp_client_secret="testsecret" 

base_url = "http://localhost:8026/openadr3/3.0.1"
auth_url = "/auth/token"  
client_id="ven_client"
client_secret="999"

def scheduler_callback(segment:ValuesMap):
    print (segment)

def main():
    try:
#        vtn = VTNOps(base_url=base_url, auth_url=auth_url, client_id=client_id, client_secret=client_secret, auth_token_url_is_json=True )
#        vtn.create_ven("crap")
#        vtn.get_programs()
#        vtn.get_program('0')
#        events = vtn.get_events()
        OADR3Config.duration_scale=1/360

        client= PriceServerClient('https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SummerHDP_MD/OpenADR3')
        events= client.getEvents()
        timeSeries = events.getTimeSeries()
        scheduler=EventScheduler(timeSeries, scheduler_callback)
        scheduler.start()
        scheduler.join()
    except Exception as ex:
        oadr3_log_critical("main failed")





if __name__ == "__main__":
    main()