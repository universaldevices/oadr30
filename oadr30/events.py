#Universal Devices
#MIT License
import json
from .log import Oadr3LoggedException, oadr3_log_critical
from .descriptors import EventPayloadDescriptor, ReportPayloadDescriptor
from .common import Interval



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

    def __init__(self, eventId:str, programId:str, intervals:[Interval], *args, **kwargs):
        if programId == None or eventId == None or intervals == None:
            raise Oadr3LoggedException('critical', "error: event requires programId, eventId, and intervals", True)

            try:

                # Default elements
                default_elements = {
                    'id': eventId,
                    'programID': programId,
                }
                
                # Initialize the dict with default elements
                super().__init__(default_elements, *args, **kwargs)

                # Update the dict with any additional keyword arguments
                self.update(kwargs)

                if self.get("intervals") == None:
                    raise Oadr3LoggedException('critical',"event must have an interval ...")
            
            except Exception as ex:
                oadr3_log_critical(f"exception in event init {ex}")