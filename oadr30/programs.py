#Universal Devices
#MIT License

import json
from .log import Oadr3LoggedException

'''
This class represents an openADR program. 
Mandatory properties are programName and id. The rest seem to be optional and are as follows
        programType: some_string
        country: US
        bindingEvents: false
        programLongName: Residential Time of Use-A
        timeZoneOffset: PT1H
        createdDateTime: 2023-06-15T09:30:00Z
        modificationDateTime: null
        targets:
        - values:
          - 0.17
          type: PRICE
        - values:
          - 0.17
          type: PRICE
        objectType: PROGRAM
        payloadDescriptors:
        - ""
        - ""
        principalSubdivision: CO
        retailerName: ACME
        programDescriptions:
        - URL: www.myCorporation.com/myProgramDescription
        - URL: www.myCorporation.com/myProgramDescription
        intervalPeriod:
          duration: null
          randomizeStart: null
          start: null
        localPrice: false
        retailerLongName: ACME Electric Inc.
'''
class Program(dict):

    '''
      Initialize using the json received from the VTN
    '''
    def __init__(self, json_data:str):
      try:
        super().__init__(json_data)
      except Exception as ex:
        raise Oadr3LoggedException("exception in Program Init-json", True)
    
    def getId(self):
      try:
        return self['id']
      except Exception as ex:
        return None
      

    def toJson(self)->str:
        return json.dumps(self)

'''
An array of programs
'''
class Programs(list):

  def __init__(self, json_data:str):
    try:
      for program in json_data:
        super().append(Program(program))

    except Exception as ex:
       raise Oadr3LoggedException('critical', "exception in Programs Init", True)
  
  def num_programs(self):
    return len(self)

