#Universal Devices
#MIT License
'''
    Common objects used throughout
'''
from typing import Any, List, Union
from .log import oadr3_log_critical
from .definitions import oadr3_alert_types, oadr3_reg_event_types, oadr3_cta2045_types

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