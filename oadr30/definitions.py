#This file defines all the OpenADR3 definitions and enumerations
from .log import oadr3_log_critical


'''
    The following defined names and types inform a VEN on how to interpret values in an event interval
    payload. The enumerations may be assigned to the payloadType attribute of a payload included in an
    interval included in an event and in an associated payloadDescriptor in the Event or Program.
'''
oadr3_reg_event_types = {
    'SIMPLE': 
    {
        'data_type': float,
        'min': 0,
        'max': 3,
        'desc': "An indication of the level of a basic demand response signal. Payload\
         value is an integer of 0, 1, 2, or 3. Note: An example mapping is normal operations, moderate load shed\
         high load shed, and emergency load shed", 
    },
    'PRICE':
    {
        'data_type': float,
        'desc': "The price of energy. Payload value is a float. Units and currency\
         defined in associated eventPayload'desc'riptor. Note: Can be used for any form of energy"
    },
    'CHARGE_STATE_SETPOINT': 
    {
        'data_type': float,
        'desc': "The state of charge of an energy storage resource. Payload value is\
         indicated by units in associated eventPayload'desc'riptor.\
         Note: Common units are percentage and kWh."
    },
    'DISPATCH_SETPOINT': 
    {
        'data_type': float,
        'desc': "The absolute amount of consumption by a resource. Payload value is\
         a float and is indicated by units in associated eventPayload'desc'riptor.\
         Note: This is used to dispatch resources."
    },
    'DISPATCH_SETPOINT_RELATIVE' :
    { 
        'data_type': float,
        'desc': "The relative change of consumption by a resource. Payload value is a\
         float and is indicated by units in associated eventPayload'desc'riptor.\
         Note: This is used to dispatch a resource\'s load."
    },
    'CONTROL_SETPOINT': 
    {
        'data_type': float,
        'desc': "Resource dependent setting. Payload value type depends on application."
    },
    'EXPORT_PRICE': 
    {
        'data_type': float,
        'desc': "The price of energy exported (usually to the grid). Payload value is\
         float and units and currency are defined in associated\
         eventPayload'desc'riptor. Note: Can be used for any form of energy."
    },
    'GHG': 
    {
        'data_type': float,
        'desc': "An estimate of marginal GreenHouse Gas emissions, in g/kWh.\
         Payload value is float."
    },
    'CURVE' : 
    {
        'data_type': list,  
        'desc': "Payload values array contains a series of one or more pairs of floats\
        representing a 2D point. Note: May be used to represent a curve of values, e.g. VoltVar values."
    },
    'OLS' :
    {
        'data_type': list, 
        'desc': "Optimum Load Shape. Payload values array contains a list of values\
        0.0 to 1.0 representing percentage of usage over the set of intervals in\
        the event.  Note: See ANSI-SCTE 267 "
    },
    'IMPORT_CAPACITY_SUBSCRIPTION' : 
    {
        'data_type': float,
        'desc': "The amount of import capacity a customer has subscribed to in\
        advance. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor."
    },
    'IMPORT_CAPACITY_RESERVATION': 
    {
        'data_type': float,
        'desc': "The amount of additional import capacity that a customer has been\
        granted by the VTN. Payload is a float, and meaning is indicated by\
        units in associated eventPayload'desc'riptor."
    },
    'IMPORT_CAPACITY_RESERVATION_FEE' : 
    {
        'data_type': float,
        'desc': "The cost per unit of power of extra import capacity available for\
        reservation. Payload is a float, and meaning is indicated by units in associated eventPayload'desc'riptor."
    },
    'IMPORT_CAPACITY_AVAILABLE' : 
    {
        'data_type': float, 
        'desc': "The amount of extra import capacity available for reservation to the\
        customer. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor.",
    },
    'IMPORT_CAPACITY_AVAILABLE_PRICE': 
    {
        'data_type': float,
        'desc': "The cost per unit of power of extra import capacity available for\
        reservation. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor."
    },
    'EXPORT_CAPACITY_SUBSCRIPTION':
    {
        'data_type': float,
        'desc': "The amount of export capacity a customer has subscribed to in\
        advance. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor."
    },
    'EXPORT_CAPACITY_RESERVATION':
    {
        'data_type': float,
        'desc': "The amount of additional export capacity that a customer has been\
        granted by the VTN. Payload is a float, and meaning is indicated by\
        units in associated eventPayload'desc'riptor."
    },
    'EXPORT_CAPACITY_RESERVATION_FEE':
    {
        'data_type': float,
        'desc': "The cost per unit of power of extra export capacity available for\
        reservation. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor."
    },
    'EXPORT_CAPACITY_AVAILABLE':
    {
        'data_type': float,
        'desc': "The amount of extra export capacity available for reservation to the\
        customer. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor."
    },
    'EXPORT_CAPACITY_AVAILABLE_PRICE':
    {
        'data_type': float,
        'desc': "The cost per unit of power of extra export capacity available for\
        reservation. Payload is a float, and meaning is indicated by units in\
        associated eventPayload'desc'riptor."
    },
    'IMPORT_CAPACITY_LIMIT':
    {
        'data_type': float,
        'desc': "The 'max'imum import level for the site. Payload is a float and meaning\
        is indicated by units in associated eventPayload'desc'riptor."
    },
    'EXPORT_CAPACITY_LIMIT':
    {
        'data_type': float,
        'desc': "The 'max'imum export level for the site. Payload is a float and meaning\
        is indicated by units in associated eventPayload'desc'riptor."
    }

}

