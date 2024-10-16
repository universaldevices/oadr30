
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
from oadr30.config import OADR3Config, OlivinePriceServer
from oadr30.scheduler import EventScheduler
from oadr30.values_map import ValuesMap
import json


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
        OADR3Config.events_start_now=True

        client= PriceServerClient(OlivinePriceServer.getUrl('hourly', 'fall', 'price'))
        events= client.getEvents()
        timeSeries = events.getTimeSeries()
        scheduler=EventScheduler(timeSeries, scheduler_callback)
        scheduler.start()
        scheduler.join()
    except Exception as ex:
        oadr3_log_critical("main failed")





if __name__ == "__main__":
    main()