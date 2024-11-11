from oadr30.vtn import VTNOps
from oadr30.log import oadr3_log_critical
from oadr30.price_server_client import PriceServerClient
from oadr30.config import OADR3Config, OlivinePriceServer, VTNRefImpl
from oadr30.scheduler import EventScheduler
from oadr30.values_map import ValuesMap
from oadr30.ven import Resource
import json,time


def scheduler_callback(segment:ValuesMap):
    print (segment)

def scheduler_future_callback(segment:ValuesMap):
    print (segment)

def main(base_url:str, auth_url:str, client_id:str, client_secret:str, ven_name:str):
    try:
        OADR3Config.duration_scale=1/360
        OADR3Config.events_start_now=True
        if base_url == None:
            base_url = VTNRefImpl.base_url
        if auth_url == None:
            auth_url = VTNRefImpl.auth_url
        if client_id == None:
            client_id = VTNRefImpl.client_id
        if client_secret == None:
            client_secret = VTNRefImpl.client_secret

        vtn = VTNOps(base_url=base_url, auth_url=auth_url, client_id=client_id, client_secret=client_secret, auth_token_url_is_json=False )
        ven = vtn.create_ven(resources=[Resource()])
        vtn.get_programs()
        program = vtn.get_program('0')
        events = vtn.get_events()
        for event in events:
            reportDescriptor = event.getReportPayloadDescriptors()
            if reportDescriptor:
                vtn.send_report(event.getId(), program.getId(), ven, reportDescriptor)

        timeSeries = events.getTimeSeries()
        scheduler=EventScheduler()
        scheduler.setTimeSeries(timeSeries)
        scheduler.registerCallback(scheduler_callback)
        scheduler.registerFutureCallback(scheduler_future_callback, 30)
        scheduler.start()
        scheduler.join()
    except Exception as ex:
        oadr3_log_critical("main failed")





if __name__ == "__main__":
     main(None, None, None, None, None)