'''
    Alerts
'''
oadr3_alert_types = {
    'ALERT_GRID_EMERGENCY' : 
    {
        'data_type': str,
        'desc': "There is an im'min'ent risk of the grid failing to continue supplying\
        power to some customers, maintaining operational parameters (e.g.\
        voltage), or ceasing to operate at all. Payload value contains a\
        human-readable string 'desc'ribing the alert."
    },
    'ALERT_BLACK_START':  
    {
        'data_type': str,
        'desc': "The grid is in the process of resu'min'g full operation. Devices should\
        'min'imize electricity use until the event is cleared. Payload value\
        contains a human-readable string 'desc'ribing the alert."
    },
    'ALERT_POSSIBLE_OUTAGE':  
    {
        'data_type': str,
        'desc': "Customers may lose grid power in the co'min'g hours or days.\
        Note: An example of this from California is Public Service Power\
        Shutoffs (usually from fire risk). Payload value contains a\
        human-readable string 'desc'ribing the alert."
    },
    'ALERT_FLEX_ALERT' : 
    {
        'data_type': str,
        'desc': "Power supply will be scarce during the event. Devices should seek to\
        shift load to times before or after the event. Devices that can shed\
        should do so during the event. Payload value contains a\
        human-readable string 'desc'ribing the alert.\
        Note: See: flexalert.org"
    },
    'ALERT_FIRE' : 
    {
        'data_type': str,
        'desc': "There is a substantial risk of fire in the area which could interrupt\
        electricity supply in addition to being a danger to life and property.\
        Payload value contains a human-readable string 'desc'ribing the alert."
    },
    'ALERT_FREEZING' : 
    {
        'data_type': str,
        'desc': "There is (or is forecast to be) temperatures low enough to be of\
        concern. Payload value contains a human-readable string 'desc'ribing\
        the alert."
    },
    'ALERT_WIND' : 
    {
        'data_type': str,
        'desc': "There is (or is forecast to be) wind speeds high enough to be of\
        concern. Includes hurricanes. Payload value contains a human-readable string 'desc'ribing the alert."
    },
    'ALERT_TSUNAMI':  
    {
        'data_type': str,
        'desc': "Tsunami waves expected to hit the coastline. Payload value contains a human-readable string 'desc'ribing the alert."
    },
    'ALERT_AIR_QUALITY':  
    {
        'data_type': str, 
        'desc': "Air quality is or is forecast to be. Payload value contains a human-readable string 'desc'ribing the alert."
    },
    'ALERT_OTHER':  
    {
        'data_type': str ,
        'desc': "{No specific definition. See associated text data element. Payload value\
        contains a human-readable string 'desc'ribing the alert."
    }

}

'''
    CTA 2045
'''
oadr3_cta2045_types = {
    'CTA2045_REBOOT':  
    {
        'data_type': float,
        'min': 0,
        'max': 1,
        'desc':"Pass through for resources that support [CTA-2045B]. Payload value 0\
        = SOFT, 1 = HARD. See [CTA-2045B] for definitions."

    },
    'CTA2045_SET_OVERRIDE_STATUS':
    {
        'data_type': int,
        'min': 0,
        'max': 1,
        'desc':"Pass through CTA-2045 Override status: 0 = No Override, 1 = Override. See [CTA-2045B]."
    }
}

