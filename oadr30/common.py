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

class ValueMap:
    """
    Represents one or more values associated with a type.
    For example, a type of "PRICE" contains a single float value.

    Attributes:
        value_type (str): Enumerated or private string signifying the nature of values.
        values (List[Union[float, int, str, bool, Point]]): A list of data points, 
        most often a singular value such as a price.
    """

    def __init__(self, valueType: str, values: List[Union[float, int, str, bool, Point]]):
        """
        Initializes the ValuesMap with a type and associated values.

        Args:
            valueType (str): The nature of the values, such as "PRICE".
            values (List[Union[float, int, str, bool, Point]]): The values associated with the type.
        """
        if not (1 <= len(valueType) <= 128):
            raise ValueError("value_type must be between 1 and 128 characters")
        
        self.valueType = valueType
        self.values = values

    def getValueType(self)->str:
        return self.value_type

    def getValues(self)->List:
        return self.values

    def __str__(self):
        return f"ValuesMap(valueType={self.valueType}, values={self.values})"

class IntervalPeriod:
    """
    Defines temporal aspects of intervals.
    A duration of default PT0S indicates instantaneous or infinity, depending on payloadType.
    A randomizeStart of default null indicates no randomization.
    """
    def __init__(self, start, duration=None, randomizeStart=None):
        if not isinstance(start, str):
            raise ValueError("start must be a string in dateTime format")
        
        if duration is not None and not isinstance(duration, str):
            raise ValueError("duration must be a string in duration format or None")
        
        if randomizeStart is not None and not isinstance(randomizeStart, str):
            raise ValueError("randomizeStart must be a string in duration format or None")
        
        self.start = start
        self.duration = duration
        self.randomizeStart = randomizeStart
    
    def __repr__(self):
        return (f"IntervalPeriod(start={self.start}, duration={self.duration}, "
                f"randomizeStart={self.randomizeStart})")

class Interval:
    """
    An object defining a temporal window and a list of valuesMaps.
    If intervalPeriod is present, it may set temporal aspects of the interval or override event.intervalPeriod.
    """
    def __init__(self, id, payloads:ValueMap, intervalPeriod:IntervalPeriod=None):
        if not isinstance(id, int):
            raise ValueError("id must be an integer")
        
        if not isinstance(payloads, ValueMap):
            raise ValueError("payloads must be a list")
        
        if intervalPeriod is not None and not isinstance(intervalPeriod, IntervalPeriod):
            raise ValueError("intervalPeriod must be a dictionary or None")
        
        self.id = id
        self.intervalPeriod = intervalPeriod
        self.payloads = payloads
    
    def __repr__(self):
        return (f"Interval(id={self.id}, intervalPeriod={self.intervalPeriod}, "
                f"payloads={self.payloads})")


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