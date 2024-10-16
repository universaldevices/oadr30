#Universal Devices
#MIT License
# iso and timezone conversion utilities

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from tzlocal import get_localzone
from dateutil import parser
import isodate
import pytz

def get_current_utc_time():
    current_time = datetime.now(timezone.utc)
    return current_time.replace(tzinfo=None)


class ISO8601_DT:

    def __init__(self, iso_date):
        try:
            if isinstance(iso_date, str):
                if not self.isDuration(iso_date):
                    dt_iso = parser.isoparse(iso_date)
                    #convert everything to utc
                    self.dt= dt_iso.astimezone(pytz.utc)
            elif isinstance(iso_date, datetime):
                self.dt=iso_date
                self.dt.astimezone(pytz.utc)

        except Exception as ex:
            raise 

    def isDuration(self, iso_date:str):
        try:
            # Attempt to parse the string as an ISO 8601 duration
            self.duration=isodate.parse_duration(iso_date)
            return True
        except (isodate.isoerror.ISO8601Error, ValueError):
            self.duration=-1
            return False

    def toUtc(self):
        try:
            return self.dt.replace(tzinfo=None)
        except Exception as ex:
            return self.dt

    def getLocalTimezone(self):
        return get_localzone()

    def toLocal(self):
        try:
            #first covnert to utc
            local_tz = get_localzone()
            dt_local = self.dt.astimezone(local_tz)
            return dt_local.replace(tzinfo=None)
        except Exception as ex:
            return self.dt

    def hasTimezone(self):
        try:
            return True if self.dt.tzinfo is not None else False
        except ValueError:
            return False

    def toSeconds(self):
        '''
            return -1 if error
        '''
        try:
            # Parse the ISO 8601 duration string
            total_seconds = self.duration.total_seconds()
            return total_seconds
        except Exception as ex:
            return -1

    def addSeconds(self, seconds_to_add, persist=False) :
    #    if seconds_to_add <= 0:
    #        return ISO8601_DT(self.dt)

        new_dt = self.dt + timedelta(seconds=seconds_to_add)
        if persist:
            self.dt = new_dt
            return self
        return ISO8601_DT(new_dt)