'''
Combination of all events 
'''
oadr3_event_types = oadr3_reg_event_types | oadr3_alert_types | oadr3_cta2045_types

'''
    These labels are qualifiers to report name labels, to indicate the nature of the reported value.
    DIRECT_READ is the default, if the qualifier is absent. Note that these apply to the data source in
    general, not to specific intervals.
'''
oadr3_report_reading_types = {
    'DIRECT_READ':
    {
        'data_type': float,
        'desc': 'Payload values have been determined by direct measurement from a resource.'
    },
    'ESTIMATED':
    {
        'data_type': float,
        'desc': 'Payload value is an estimate where no Direct Read was available for the interval, but sufficient other data exist to make a reasonable estimate.'
    }, 
    'SUMMED':
    {
        'data_type': float,
        'desc': 'Payload value is the sum of multiple data sources.',
    },
    'MEAN': 
    {
        'data_type': float,
        'desc': 'Payload value represents the mean measurements over an interval.',

    },
    'PEAK': 
    {
        'data_type': float,
        'desc': 'Payload value represents the highest measurement over an interval.',

    },
    'FORECAST':
    {
        'data_type': float,
        'desc': 'Payload value is a forecast of future values, not a measurement or estimate of actual data.',
    } ,
    'AVERAGE':
    {

        'desc': 'Payload value represents the average of measurements over an interval.',
        'data_type': float,
    }
}

'''
    These definitions characterize the operating state of a resource under control of a VEN
'''
oadr3_resource_operating_state = {
    'NORMAL':
    {
        'desc':'Resource is operating normally. No Demand Response directives are currently being followed.'
    },
    'ERROR':
    {
        'desc':'Resource has self-reported an error or is not addressable by VEN.'
    },
    'IDLE_NORMAL':
    {
        'desc':'CTA-2045 device “Indicates that no demand response event is in effect and the SGD has no/insignificant energy consumption.”'
    },
    'RUNNING_NORMAL':
    {
        'desc':'CTA-2045 device “Indicates that no demand response event is in effect and the SGD has significant energy consumption.”'
    },
    'RUNNING_CURTAILED':
    {
        'desc':'CTA-2045 device “Indicates that a curtailment type demand response event is in effect and the SGD has significant energy consumption.”'
    },
    'RUNNING_HEIGHTENED':
    { 
        'desc':'CTA-2045 device “Indicates that a heightened-operation type of demand response event is in effect and the SGD has significant energy consumption.”'
    },
    'IDLE_CURTAILED': 
    {
        'desc':'CTA-2045 device “Indicates that a curtailment type demand response event is in effect and the SGD has no/insignificant energy consumption.”'
    },
    'SGD_ERROR_CONDITION':
    {
        'desc':'CTA-2045 device “Indicates that the SGD is not operating because it needs maintenance support or is in some way disabled (i.e. no response to the grid).”'
    } ,
    'IDLE_HEIGHTENED':
    {
        'desc':'CTA-2045 device “Indicates that a heightened-operation type of demand response event is in effect and the SGD has no/insignificant energy consumption.”'
    } ,
    'IDLE_OPTED_OUT':
    {
        'desc':'CTA-2045 device “Indicates that the SGD is presently opted out of any demand response events and the SGD has no/insignificant energy consumption.”'
    },
    'RUNNING_OPTED_OUT':
    {
        'desc':'CTA-2045 device “Indicates that the SGD is presently opted out of any demand response events and the SGD has significant energy consumption.”'
    }
}


