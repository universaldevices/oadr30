#Universal Devices
#MIT License
# iso and timezone conversion utilities

from datetime import datetime
from zoneinfo import ZoneInfo
from tzlocal import get_localzone
from dateutil import parser
import isodate
import pytz


class ISO8601_Util:

    def __init__(self, iso_date:str):
        self.iso_date=iso_date

    def toUtc(self):
        try:
            dt = parser.isoparse(self.iso_date)
            # Convert the datetime to UTC
            dt_utc = dt.astimezone(pytz.utc)
            return dt_utc.replace(tzinfo=None)
        except Exception as ex:
            return self.iso_date

    def getLocalTimezone(self):
        return get_localzone()

    def toLocal(self):
        try:
            #first covnert to utc
            #we cannot use toUtc since it will have timzone offset in there
            dt = parser.isoparse(self.iso_date)
            dt_utc = dt.astimezone(pytz.utc)
            local_tz = get_localzone()
            dt_local = dt_utc.astimezone(local_tz)
            return dt_local.replace(tzinfo=None)
        except Exception as ex:
            return self.iso_date

    def hasTimezone(self):
        try:
            # Parse the ISO 8601 string
            dt = parser.isoparse(self.iso_date)
            return True if dt.tzinfo is not None else False
        except ValueError:
            return False

    def toSeconds(self):
        '''
            return -1 if error
        '''
        try:
            # Parse the ISO 8601 duration string
            duration = isodate.parse_duration(self.iso_date)
            # Convert to total seconds
            total_seconds = duration.total_seconds()
            return total_seconds
        except Exception as ex:
            return -1 


