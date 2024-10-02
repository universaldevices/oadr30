#Universal Devices
#MIT License
import json
from .log import Oadr3LoggedException, oadr3_log_critical
from .descriptors import EventPayloadDescriptor, ReportPayloadDescriptor
from .common import Interval, IntervalPeriod



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
      except Exception as ex:
        raise Oadr3LoggedException('critical', "exception in Event Init-json", True)

    def toJson(self)->str:
        return json.dumps(self)

    def getIntervalPeriod(self)->IntervalPeriod:
      try:
        return IntervalPeriod(self['intervalPeriod'])
      except Exception as ex:
        return None

    def getEventPayloadDescriptors(self)->[]:
      try:
        out=[]
        for pd in self['payloadDescriptors']:
          out.append(EventPayloadDescriptor(pd))
        return out
      except Exception as ex:
        return None

    def getIntervals(self)->[]:
      try:
        out=[]
        for intrv in self['intervals']:
          out.append(Event(intrv))
        return out
      except Exception as ex:
        return None


class Events(list):
  '''
    An array of events
  '''
  def __init__(self, json_data):
    try:
      if 'createdDateTime' in json_data:
        # we do not have an arry. It's just one stupid element 
        event = Event(json_data)
        d = event.getEventPayloadDescriptors()
        i = event.getIntervalPeriod()
        isi = event.getIntervals()
        super().append(Event(json_data))
      else:
        for event in json_data:
          super().append(Event(event))

    except Exception as ex:
       raise Oadr3LoggedException('critical', "exception in Events Init", True)

  def num_events(self):
    return len(self)