'''
    The following enumerations may be assigned to the payloadType attribute of a payload included in an
    interval included in a report.
'''
oadr3_report_types = {
    'READING':
    {
        'data_type':float,
        'desc': 'An instantaneous data point, as from a meter. Same as pulse count. Payload\
            value is a float and units are defined in payloadDescriptor.'
    },
    'USAGE':{ 
        'data_type':float,
        'desc': 'Energy usage over an interval. Payload value is a float and units are defined in payloadDescriptor.'
    },
    'DEMAND':{ 
        'data_type':float,
        'desc': 'DEMAND Power usage for an interval, i.e. Real Power. Payload value is a float, units defined in payloadDescriptor. Reading type indicates MEAN, PEAK,FORECAST'
    },
    'SETPOINT':{ 
        'data_type':float,
        'desc': 'Current control setpoint of a resource, see CONTROL_SETPOINT event payloadType above. Payload values are determined by application.'
    },
    'DELTA_USAGE':{ 
        'data_type':float,
        'desc': 'DELTA_USAGE Change in usage as compared to a baseline. Payload value is a float and units are defined in payloadDescriptor.'
    },
    'BASELINE':{ 
        'data_type':any,
        'desc': 'Indicates energy or power consumption in the absence of load control. Payload value is determined by reading type which may indicate usage or demand.'
    },
    'OPERATING_STATE': 
    { 
        'data_type': oadr3_resource_operating_state,
        'desc':'Payload values array includes a list of operating state enumerations, see definitin.'
    },
    'UP_REGULATION_AVAILABLE':
    {
        'data_type': float,
        'desc': 'Up Regulation capacity available for dispatch, in real power. Payload value is a float, units defined in payloadDescriptor. Reading type indicates MEAN, PEAK, FORECAST.'
    },
    'DOWN_REGULATION_AVAILABLE':
    {
        'data_type': float,
        'desc': 'Down Regulation capacity available for dispatch, in real power. Payload value is a float, units defined in payloadDescriptor. Reading type indicates MEAN, PEAK, FORECAST.'
    },
    'REGULATION_SETPOINT':
    {
        'data_type': float,
        'desc': 'Regulation setpoint as instructed as part of regulation services. Payload value is a float, units defined in payloadDescriptor. \
        Reading type indicates MEAN, PEAK, FORECAST.'
    },
    'STORAGE_USABLE_CAPACITY':
    {
        'data_type': float,
        'desc': 'Usable energy that the storage device can hold when fully charged. Payload value is a float, units of energy defined in payloadDescriptor.'
    },
    'STORAGE_CHARGE_LEVEL':
    {
        'data_type': float,
        'desc': 'Current storage charge level expressed as a percentage, where 0% is empty and 100% is full. Payload value is a float, units of PERCENT defined in payloadDescriptor.'
    },
    'STORAGE_MAX_DISCHARGE_POWER':
    {
        'data_type': float,
        'desc': 'The maximum sustainable power that can be discharged into an electricity\
        network (injection). Payload value is a float, units of power defined in\
        payloadDescriptor.'
    },
    'STORAGE_MAX_CHARGE_POWER' :
    {
        'data_type': float, 
        'desc': 'The maximum sustainable power that can be charged from an electricity\
        network (load). Payload value is a float, units of power defined in\
        payloadDescriptor.'
    },
    'SIMPLE_LEVEL':
    { 
        'data_type': float,
        'min': 0,
        'max': 3,
        'desc':'Simple level that a VEN resource is operating at for each Interval. Payload value is an integer 0, 1, 2, 3 corresponding to values in SIMPLE events.'
    },
    'USAGE_FORECAST':
    {
        'data_type': float,
        'desc' : 'Payload values array contains a single float indicating expected resource usage for the associated interval. Units of energy defined in payloadDescriptor.'
    },
    'STORAGE_DISPATCH_FORECAST':
    {
        'data_type': float,
        'desc': 'Payload values array contains a single float indicating expected stored energy that could be dispatched for the associated interval.'
    },
    'LOAD_SHED_DELTA_AVAILABLE':
    {
        'data_type': float,
        'desc': 'Payload values array contains a single float indicating expected increase or decrease in load by a resource for the associated interval.'
    },
    'GENERATION_DELTA_AVAILABLE':
    {
        'data_type': float,
        'desc': 'Payload values array contains a single float indicating expected generation by a resource for the associated interval.'
    },
    'DATA_QUALITY':
    {
        'data_type': float,
        'desc': 'Payload values array contains a string indicating data quality of companion report payload in the same interval. Strings may be one of enumerated Data Quality enumerations.'
    },
    'IMPORT_RESERVATION_CAPACITY':
    {
        'data_type': float,
        'desc': 'Amount of additional import capacity requested. Payload values are a float.'
    },
    'IMPORT_RESERVATION_FEE':
    {
        'data_type': float,
        'desc': 'Amount per unit of import capacity that the VEN is willing to pay for the requested reservation. Payload value is a float with currency defined in payloadDescriptor.'
    },
    'EXPORT_RESERVATION_CAPACITY':
    {
        'data_type': float,
        'desc': 'Amount of additional export capacity requested. Payload values are a float'
    },
    'EXPORT_RESERVATION_FEE':
    {
        'data_type': float,
        'desc': 'Amount per unit of export capacity that the VEN is willing to pay for the requested reservation. Payload value is a float with currency defined in payloadDescriptor.'
    }
}


