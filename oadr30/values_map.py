#Universal Devices
#MIT License
'''
    Common objects used throughout
'''
from typing import Any, List, Union
from .log import oadr3_log_critical
from .definitions import oadr3_alert_types, oadr3_reg_event_types, oadr3_cta2045_types
from .descriptors import EventPayloadDescriptor

class ValuesMap(dict):
    """
    Represents one or more values associated with a type.
    For example, a type of "PRICE" contains a single float value.

    Attributes:
        type (str): Enumerated or private string signifying the nature of values.
        values (List[Union[float, int, str, bool, Point]]): A list of data points, 
        most often a singular value such as a price.
    """

    def __init__(self, json_data, global_payload_descriptors:list | None):
        try:
            super().__init__(json_data)
            payloadType=self.getPayloadType()
            self.eventType=None #regular events
            self.eventInfo=None
            self.units = None
            self.currency = None

            if payloadType in oadr3_reg_event_types:
                self.eventType='event' #regular events
                self.eventInfo = oadr3_reg_event_types[payloadType]
            elif payloadType in oadr3_alert_types:
                self.eventType='alert' #alerts
                self.eventInfo = oadr3_alert_types[payloadType]
            elif payloadType in oadr3_cta2045_types:
                self.eventType='cta2045' #obvious
                self.eventInfo = oadr3_cta2045_types[payloadType]
            else:
                raise oadr3_log_critical(f"{payloadType} is not valid. {ex}", True)
            
            if global_payload_descriptor is not None:
                for ed in global_payload_descriptor:
                    if ed.getPayloadType() == payloadType:
                        self.units = ed.getUnits()
                        self.currency = ed.getCurrency()

        except Exception as ex:
            oadr3_log_critical(f"exception in ValueMap:__init__: {ex}", True)

    def getPayloadType(self):
        try:
            return self['type']
        except Exception as ex:
            try:
                return self['payloadType']
            except Exception as ex2:
                return None

    def getEventType(self):
        return self.eventType

    def getDataType(self):
        try:
            dt = self.eventInfo['data_type']
        except Exception as ex:
            return float

    def getMin(self):
        try:
            self.eventInfo['min']
        except Exception as ex:
            return None

    def getMax(self):
        try:
            self.eventInfo['max']
        except Exception as ex:
            return None

    def getDescription(self):
        try:
            self.eventInfo['desc']
        except Exception as ex:
            return None

    def getValues(self)->list:
        try:
            values=[]
            data_type=self.getDataType()
            if data_type == list:
                values.append(self['values'])
            else:
                for value in self['values']:
                    values.append(data_type(value))

            return values
        except Exception as ex:
            oadr3_log_critical(f"invalid values in the array: {ex}", True)
            return None

    def isEvent(self):
        try:
            return self.eventType == "event"
        except Exception as ex:
            return False

    def isAlert(self):
        try:
            return self.eventType == "alert"
        except Exception as ex:
            return False

    def isCta2045(self):
        try:
            return self.eventType == "cta2045"
        except Exception as ex:
            return False
            
