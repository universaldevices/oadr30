#Universal Devices
#MIT License
import json
from .log import Oadr3LoggedException, oadr3_log_critical
from .descriptors import EventPayloadDescriptor, ReportPayloadDescriptor
from .interval import Interval



'''
This class represents an openADR ven
event: VEN object to communicate a Demand Response request to VEN.
yaml 3.0.1:
    ven:
      required:
      - venName
      type: object
      properties:
        id:
          $ref: '#/components/schemas/objectID'
        createdDateTime:
          $ref: '#/components/schemas/dateTime'
        modificationDateTime:
          $ref: '#/components/schemas/dateTime'
        objectType:
          type: string
          description: Used as discriminator.
          enum:
          - VEN
        venName:
          maxLength: 128
          minLength: 1
          type: string
          description: |
            User generated identifier, may be VEN identifier provisioned out-of-band.
            venName is expected to be unique within the scope of a VTN
          example: VEN-999
        attributes:
          type: array
          description: A list of valuesMap objects describing attributes.
          nullable: true
          items:
            $ref: '#/components/schemas/valuesMap'
        targets:
          type: array
          description: A list of valuesMap objects describing target criteria.
          nullable: true
          items:
            $ref: '#/components/schemas/valuesMap'
        resources:
          type: array
          description: A list of resource objects representing end-devices or systems.
          nullable: true
          items:
            $ref: '#/components/schemas/resource'
      description: Ven represents a client with the ven role.
      example:
        venName: VEN-999
        createdDateTime: 2023-06-15T09:30:00Z
        resources:
        - venID: null
          createdDateTime: null
          resourceName: RESOURCE-999
          attributes:
          - null
          - null
          id: null
          modificationDateTime: null
          targets:
          - null
          - null
          objectType: RESOURCE
        - venID: null
          createdDateTime: null
          resourceName: RESOURCE-999
          attributes:
          - null
          - null
          id: null
          modificationDateTime: null
          targets:
          - null
          - null
          objectType: RESOURCE
        attributes:
        - values:
          - 0.17
          type: PRICE
        - values:
          - 0.17
          type: PRICE
        id: object-999
        modificationDateTime: null
        targets:
        - null
        - null
        objectType: VEN
'''

class VEN(dict):
    '''
      A class representing a VEN. Initially, a VEN must be created in the VTN. If successful
      the VTN will return a VEN object with an ID.
    '''
    def __init__(self, json_data:str):
      try:
        super().__init__(json_data)
      except Exception as ex:
        raise Oadr3LoggedException('critical', "exception in VEN Init-json", True)

    @staticmethod
    def create_ven_request_payload(name:str, attributes=None, resources=None, targets=None):
      ven = {
        "venName": name
      }

      return ven 

    def toJson(self)->str:
        return json.dumps(self)

class Events(list):
  '''
    An array of events
  '''
  def __init__(self, json_data:str):
    try:
      for event in json_data:
        super().append(Event(event))

    except Exception as ex:
       raise Oadr3LoggedException('critical', "exception in Events Init", True)

  def num_events(self):
    return len(self)
