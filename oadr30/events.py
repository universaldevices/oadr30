#Universal Devices
#MIT License
import json
from .log import Oadr3LoggedException, oadr3_log_critical
from .descriptors import EventPayloadDescriptor, ReportPayloadDescriptor
from .interval import Interval, IntervalPeriod



'''
This class represents an openADR event
event: Event object to communicate a Demand Response request to VEN.
yaml 3.0.1:
event:
      type: object
      description: |
        Event object to communicate a Demand Response request to VEN.
        If intervalPeriod is present, sets default start time and duration of intervals.
      required:
        - programID
        - intervals
      properties:
        id:
          $ref: '#/components/schemas/objectID'
          # VTN provisioned on object creation.
        createdDateTime:
          $ref: '#/components/schemas/dateTime'
          #  VTN provisioned on object creation.
        modificationDateTime:
          $ref: '#/components/schemas/dateTime'
          #  VTN provisioned on object modification.
        objectType:
          type: string
          description: Used as discriminator
          enum: [EVENT]
          # VTN provisioned on object creation.
        programID:
          $ref: '#/components/schemas/objectID'
          # ID attribute of program object this event is associated with.
        eventName:
          type: string
          description: User defined string for use in debugging or User Interface.
          example: price event 11-18-2022
          nullable: true
          default: null
        priority:
          type: integer
          minimum: 0
          description: Relative priority of event. A lower number is a higher priority.
          example: 0
          nullable: true
          default: null
        targets:
          type: array
          description: A list of valuesMap objects.
          items:
            $ref: '#/components/schemas/valuesMap'
          nullable: true
          default: null
        reportDescriptors:
          type: array
          description: A list of reportDescriptor objects. Used to request reports from VEN.
          items:
            $ref: '#/components/schemas/reportDescriptor'
          nullable: true
          default: null
        payloadDescriptors:
          type: array
          description: A list of payloadDescriptor objects.
          items:
            $ref: '#/components/schemas/eventPayloadDescriptor'
          nullable: true
          default: null
        intervalPeriod:
          $ref: '#/components/schemas/intervalPeriod'
          # Defines default start and durations of intervals.
        intervals:
          type: array
          description: A list of interval objects.
          items:
            $ref: '#/components/schemas/interval'
'''

class Event(dict):
    '''
      Initialize using the json received from the VTN
    '''
    def __init__(self, json_data):
        try:
          super().__init__(json_data)
          self.tsValues=[]
          self.__createTimeSeriesValues()
        except Exception as ex:
          raise Oadr3LoggedException('critical', "exception in Event Init-json", True)

    def toJson(self)->str:
        return json.dumps(self)

    def getId(self)->str:
        try:
          return self['id']
        except Exception as ex:
          return None

    def getProgramId(self)->str:
        try:
          return self['programID']
        except Exception as ex:
          return None


    def getIntervalPeriod(self)->IntervalPeriod:
        try:
          return IntervalPeriod(self['intervalPeriod'])
        except Exception as ex:
          return None

    def getEventPayloadDescriptors(self)->list:
        try:
          out=[]
          for pd in self['payloadDescriptors']:
            out.append(EventPayloadDescriptor(pd))
          return out
        except Exception as ex:
          return None

    def getReportPayloadDescriptors(self)->list:
        try:
          out=[]
          for pd in self['reportDescriptors']:
            out.append(ReportPayloadDescriptor(pd))
          return out
        except Exception as ex:
          return None

    def getIntervals(self)->list:
        try:
          intervals=[]
          index=0
          for intrv in self['intervals']:
            intervals.append(Interval(intrv, index, self.getIntervalPeriod(), self.getEventPayloadDescriptors()))
            index+=1
          return intervals
        except Exception as ex:
          return None

    def __createTimeSeriesValues(self):
        self.tsValues.clear()
        intervals = self.getIntervals()
        for interval in intervals:
          values=interval.getValues()
          if values:
            for value in values:
              self.tsValues.append(value)

    def getTimeSeriesValues(self):
        return self.tsValues

class Events(list):
  '''
    An array of events
  '''
  def __init__(self, json_data):
  #  self.event_buckets={} #bucket based on payload type
    try:
      if 'createdDateTime' in json_data:
        # we do not have an arry. It's just one stupid element 
        event = Event(json_data)
        super().append(Event(json_data))
      else:
        for event in json_data:
          super().append(Event(event))

    except Exception as ex:
       raise Oadr3LoggedException('critical', "exception in Events Init", True)

  def appendEvents(self, events):
    try:
        for event in events:
          self.append(event)

    except Exception as ex:
      oadr3_log_critical("failed appending events", True)
      

  def getTimeSeries(self):
    sorted_out=[]
    try:
      out=[]
      for event in self:
        out.extend(event.getTimeSeriesValues())
      #sort everything based on start time
      sorted_out = sorted(out, key=lambda x: x.getStartTime() )
    except Exception as ex:
      oadr3_log_critical("failed sorting", True)
    return sorted_out

  def num_events(self):
    return len(self)
