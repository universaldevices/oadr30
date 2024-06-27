#Universal Devices
#MIT License

from .common import validate_string
from .log import Oadr3LoggedException

class EventPayloadDescriptor:
    """
    Contextual information used to interpret event valuesMap values.
    E.g. a PRICE payload simply contains a price value, an
    associated descriptor provides necessary context such as units and currency.
    """
    def __init__(self, payloadType:str, units=None, currency=None):
        if not validate_string(payloadType, 128):
            raise Oadr3LoggedException('error', "payloadType must be a string between 1 and 128 characters", True)
        
        self.payloadType = payloadType
        self.units = units
        self.currency = currency


    def getPayloadType(self)->str:
        return self.payloadType

    def getUnits(self)->str:
        return self.units

    def getCurrency(self)->str:
        return self.currency
    
    def __str__(self):
        return (f"EventPayloadDescriptor("
                f"payloadType={self.payloadType}, units={self.units}, "
                f"currency={self.currency})")

class ReportPayloadDescriptor:
    """
    Contextual information used to interpret report payload values.
    E.g. a USAGE payload simply contains a usage value, an
    associated descriptor provides necessary context such as units and data quality.
    """
    def __init__(self, payloadType, readingType=None, units=None, accuracy=None, confidence=None):

        if not validate_string(payloadType,128):
            raise Oadr3LoggedException('error', "payloadType must be a string between 1 and 128 characters", True)
        
        if readingType is not None and not isinstance(readingType, str):
            raise Oadr3LoggedException('error', "readingType must be a string or None", True)
        
        if units is not None and not isinstance(units, str):
            raise Oadr3LoggedException('error', "unit must be a string or None", True)
        
        if accuracy is not None and not isinstance(accuracy, (float, int)):
            raise Oadr3LoggedException('error', "accuracy must be a float or int or None")
        
        if confidence is not None and (not isinstance(confidence, int) or not (0 <= confidence <= 100)):
            raise Oadr3LoggedException('error', "confidence must be an integer between 0 and 100 or None")
        
        self.payloadType = payloadType
        self.readingType = readingType
        self.units = units
        self.accuracy = accuracy
        self.confidence = confidence

    def getPaylaodType(self)->str:
        return self.payloadType

    def getReadingType(self)->str:
        return self.readingType

    def getUnits(self)->str:
        return self.units

    def getAccuracy(self)->(float, int):
        return self.accuracy

    def getConfidence(self)->int:
        return self.confidence
    
    def __str__(self):
        return (f"ReportPayloadDescriptor("
                f"payloadType={self.payloadType}, readingType={self.readingType}, "
                f"units={self.units}, accuracy={self.accuracy}, confidence={self.confidence})")

