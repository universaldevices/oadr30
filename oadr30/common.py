#Universal Devices
#MIT License
'''
    Common objects used throughout
'''
from typing import Any, List, Union
from .log import oadr3_log_critical

class Point:
    """
    A class to represent a point on a 2D grid.

    Attributes:
        x (float): A value on the x-axis.
        y (float): A value on the y-axis.

    Args:
        x (float): A value on the x-axis.
        y (float): A value on the y-axis.
    """

    def __init__(self, x: float, y: float):
        """
        Constructs all the necessary attributes for the point object.

        Args:
            x (float): A value on the x-axis.
            y (float): A value on the y-axis.
        """
        self.x = x
        self.y = y

    def getX(self)->float:
        return self.x

    def getY(self)->float:
        return self.y

    def setX(self, x:float):
        self.x = x

    def setY(self, y:float):
        self.y = y

    def __str__(self):
        """
        Generates a string representation of the point.

        Returns:
            str: A string representing the point as (x, y).
        """
        return f"Point(x={self.x}, y={self.y})"

class ValueMap(dict):
    """
    Represents one or more values associated with a type.
    For example, a type of "PRICE" contains a single float value.

    Attributes:
        value_type (str): Enumerated or private string signifying the nature of values.
        values (List[Union[float, int, str, bool, Point]]): A list of data points, 
        most often a singular value such as a price.
    """

    #def __init__(self, valueType: str, values: List[Union[float, int, str, bool, Point]]):
    def __init__(self, json_data):
        """
        Initializes the ValuesMap with a type and associated values.

        Args:
            valueType (str): The nature of the values, such as "PRICE".
            values (List[Union[float, int, str, bool, Point]]): The values associated with the type.
        """
        try:
            super.__init__(jason_data)
            #if not (1 <= len(self['valueType']) <= 128):
            #    raise ValueError("valueType must be between 1 and 128 characters")
            #if self['valueType'] not in ['float', 'int', 'str', 'bool', 'Point']:
            #    raise ValueError("valueType must be one of float, int, str, bool, or Point") 
        except Exception as ex:
            oadr3_log_critical(f"exception in ValueMap:__init__: {ex}", True)

    def getValueType(self)->str:
        try:
            return self['valueType']
        except Exception as ex:
            return 'float'

    def getValues(self)->List:
        try:
            return self['values']
        except Exception as ex:
            return []

    def __str__(self):
        return f"ValuesMap(valueType={self.valueType}, values={self.values})"

class IntervalPeriod(dict):
    """
    Defines temporal aspects of intervals.
    A duration of default PT0S indicates instantaneous or infinity, depending on payloadType.
    A randomizeStart of default null indicates no randomization.
    """
    def __init__(self, json_data):
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

class EventPayload(dict):
    """
        defines the actual payload inside an interval.
    """
    def __init__(self, json_data):
        try:
            super.__init__(json_data)
        except Exception as ex:
            oadr3_log_critical(f"exception in EventPayload:__init__: {ex}", True)
    
    def getPayloadType(self):
        try:
            return self['payloadType']
        except Exception as ex:
            return None

    def getValueType(self)->str:
        try:
            return self['valueType']
        except Exception as ex:
            return 'float'

    def getValues(self)->List:
        try:
            return self['values']
        except Exception as ex:
            return []

class Interval(dict):
    """
    An object defining a temporal window and a list of valuesMaps.
    If intervalPeriod is present, it may set temporal aspects of the interval or override event.intervalPeriod.
    """
    def __init__(self, json_data): 
        try:
            super().__init__(json_data)
        except Exception as ex:
            oadr3_log_critical(f"exception in interval: {ex}", True)

    def getId(self):
        try:
            return self['id'] 
        except Exception as ex:
            return None
    
    def getPayloads(self)->List:
        try:
            out=[]
            for pd in self['payloads']:
                out.append(EventPayload(pd))
            return out
        except Exception as ex:
            return None
    
#    def __repr__(self):
#        return (f"Interval(id={self.getId()}"
#                f"payloads={self.payloads})")


'''
Validate a string + its length
'''
def validate_string(string:str, length:int)->bool:
    try:
        if not isinstance(string, str) or not (1 <= len(string) <= length):
            return False
        return True
    except Exception as ex:
        oadr3_log_critical(f"exception in validate_string: {ex}")
        return False

'''
Raise an exception + log to the logfile
'''