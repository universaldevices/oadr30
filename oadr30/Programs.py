#Universal Devices
#MIT License

import json

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
        Provide the programName and Id. Optionally, provide additional properties in the form of name: value pairs
    '''
    def __init__(self, programName:str, programId: str, *args, **kwargs):
        if programName == None or programId == None:
            raise Exception("A program needs both programName and ProgramId")
        try:
            # Default elements
            default_elements = {
                'id': programId,
                'programName': programName,
                'country': 'US',
                'programType': 'PRICING_TARIFF',
            }
            
            # Initialize the dict with default elements
            super().__init__(default_elements, *args, **kwargs)
            
            # Update the dict with any additional keyword arguments
            self.update(kwargs)
        except Exception as ex:
            print (str(ex))

    def toJson(self)->str:
        return json.dumps(self)
