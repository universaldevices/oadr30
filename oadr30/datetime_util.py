#Universal Devices
#MIT License
# iso and timezone conversion utilities

from datetime import datetime
from zoneinfo import ZoneInfo
import pytz
from .log import oadr3_log_critical

def iso8601_utc_to_local_datetime(iso_utc_datetime:str):
    try:
        # Parse the ISO 8601 string into a datetime object
        utc_time = datetime.strptime(iso_utc_datetime, "%Y-%m-%dT%H:%M:%SZ")

    except Exception as ex:
        oadr3_log_critical(f"exception conversion from iso8601 to local time: {ex}")



