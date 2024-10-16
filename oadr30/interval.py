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
from .datetime_util import ISO8601_DT
from .config import OADR3Config
from datetime import datetime, timezone
import random

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
        '''
            Returns the [local] start time as ISO8601_DT object 
        '''
        try:
            iso_date = self['start']
            iso = ISO8601_DT(datetime.now(timezone.utc)) if OADR3Config.events_start_now else ISO8601_DT(iso_date)
            randomized_start= self.getRandomizedStart()
            if randomized_start != 0:
                iso.addSeconds(randomized_start, True)
            return iso
        except Exception as ex:
            return None

    def getDuration(self):
        '''
            Returns the ISO formatted duration in seconds
        '''
        try:
            duration = self['duration']
            iso = ISO8601_DT(duration)
            return iso.toSeconds()*OADR3Config.duration_scale
        except Exception as ex:
            return None

    def getRandomizedStart(self):
        '''
            Returns the randomized start seconds
        '''
        try:
            duration =  self['randomizedStart']
            iso = ISO8601_DT(duration)
            return random.randint(0, iso.toSeconds)
        except Exception as ex:
            return 0
        
#    def __repr__(self):
#        return (f"IntervalPeriod(start={self.start}, duration={self.duration}, "
#       f"randomizeStart={self.randomizeStart})")

class Interval(dict):
    """
    An object defining a temporal window and a list of valuesMaps.
    If intervalPeriod is present, it may set temporal aspects of the interval or override event.intervalPeriod.
    """
    def __init__(self, json_data, index:int, global_interval_period:IntervalPeriod , global_payload_descriptor:list ): 
        '''
            index must start from 0
        '''
        try:
            super().__init__(json_data)
            self.global_interval_period = global_interval_period
            self.global_payload_descriptor = global_payload_descriptor
            self.index=0 if index < 0 else index
            self.interval_period, self.is_global_interval_period=self.__getIntervalPeriod()
        except Exception as ex:
            oadr3_log_critical(f"exception in interval: {ex}", True)

    def getId(self):
        try:
            return self['id'] 
        except Exception as ex:
            return None
    
    def getValues(self)->list:
        values=[]
        try:
            ip=self.interval_period
            if ip == None:
                oadr3_log_critical("need interval period", False)
                return values

            startTime:ISO8601_DT=ip.getStartTime()
            duration=ip.getDuration()
            for pd in self['payloads']:
                if self.is_global_interval_period:
                    #if it's global, we have to multiply the duration by the index
                    abs_duration = duration * self.index
                    startTime = startTime.addSeconds(abs_duration)
                values.append(ValuesMap(pd, startTime, duration, self.global_payload_descriptor))
            return values
        except Exception as ex:
            return values

    def __getIntervalPeriod(self):
        ''' 
            returns the actual interval period + whether a global one (True) or local (False)
        '''
        local_interval_period = None
        try:
            local_interval_period = IntervalPeriod(self['intervalPeriod'])
        except Exception as ex:
            local_interval_period = None

        if local_interval_period == None:
            return self.global_interval_period, True 
            
        return local_interval_period, False 

#    def __repr__(self):
#        return (f"Interval(id={self.getId()}"
#                f"payloads={self.payloads})")

