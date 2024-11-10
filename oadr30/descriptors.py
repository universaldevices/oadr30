#Universal Devices
#MIT License

from .common import validate_string
from .log import Oadr3LoggedException

class EventPayloadDescriptor(dict):
    """
    Contextual information used to interpret event valuesMap values.
    E.g. a PRICE payload simply contains a price value, an
    associated descriptor provides necessary context such as units and currency.
    """
    def __init__(self, json_data):
        try:
            super().__init__(json_data)
            if not validate_string(self['payloadType'], 128):
                raise Oadr3LoggedException('error', "payloadType must be a string between 1 and 128 characters", True)
        except Exception as ex:
            raise Oadr3LoggedException('critical', "exception in EventPayloadDescriptor Init", True)

    def getPayloadType(self)->str:
        try:
            return self['payloadType']
        except Exception as ex:
            return None

    def getUnits(self)->str:
        try:
            return self['units']
        except Exception as ex:
            return None

    def getCurrency(self)->str:
        try:
            return self['currency']
        except Exception as ex:
            return None
    
    def __str__(self):
        return (f"EventPayloadDescriptor("
                f"payloadType={self.getPayloadType()}, units={self.getUnits()}, "
                f"currency={self.getCurrency()})")

class ReportPayloadDescriptor(dict):
    """
    Contextual information used to interpret report payload values.
    E.g. a USAGE payload simply contains a usage value, an
    associated descriptor provides necessary context such as units and data quality.
    """
    def __init__(self, json_data):
        try:
            super().__init__(json_data)
            if not validate_string(self['payloadType'], 128):
                raise Oadr3LoggedException('error', "payloadType must be a string between 1 and 128 characters", True)
        except Exception as ex:
            raise Oadr3LoggedException('critical', "exception in ReportPayloadDescriptor Init", True)

    def getPaylaodType(self)->str:
        try:
            return self['payloadType']
        except Exception as ex:
            return None
    
    def getAggregate(self)->bool:
        try:
            return self['aggregate']
        except Exception as ex:
            return None

    def getFrequency(self)->int:
        try:
            return self['aggregate']
        except Exception as ex:
            return None

    def getHistorical(self)->bool:
        try:
            return self['historical']
        except Exception as ex:
            return None

    def getNumIntervals(self)->bool:
        try:
            return self['numIntervals']
        except Exception as ex:
            return None

    def getRepeat(self)->int:
        try:
            return self['repeat']
        except Exception as ex:
            return None

    def getStartInterval(self):
        try:
            return self['startInterval']
        except Exception as ex:
            return None