'''
    No clue what this is!
'''
oadr3_resource_names = {
    'AGGREGATED_REPORT':
    {
        'desc': 'A report contains a list of resources, each of which may contain a list of\
        intervals containing reporting data. Each item in the resource list contains a\
        resourceName attribute. This resourceName indicates the the interval data\
        is the aggregate of data from more than one resource.'
    }
}

'''
    These can be used to qualify report payloads, to indicate the status of individual interval values. These
    are values that may be used in payloads of type DATA_QUALITY.
'''
oadr3_data_quality = {
    'OK': 
    {
        'desc': 'There are no known reasons to doubt the validity of the data.'
    },
    'MISSING': 
    {
        'desc': 'The data item is unavailable for this interval.'
    },
    'ESTIMATED':
    { 
        'desc' : 'This data item has been estimated from other relevant information such as adjacent intervals.'
    },
    'BAD': 
    {
        'desc' : 'There is a data item but it is known or suspected to be erroneous.'
    }
}

'''
    VENs, resources, subscriptions, events and programs may include a targets array, each element defining
    a targeting type and a set of appropriate values. Targeting values may be used to selectively read a
    subset of objects.
'''
oadr3_targets = {
    'POWER_SERVICE_LOCATION':
    {
        'desc': 'A Power Service Location is a utility named specific location in geography or the distribution system, usually the point of service to a customer site.'
    },
    'SERVICE_AREA':
    {
        'desc': 'A Service Area is a utility named geographic region. Target values array contains a string representing a service area name.'
    },
    'GROUP':
    {
        'desc': 'Target values array contains a string representing a group.'
    },
    'RESOURCE_NAME':
    {
        'desc': 'Target values array contains a string representing a resource name.'
    },
    'VEN_NAME': 
    {
        'desc': 'Target values array contains a string representing a VEN name.'
    },
    'EVENT_NAME':
    {
        'desc': 'Target values array contains a string representing an event name.'
    }, 
    'PROGRAM_NAME':
    {
        'desc': 'Target values array contains a string representing a program name'
    } 
}

'''
    VEN and resource representations may include a list of attributes, based on the valueMap object
'''
oadr3_attributes = {
    'LOCATION':
    { 
        'desc': 'Describes a single geographic point. Values[] contains 2 floats, generally\
        representing longitude and latitude. Demand Response programs may define\
        their own use of these fields.'
    },
    'AREA Describes':
    {
        'desc': 'a geographic area. Values[] contains application specific data.\
        Demand Response programs may define their own use of these fields, such\
        as GeoJSON polygon data.'
    },
    'MAX_POWER_CONSU MPTION':
    {
        'desc': 'Values contains a floating point number describing the maximum consumption, in kiloWatts.'
    },
    'MAX_POWER_EXPORT':
    {
        'desc': 'Values contains a floating point number describing the maximum power the device can export, in kiloWatts.'
    },
    'DESCRIPTION':
    {
        'desc': 'Free-form text tersely describing a ven or resource.'
    }
}

'''
    Supported units of measure!
'''
oadr3_units_of_measure = {
    'KWH': 
    {
        'desc': 'kilowatt-hours (kWh)'
    },
    'GHG': 
    {
        'desc': 'Greenhouse gas emissions: g/kWh'
    },
    'VOLTS': 
    {
        'desc': 'volts (V)'
    },
    'AMPS': 
    {
        'desc': 'Current (A)'
    },
    'CELSIUS': 
    {
        'desc': 'Temperature (C)'
    },
    'FAHRENHEIT': 
    {
        'desc': 'Temperature (F)'
    },
    'PERCENT': 
    {
        'desc': '%'
    },
    'KW': 
    {
        'desc': 'kilowatts (kW)'
    },
    'KVAH': 
    {
        'desc': 'kilovolt-ampere hours (kVAh)'
    },
    'KVARH': 
    {
        'desc': 'kilovolt-amperes reactive hours (kVARh)'
    },
    'KVA': 
    {
        'desc': 'kilovolt-amperes (kVA)'
    },
    'KVAR': 
    {
        'desc': 'kilovolt-amperes reactive (kVAR)'
    }
}

def main():
    event = oadr3_reg_event_types['SIMPLE']
    alert = oadr3_alert_types['ALERT_GRID_EMERGENCY']
    cta2045 = oadr3_cta2045_types['CTA2045_SET_OVERRIDE_STATUS']
    print (cta2045)

if __name__ == "__main__":
    main()