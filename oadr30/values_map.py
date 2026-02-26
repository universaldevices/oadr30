#Universal Devices
#MIT License
'''
    Common objects used throughout
'''
from .log import oadr3_log_critical
from .definitions import oadr3_alert_types, oadr3_reg_event_types, oadr3_cta2045_types
from .datetime_util import ISO8601_DT, get_current_utc_time 
from zoneinfo import ZoneInfo

class ValuesMap:
    """
    Represents one or more values associated with a type.
    For example, a type of "PRICE" contains a single float value.

    Attributes:
        type (str): Enumerated or private string signifying the nature of values.
        values (List[Union[float, int, str, bool, Point]]): A list of data points, 
        most often a singular value such as a price.
    """

    @staticmethod
    def getNormalizedValuesMap(json_data, startTime:ISO8601_DT, duration, global_payload_descriptor:list | None)->list:
        """ 
            returns a list of values maps based on the payload
        """ 

        try:
            vm = ValuesMap(json_data, startTime, duration, global_payload_descriptor)
            if vm.payloadType != 'PRICE' and vm.payloadType != "GHG" and vm.payloadType != "EXPORT_PRICE":
                return [vm]


            num_values = len(vm.values) 
            if num_values <= 1:
                return [vm]

            out = []
            duration = vm.duration/num_values
            index=0

            for value in vm.values:
                st=startTime.addSeconds(index*duration)
                json_data['values']=[value]
                cp = ValuesMap(json_data, st, duration, global_payload_descriptor)
                out.append(cp)
                index+=1
            return out
        except Exception as ex:
            oadr3_log_critical(f"failed creating a list of values maps: {ex}", True)
            return None


    def __init__(self, json_data, start_time:ISO8601_DT, duration, global_payload_descriptor:list | None):
        try:
            data=dict(json_data)
            eventInfo=None

            self.payloadType=self.__getPayloadType(data)
            self.eventType=None #regular events
            self.units = None
            self.currency = None
            self.startTime=start_time.toUtc()
            self.duration=duration
            self.endTime=start_time.addSeconds(duration).toUtc()
            self.processed=False #whether the scheduler has already processed 
            self.notified=False

            ##to calculate the end time:
            #endTime=startTime.addSeconds(duration)
            eventInfo = None

            if self.payloadType in oadr3_reg_event_types:
                self.eventType='event' #regular events
                eventInfo = oadr3_reg_event_types[self.payloadType]
            elif self.payloadType in oadr3_alert_types:
                self.eventType='alert' #alerts
                eventInfo = oadr3_alert_types[self.payloadType]
            elif self.payloadType in oadr3_cta2045_types:
                self.eventType='cta2045' #obvious
                eventInfo = oadr3_cta2045_types[self.payloadType]
            else:
                raise oadr3_log_critical(f"{self.payloadType} is not valid. {ex}", True)

            try:
                self.dataType = eventInfo['data_type']
            except Exception as ex:
                self.dataType = None
            try:
                self.min = eventInfo['min']
            except Exception as ex:
                self.min = None
            try:
                self.max = eventInfo['max']
            except Exception as ex:
                self.max = None
            try:
                self.desc = eventInfo['desc']
            except Exception as ex:
                self.desc = None

            #should be done after we figure out what the data type is 
            self.values=self.__getValues(data)
            if global_payload_descriptor is not None:
                for ed in global_payload_descriptor:
                    if ed.getPayloadType() == self.payloadType:
                        self.units = ed.getUnits()
                        self.currency = ed.getCurrency()

        except Exception as ex:
            oadr3_log_critical(f"exception in ValueMap:__init__: {ex}", True)

    def __getPayloadType(self, data):
        try:
            return data['type']
        except Exception as ex:
            try:
                return data['payloadType']
            except Exception as ex2:
                return None

    def __getValues(self, data)->list:
        try:
            values=[]
            data_type=self.getDataType()
            if data_type == list:
                values.append(data['values'])
            else:
                for value in data['values']:
                    values.append(data_type(value))

            return values
        except Exception as ex:
            oadr3_log_critical(f"invalid values in the array: {ex}", True)
            return None

    def setNotified(self):
        self.notified=True

    def isNotified(self):
        return self.notified

    def setProcessed(self):
        self.processed=True

    def isProcessed(self):
        return self.processed

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime
    
    def isEnded(self):
        return get_current_utc_time() > self.endTime

    def getDuration(self):
        return self.duration

    def getPayloadType(self):
        return self.payloadType

    def getValues(self):
        return self.values

    def getEventType(self):
        return self.eventType

    def getDataType(self):
        return self.dataType

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    def getDescription(self):
        return self.desc

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

    def __str__(self):
        #return f'start={ISO8601_DT.toLocal_dt(self.startTime)}, end={ISO8601_DT.toLocal_dt(self.endTime)},(utc={self.startTime} to {self.endTime}), duration={self.duration}, type={self.payloadType}, value={self.values[0]}, processed={self.processed}, ended={self.isEnded()}'
        return f'FROM:{ISO8601_DT.toLocal_dt(self.startTime)}, TO:{ISO8601_DT.toLocal_dt(self.endTime)}, DURATION:{self.duration}, NOTIFIED:{self.notified}, PROCESSED:{self.processed}, ENDED={self.isEnded()}, TYPE:{self.payloadType}, VALUE:{self.values[0]}'

    #we need this function to check whether timeseries are identical
    def __eq__(self, other):
        try:
            if isinstance(other, ValuesMap):
                return  self.getStartTime() == other.getStartTime() and \
                    self.getDuration() == other.getDuration() and \
                    self.getPayloadType() == other.getPayloadType() and \
                    self.getValues() == other.getValues() and \
                    self.getEventType() == other.getEventType() and \
                    self.getDataType() == other.getDataType() and \
                    self.getMax() == other.getMax() and \
                    self.getMin() == other.getMin()
            return False
        except Exception as ex:
            return False

                    
