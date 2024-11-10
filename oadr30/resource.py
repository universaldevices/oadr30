#Universal Devices
#MIT License
import json
from .log import Oadr3LoggedException, oadr3_log_critical
from .config import OADR3Config
from .definitions import oadr3_report_types, oadr3_report_reading_types


'''
      This class defines a resource:
      resource:
      type: object
      description: |
        A resource is an energy device or system subject to control by a VEN.
      required:
        - resourceName
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
          description: Used as discriminator.
          enum: [RESOURCE]
          # VTN provisioned on object creation.
        resourceName:
          type: string
          description: |
            User generated identifier, resource may be configured with identifier out-of-band.
            resourceName is expected to be unique within the scope of the associated VEN.
          minLength: 1
          maxLength: 128
          example: RESOURCE-999
        venID:
          $ref: '#/components/schemas/objectID'
          # VTN provisioned on object creation based on path, e.g. POST <>/ven/{venID}/resources.
        attributes:
          type: array
          description: A list of valuesMap objects describing attributes.
          items:
            $ref: '#/components/schemas/valuesMap'
          nullable: true
          default: null
        targets:
          type: array
          description: A list of valuesMap objects describing target criteria.
          items:
            $ref: '#/components/schemas/valuesMap'
          nullable: true
          default: null
'''

class Resource(dict):
    def __init__(self, json_data = None, name = None):
      try:
        if json_data:
          super().__init__(json_data)
        else:
          self.setName(name if name else OADR3Config.default_system_resource_name)
      except Exception as ex:
        raise Oadr3LoggedException('critical', "exception in Resource Init-json", True)

    def setName(self, name:str):
      if not name:
        return
      self['resourceName']=name

    def getReportPayload(self, programId, eventId, venName=OADR3Config.default_client_name ):
      try:
        resourceName=self['resourceName']
        return json.dumps({
          "programID": f"{programId}",
          "eventID": f"{eventId}",
          "clientName": f"{venName}",
          "resources": [
              {
                  "resourceName": f"{resourceName}",
                  "intervals": [
                      {
                          "id": 0,
                          "payloads": [
                              {
                                  "type": f"{OADR3Config.default_system_resource_type}",
                                  "values": [
                                      "NORMAL"
                                  ]
                              }
                          ]
                      }
                  ]
              }
          ]
        })
      except Exception as ex:
        oadr3_log_critical("couldn't create report payload")
        return None



