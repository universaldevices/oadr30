#Universal Devices
#MIT License
import time
import threading
from datetime import datetime, timedelta
from .values_map import ValuesMap

class EventScheduler(threading.Thread):
    def __init__(self, timeseries, callback):
        '''
            timeseries is an array of valuemaps
        '''
        threading.Thread.__init__(self)
        self.timeseries:[ValuesMap] = timeseries  # List of datetime objects
        self.callback = callback      # Callback function to call when time is reached
        self.stop_event = threading.Event()  # Event to stop the thread
        self.current_index = 0 

    def run(self):
        #first go through the whole list and make sure you bypass
        #everything that's old and  not processed
        for self.current_index in range(len(self.timeseries)):
            segment:ValuesMap = self.timeseries[self.current_index]
            if datetime.now() > segment.getEndTime():
                segment.setProcessed()
                continue
            break

        # at this juncture, current_index points to a segment that needs to be scheduled
        while not self.stop_event.is_set():
            if self.current_index >= len(self.timeseries):
                #don't do anything and sleep
                time.sleep(1000)
                continue

            segment:ValuesMap=self.timeseries[self.current_index]
            current_time = datetime.now()
            start_time = segment.getStartTime()

            # Calculate the time to sleep until the next event
            time_diff = (start_time - current_time).total_seconds()
            if time_diff > 0:
                # Wait until the next event or stop event is set
                self.stop_event.wait(timeout=time_diff)
                
            # If the stop_event was set while waiting, exit early
            if self.stop_event.is_set():
                continue #stops it

            #if we get here, the event has already started
            #call the callback, set processed, increment index and continue
            self.callback(segment)
            segment.setProcessed()
            current_time = datetime.now()
            end_time = segment.getEndTime()
            #increment
            self.current_index=self.current_index+1
            time_diff = (end_time - current_time).total_seconds()
            if time_diff > 0:
                # Wait until the next event or stop event is set
                self.stop_event.wait(timeout=time_diff)


    def stop(self):
        self.stop_event.set()  # Set the event to signal stopping
