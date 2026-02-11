#Universal Devices
#MIT License
import threading
from datetime import timedelta
from .values_map import ValuesMap
from .datetime_util import get_current_utc_time

class FutureCallback:
    def __init__(self, callback:callable, duration: int):
        self.callback=callback
        self.duration=duration

class SchedulePoint:
    """A point in time when one or more event transitions occur.
       The scheduler walks a sorted list of these, sleeping between points.
    """
    def __init__(self, time):
        self.time = time
        self.starting = []   # segments that START at this time
        self.ending = []     # segments that END at this time

    def __repr__(self):
        return (f"SchedulePoint({self.time}, "
                f"starts={len(self.starting)}, "
                f"ends={len(self.ending)})")

class SchedulerControl():
    def __init__(self):
        self.stop_event = threading.Event()  # Event to signal stopping the thread
        self.start_event = threading.Event()  # Event to signal starting the thread
        self.stopped = True

    def wait_for_stop(self, timeout=None):
        self.stopped = False
        result = self.stop_event.wait(timeout=timeout)
        return result
    
    def wait_for_start(self, timeout=None):
        self.stopped = True
        result = self.start_event.wait(timeout=timeout)
        return result
        
    def start(self):
        self.stop_event.clear()  # Clear the stop event to allow the thread to run
        self.start_event.set()  # Set the start event to signal the thread to start

    def stop(self):
        self.stop_event.set()  # Set the stop event to signal the thread to stop
        self.start_event.clear()  # Clear the start event

    def is_start_set(self):
        return self.start_event.is_set()
    
    def is_stop_set(self):
        return self.stop_event.is_set()
    
    def is_stopped(self):
        return self.stopped


class EventScheduler(threading.Thread):
    def __init__(self):
        '''
            timeseries is an array of valuemaps
            all times are in utc and not local
        '''
        threading.Thread.__init__(self)
        self.timeseries:list[ValuesMap] = None  # List of datetime objects
        self.callbacks = [] #an array of callbacks
        self.future_callbacks = [] #an array of callbacks
        self.scheduler_control = SchedulerControl()  # Event to signal stopping the thread 
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

    def setTimeSeries(self, ts:list[ValuesMap]):
        if not self.is_alive():
            self.start()
        if self.timeseries == ts:
            return
        #different time series
        while not self.scheduler_control.is_stop_set():
            self.scheduler_control.stop()

        self.timeseries = ts 
        #restart the thread
        self.scheduler_control.start()

    def _build_schedule(self, timeseries:list[ValuesMap]) -> list[SchedulePoint]:
        """Build a sorted list of SchedulePoints from a flat timeseries.
           Each unique start/end time becomes a single SchedulePoint
           containing all the segments that transition at that moment.
        """
        points = {}  # datetime -> SchedulePoint
        for segment in timeseries:
            start = segment.getStartTime()
            end   = segment.getEndTime()

            if start not in points:
                points[start] = SchedulePoint(start)
            points[start].starting.append(segment)

            if end not in points:
                points[end] = SchedulePoint(end)
            points[end].ending.append(segment)

        return sorted(points.values(), key=lambda p: p.time)

    def _notify_future_events(self, schedule:list[SchedulePoint], from_index:int):
        """Notify future-callbacks about upcoming segments within their look-ahead window."""
        try:
            for f_callback in self.future_callbacks:
                current_time = get_current_utc_time()
                future_time  = current_time + timedelta(seconds=f_callback.duration)
                for i in range(from_index, len(schedule)):
                    point = schedule[i]
                    if point.time > future_time:
                        break
                    for segment in point.starting:
                        if not segment.isProcessed():
                            f_callback.callback(segment)
        except Exception as ex:
            pass

    def run(self):

        while True:
            self.scheduler_control.wait_for_start(timeout=1800)
            if self.scheduler_control.is_stop_set():
                continue

            schedule = self._build_schedule(self.timeseries)

            # ------ skip schedule points that are entirely in the past ------
            point_index = 0
            now = get_current_utc_time()
            while point_index < len(schedule) and schedule[point_index].time <= now:
                for segment in schedule[point_index].starting:
                    if now > segment.getEndTime():
                        segment.setProcessed()
                point_index += 1

            # ------ walk the remaining schedule ------
            while point_index < len(schedule) and not self.scheduler_control.is_stop_set():
                point = schedule[point_index]
                current_time = get_current_utc_time()

                # sleep until this trigger point
                time_diff = (point.time - current_time).total_seconds()
                if time_diff > 0:
                    self._notify_future_events(schedule, point_index)
                    self.scheduler_control.wait_for_stop(timeout=time_diff)
                    if self.scheduler_control.is_stop_set():
                        break

                # --- process endings first so callbacks know prior events finished ---
                for segment in point.ending:
                    for callback in self.callbacks:
                        callback(segment)   # segment.isEnded() == True at this time

                # --- then process starts ---
                for segment in point.starting:
                    for callback in self.callbacks:
                        callback(segment)
                    segment.setProcessed()

                point_index += 1

            # all points consumed (or stopped) – wait for new timeseries
            if not self.scheduler_control.is_stop_set():
                self.scheduler_control.stop()
    
    def stop(self):
        if self.scheduler_control.is_stopped():
            return
        self.scheduler_control.stop()  # Set the event to signal stopping
        self.timeseries = None
        self.current_index = 0
       # for callback in self.callbacks:
       #     callback(None)
