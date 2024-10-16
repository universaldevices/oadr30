#Universal Devices
#MIT License
import time
import threading
from datetime import datetime, timedelta, timezone
from .values_map import ValuesMap
from .datetime_util import get_current_utc_time

class FutureCallback:
    def __init__(self, callback:callable, duration: int):
        self.callback=callback
        self.duration=duration

class EventScheduler(threading.Thread):
    def __init__(self):
        '''
            timeseries is an array of valuemaps
            all times are in utc and not local
        '''
        threading.Thread.__init__(self)
        self.timeseries:[ValuesMap] = None  # List of datetime objects
        self.callbacks = [] #an array of callbacks
        self.future_callbacks = [] #an array of callbacks
        self.stop_event = threading.Event()  # Event to stop the thread
        self.stop()
        self.current_index = 0 

    def registerCallback(self, callback):
        self.callbacks.append(callback)
        

    def removeCallback(self, callback):
        try:
            self.callbacks.remove(callback)
        except Exception as ex:
            pass

    def registerFutureCallback(self, callback, duration:int):
        '''
            Register to be notified of events duration seconds in the future
        '''
        self.future_callbacks.append(FutureCallback(callback,duration))
        
    def removeFutureCallback(self, callback):
        try:
            for i in range(len(self.future_callbacks)):
                f_callback=self.future_callbacks[i]
                if f_callback == callback:
                    del self.future_callbacks[i]
        except Exception as ex:
            pass

    def setTimeSeries(self, ts:[ValuesMap]):
        while not self.isStopped():
            self.stop()
            self.stop_event.wait(timeout=2)

        self.stop_event.clear()

        if self.timeseries != ts:
            self.timeseries = ts 
            self.current_index = 0

    def notifyFutureEvents(self, start_index:int):
        try:
               for f_callback in self.future_callbacks:
                    duration = f_callback.duration
                    current_time=get_current_utc_time()
                    future_time=current_time + timedelta(seconds=duration)
                    #now go through all the segments starting from the start_index
                    #and see whether or not they are in the range
                    print (f" --- future: {future_time} ---")
                    for start_index in range(len(self.timeseries)):
                        segment:ValuesMap = self.timeseries[start_index]
                        if segment.isProcessed():
                            continue
                        if segment.getStartTime() > future_time:
                            break 
                        f_callback.callback(segment)
                    print (" --- end future ---")
        except Exception as ex:
            pass

    def run(self):
        #first go through the whole list and make sure you bypass
        #everything that's old and  not processed
        for self.current_index in range(len(self.timeseries)):
            segment:ValuesMap = self.timeseries[self.current_index]
            if get_current_utc_time() > segment.getEndTime():
                segment.setProcessed()
                continue
            break

        # at this juncture, current_index points to a segment that needs to be scheduled
        while not self.stop_event.is_set():
            if self.current_index >= len(self.timeseries):
                self.stop_event.wait(timeout=1800)
                continue

            segment:ValuesMap=self.timeseries[self.current_index]
            current_time = get_current_utc_time() 
            start_time = segment.getStartTime()

            # Calculate the time to sleep until the next event
            time_diff = (start_time - current_time).total_seconds()
            if time_diff > 0:
                self.notifyFutureEvents(self.current_index)
                # Wait until the next event or stop event is set
                self.stop_event.wait(timeout=time_diff)
                
            # If the stop_event was set while waiting, exit early
            if self.stop_event.is_set():
                continue #stops it

            #if we get here, the event has already started
            #call the callback, set processed, increment index and continue
            for callback in self.callbacks:
                callback(segment)
            segment.setProcessed()
            #notify future events
            current_time = get_current_utc_time() 
            end_time = segment.getEndTime()
            #increment
            self.current_index=self.current_index+1
            time_diff = (end_time - current_time).total_seconds()
            if time_diff > 0:
                self.notifyFutureEvents(self.current_index+1)
                # Wait until the next event or stop event is set
                self.stop_event.wait(timeout=time_diff)


    def isStopped(self):
        return self.stop_event.is_set()

    def stop(self):
        self.stop_event.set()  # Set the event to signal stopping
