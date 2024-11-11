from oadr30.vtn import VTNOps
from oadr30.log import oadr3_log_critical
from oadr30.price_server_client import PriceServerClient
from oadr30.config import OADR3Config, OlivinePriceServer, VTNRefImpl
from oadr30.scheduler import EventScheduler
from oadr30.values_map import ValuesMap
from oadr30.vtn import VTNOps
import json,time


def scheduler_callback(segment:ValuesMap):
    print (segment)

def scheduler_future_callback(segment:ValuesMap):
    print (segment)

def main():
    try:
        OADR3Config.duration_scale=1/360
        OADR3Config.events_start_now=True

        client= PriceServerClient(OlivinePriceServer.getUrl('hourly', 'fall', 'price'))
        events= client.getEvents()
        client= PriceServerClient(OlivinePriceServer.getUrl('hourly', 'fall', 'ghg'))
        ghgEvents=client.getEvents()
        events.appendEvents(ghgEvents) #combine them
        vtn = VTNOps(VTNRefImpl.base_url,VTNRefImpl.bl_client_id, VTNRefImpl.bl_client_secret)
        vtn.create_events(events)
    except Exception as ex:
        oadr3_log_critical("main failed")





if __name__ == "__main__":
    main()