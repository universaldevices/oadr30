#Universal Devices
#MIT License
'''
    Common objects used throughout
'''
from typing import Any, List, Union
from .log import oadr3_log_critical
from .definitions import oadr3_alert_types, oadr3_reg_event_types, oadr3_cta2045_types
from .values_map import ValuesMap
from .descriptors import EventPayloadDescriptor

class IntervalPeriod(dict):
    """
    Defines temporal aspects of intervals.
    A duration of default PT0S indicates instantaneous or infinity, depending on payloadType.
    A randomizeStart of default null indicates no randomization.
    """
    def __init__(self, json_data):
        self.__update__(json_data)


    def __update__(self, json_data):
        try:
            super().__init__(json_data)
            if 'start' in self:
                if self['start'] is None or not isinstance(self['start'], str):
                    raise ValueError("start must be a string in time format or None")
            if 'duration' in self:
                if self['duration'] is not None and not isinstance(self['duration'], str):
                    raise ValueError("duration must be a string in duration format or None")
            if 'randomizedStart' in self: 
                if self['randomizeStart'] is not None and not isinstance(self['randomizeStart'], str):
                    raise ValueError("randomizeStart must be a string in duration format or None")
        except Exception as ex:
            oadr3_log_critical(f"exception in IntervalPeriod:__init__: {ex}", True)

    def getStartTime(self):
        try:
            return self['start']
        except Exception as ex:
            return None

    def getDuration(self):
        try:
            return self['duration']
        except Exception as ex:
            return None

    def getRandomizedStart(self):
        try:
            return self['randomizedStart']
        except Exception as ex:
            return None
        
#    def __repr__(self):
#        return (f"IntervalPeriod(start={self.start}, duration={self.duration}, "
#       f"randomizeStart={self.randomizeStart})")

class Interval(dict):
    """
    An object defining a temporal window and a list of valuesMaps.
    If intervalPeriod is present, it may set temporal aspects of the interval or override event.intervalPeriod.
    """
    def __init__(self, json_data, global_interval_period:IntervalPeriod , global_payload_descriptor:list ): 
        try:
            super().__init__(json_data)
            self.global_interval_period = global_interval_period
            self.global_payload_descriptor = global_payload_descriptor
        except Exception as ex:
            oadr3_log_critical(f"exception in interval: {ex}", True)

    def getId(self):
        try:
            return self['id'] 
        except Exception as ex:
            return None
    
    def getValues(self)->list:
        try:
            values=[]
            for pd in self['payloads']:
                values.append(ValuesMap(pd, global_payload_descriptor))
            return values
        except Exception as ex:
            return None

    def getIntervalPeriod(self):
        try:
            local_interval_perid = IntervalPeriod(self['intervalPeriod'])
            return self.global_interval_period if local_interval_period == None else self.global_interval_period
        except Exception as ex:
            return None

        
    
#    def __repr__(self):
#        return (f"Interval(id={self.getId()}"
#                f"payloads={self.payloads})")

