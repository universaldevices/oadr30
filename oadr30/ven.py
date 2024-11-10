#Universal Devices
#MIT License
import json
from .log import Oadr3LoggedException, oadr3_log_critical
from .descriptors import EventPayloadDescriptor, ReportPayloadDescriptor
from .interval import Interval
from .config import OADR3Config
from .resource import Resource

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
    def __init__(self, json_data):
      try:
        super().__init__(json_data)
      except Exception as ex:
        raise Oadr3LoggedException('critical', "exception in VEN Init-json", True)
    
    def toJson(self)->str:
        return json.dumps(self)

    def save(self)->bool:
      try:
        with open(OADR3Config.ven_persistence_file, 'w') as file:
          json.dump(self, file)
          return True
      except Exception as ex:
        oadr3_log_critical("failed saving ven ...")
        return False

    def getResources(self):
      try:
        out = []
        resources = self['resources']
        if resources:
          for resource in resources:
            out.append(Resource(resource))
        return out
      except Exception as ex:
        oadr3_log_critical("failed getting resources ...")
        return None

    @staticmethod
    def create_ven_request_payload(name:str=None, attributes:list=None, resources:list=None, targets:list=None):
      if not name:
        name=OADR3Config.default_ven_name

      body = f'"venName": "{name}"'
      if attributes:
          jatt=json.dumps(attributes)
          body = f'{body},"attributes":{jatt}'
      if resources:
          jres=json.dumps(resources)
          body = f'{body},"resources":{jres}'
      if targets:
          jtar=json.dumps(targets)
          body = f'{body},"targets":{jtar}'
      
      return f'{{{body}}}'

    @staticmethod
    def restore_ven():
      '''
        return a ven if one exists, otherwise, return None 
      '''
      try:
        with open(OADR3Config.ven_persistence_file, 'r') as file:
          ven = json.load(file)
          return VEN(ven)
      except Exception as ex:
        return None


