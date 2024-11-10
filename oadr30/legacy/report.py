#Universal Devices
#MIT License

from common import Interval, IntervalPeriod, validate_string
from log import Oadr3LoggedException 
import json

'''
    This class defines a resource in a report

          items:
            type: object
            description: Report data associated with a resource.
            required:
              - resourceName
              - intervals
            properties:
              resourceName:
                type: string
                minLength: 1
                maxLength: 128
                description: User generated identifier. A value of AGGREGATED_REPORT indicates an aggregation of more that one resource's data
                example: RESOURCE-999
              intervalPeriod:
                $ref: '#/components/schemas/intervalPeriod'
                # Defines default start and durations of intervals.
              intervals:
                type: array
                description: A list of interval objects.
                items:
                  $ref: '#/components/schemas/interval'

'''
class ReportResource():

  def __init__(self, resourceName:str, intervals:[Interval]):

    if not validate_string(resourceName, 128):
      raise Oadr3LoggedException('critical', 'resource name is mandatory with a length of less than 128 ...', True)

    self.resourceName = resourceName
    self.intervalPeriod:IntervalPeriod = None 
    if intervals == None:
      intervals = []


'''
    This class represents oadr3 report
    report:
      type: object
      description: report object.
      required:
        - programID
        - eventID
        - clientName
        - resources
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
          enum: [REPORT]
          # VTN provisioned on object creation.
        programID:
          $ref: '#/components/schemas/objectID'
          # ID attribute of program object this report is associated with.
        eventID:
          $ref: '#/components/schemas/objectID'
          # ID attribute of event object this report is associated with.
        clientName:
          type: string
          description: User generated identifier; may be VEN ID provisioned out-of-band.
          minLength: 1
          maxLength: 128
          example: VEN-999
        reportName:
          type: string
          description: User defined string for use in debugging or User Interface.
          example: Battery_usage_04112023
          nullable: true
          default: null
        payloadDescriptors:
          type: array
          description: A list of reportPayloadDescriptors.
          items:
            $ref: '#/components/schemas/reportPayloadDescriptor'
          nullable: true
          default: null
          # An optional list of objects that provide context to payload types.
        resources:
          type: array
          description: A list of objects containing report data for a set of resources.
          items:
            type: object
            description: Report data associated with a resource.
            required:
              - resourceName
              - intervals
            properties:
              resourceName:
                type: string
                minLength: 1
                maxLength: 128
                description: User generated identifier. A value of AGGREGATED_REPORT indicates an aggregation of more that one resource's data
                example: RESOURCE-999
              intervalPeriod:
                $ref: '#/components/schemas/intervalPeriod'
                # Defines default start and durations of intervals.
              intervals:
                type: array
                description: A list of interval objects.
                items:
                  $ref: '#/components/schemas/interval'

'''

class Report(dict):
    '''
        Provide required elements below. Optionally, provide additional properties in the form of name: value pairs
        - programID
        - eventID
        - clientName
        - resources
    '''
    def __init__(self, programId: str, eventId: str, clientName: str, resources: [ReportResource], *args, **kwargs):
        if programId == None or eventId == None or clientName == None or resource == None:
            raise Oadr3LoggedException('critical', 'programId, eventId, clientName, and resources are all mandatory ...', True)
        try:
            # Default elements
            default_elements = {
                'programID': programId,
                'eventID': eventId,
                'clientName': clientName,
                'resources': resources 
            }
            
            # Initialize the dict with default elements
            super().__init__(default_elements, *args, **kwargs)
            
            # Update the dict with any additional keyword arguments
            self.update(kwargs)
        except Exception as ex:
            raise Oadr3LoggedException('critical', f"exception in Report init {ex}", True)

    def toJson(self)->str:
        return json.dumps(self)
