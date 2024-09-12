from typing import Optional, Union, List, Dict, Any


# -- Constants --

"""EFIX Types List (in order of EFIX type number)"""
"""EFIX = Electronic Fixing Device, this describes which GNSS system the device uses"""
EFIX_TYPES: Dict[int,str] = {
    0: "Undefined",
    1: "GPS",
    2: "GLONASS",
    3: "Combined GPS/GLONASS",
    4: "Loran-C",
    5: "Chayka",
    6: "Integrated Navigation System",
    7: "Surveyed",
    8: "Galileo",
    **{i: "Unknown" for i in range(9, 15)},
    15: "Internal GNSS"
}

"""Message Types List (in order of message type number)"""
MESSAGE_TYPES: List[str] = [
    "Position Report Class A", # -- Supported
    "Position Report Class A (Assigned schedule)", # -- Supported
    "Position Report Class A (Response to interrogation)", # -- Supported
    "Base Station Report", 
    "Static and Voyage Related Data",
    "Binary Addressed Message",
    "Binary Acknowledge",
    "Binary Broadcast Message",
    "Standard SAR Aircraft Position Report",
    "UTC and Date Inquiry",
    "UTC and Date Response",
    "Addressed Safety Related Message",
    "Safety Related Acknowledge",
    "Safety Related Broadcast Message",
    "Interrogation",
    "Assignment Mode Command",
    "DGNSS Binary Broadcast Message",
    "Standard Class B CS Position Report",
    "Extended Class B Equipment",
    "Data Link Management",
    "Aid-to-Navigation Report",
    "Channel Management",
    "Group Assignment Command",
    "Static Data Report",
    "Single Slot Binary Message",
    "Multiple Slot Binary Message",
    "Long Range AIS Broadcast Message"
]

NAVIGATION_STATUS: List[str] = [
    "Under way (Power)",
    "At anchor",
    "Not under command",
    "Restricted maneuverability",
    "Draft Constrained",
    "Moored",
    "Aground",
    "Engaged in fishing",
    "Under way (Sailing)",
    "---", # Reserved for future use
    "---", # Reserved for future use
    "Towing Astern", # Regional use
    "Towing Alongside", # Regional use
    "---", # Reserved for future use
    "AIS-SART is active",
    "Undefined (default)"
]

SHIP_TYPE: Dict[int,str] = {
    0: "Not available (default)",
    **{i: "Reserved for future use" for i in range(1, 20)},
    20: "Wing in ground (WIG)",
    21: "Wing in ground (WIG), Hazardous category A",
    22: "Wing in ground (WIG), Hazardous category B",
    23: "Wing in ground (WIG), Hazardous category C",
    24: "Wing in ground (WIG), Hazardous category D",
    **{i: "Wing in ground (WIG), Reserved for future use" for i in range(25, 30)},
    30: "Fishing",
    31: "Towing",
    32: "Towing: length exceeds 200m or breadth exceeds 25m",
    33: "Dredging or underwater ops",
    34: "Diving ops",
    35: "Military ops",
    36: "Sailing",
    37: "Pleasure Craft",
    38: "Reserved",
    39: "Reserved",
    40: "High speed craft (HSC)",
    41: "High speed craft (HSC), Hazardous category A",
    42: "High speed craft (HSC), Hazardous category B",
    43: "High speed craft (HSC), Hazardous category C",
    44: "High speed craft (HSC), Hazardous category D",
    **{i: "High speed craft (HSC), Reserved for future use" for i in range(45, 49)},
    49: "High speed craft (HSC)",
    50: "Pilot Vessel",
    51: "Search and Rescue vessel",
    52: "Tug",
    53: "Port Tender",
    54: "Anti-pollution equipment",
    55: "Law Enforcement",
    56: "Spare - Local Vessel",
    57: "Spare - Local Vessel",
    58: "Medical Transport",
    59: "Noncombatant ship according to RR Resolution No. 18",
    60: "Passenger",
    61: "Passenger, Hazardous category A",
    62: "Passenger, Hazardous category B",
    63: "Passenger, Hazardous category C",
    64: "Passenger, Hazardous category D",
    **{i: "Passenger, Reserved for future use" for i in range(65, 69)},
    69: "Passenger",
    70: "Cargo",
    71: "Cargo, Hazardous category A",
    72: "Cargo, Hazardous category B",
    73: "Cargo, Hazardous category C",
    74: "Cargo, Hazardous category D",
    **{i: "Cargo, Reserved for future use" for i in range(75, 79)},
    79: "Cargo",
    80: "Tanker",
    81: "Tanker, Hazardous category A",
    82: "Tanker, Hazardous category B",
    83: "Tanker, Hazardous category C",
    84: "Tanker, Hazardous category D",
    **{i: "Tanker, Reserved for future use" for i in range(85, 89)},
    89: "Tanker",
    90: "Other Type",
    91: "Other Type, Hazardous category A",
    92: "Other Type, Hazardous category B",
    93: "Other Type, Hazardous category C",
    94: "Other Type, Hazardous category D",
    **{i: "Other Type, Reserved for future use" for i in range(95, 99)},
    99: "Other Type, no additional information"
}

AIS_TYPES: Dict[int,str] = {
    0: "ITU 1371",
    1: "Future - 1",
    2: "Future - 2",
    3: "Future - 3",
}

MONTHS: Dict[int,str] = {
    0: "N/A",
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

PAYLOAD_BINARY_LOOKUP: Dict[str, str] = {
    chr(i): bin(i - 48 if i - 48 < 40 else i - 56)[2:].zfill(6)
    for i in range(48, 120)  # '0' to 'w' in ASCII
}

BINARY_ASCII_LOOKUP: Dict[str, str] = {
    bin(i)[2:].zfill(6): chr(i + 64 if i < 31  else i )
    for i in range(64)  # 0 to 63
}


# -- Utility Functions --
    
def safe_int(value: Optional[str], base: int = 2, signed: bool = False) -> int:
    if(value is not None):
        try:
            if(signed):
                if(value[0] == "1"):
                    return -(2**(len(value) - 1)) + int(value[1:], base)
                else:
                    return int(value, base)
            else:
                return int(value, base)
        except Exception as e:
            print("Error: ", e)
            return -1
    else:
        return -1

def get_segment(binaryString: str, start: int, end: int) -> Optional[str]:
    return binaryString[start:end] if len(binaryString) >= end else None

def get_val(val: Any) -> Union[str, Any]:
    """Filter function for returning "N/A" if the value is -1"""
    if val == -1:
        return "N/A"
    else:
        return val


# -- Calculation Functions -- 

def calculate_longitude(rawLongitude: Optional[str]) -> Union[int, float]:
    """Longitude calculation -- input is in 1/600000 minutes."""
    if rawLongitude is None:
        return -1  
    else:
        return rawLongitude / 600000

def calculate_latitude(rawLatitude: Optional[int]) -> Union[int, float]:
    """Latitude calculation -- input is in 1/600000 minutes."""
    if rawLatitude is None:
        return -1 
    else:
        return rawLatitude / 600000
    
def calculate_speed_over_ground(raw_sog: Optional[int]) -> Union[int, float]:
    """Calculate speed over ground in knots."""
    if raw_sog is None:
        return -1
    elif raw_sog in (1023, 1022):
        return raw_sog
    else:
        return raw_sog / 10

def calculate_course_over_ground(raw_cog: Optional[int]) -> Union[int, float]:
    """Calculate course over ground in degrees."""
    if raw_cog is None:
        return -1
    elif raw_cog == 3600:
        return 3600
    else:
        return raw_cog / 10


# -- String Conversion Functions -- 

def longitude_to_string(longitude: Union[int, float]) -> str:
    if longitude == -1:
        return "Missing from AIS message"
    elif longitude == 181:
        return "Position not available"
    else:
        return f"{longitude}°"
    
def latitude_to_string(latitude: Union[int, float]) -> str:
    if latitude == -1:
        return "Missing from AIS message"
    elif latitude == 91:
        return "Position not available"
    else:
        return f"{latitude}°"
    
def bitstring_to_ascii(bitstring: str) -> str:
    if bitstring is None:
        return "Missing from AIS message"
    return "".join(map(lambda x: BINARY_ASCII_LOOKUP.get(x,'') if isinstance(x,str) else '', [bitstring[i:i+6] for i in range(0, len(bitstring), 6)]))    

def speed_over_ground_to_string(sog: Union[int, float]) -> str:
    if sog == -1:
        return "Missing from AIS message"
    elif sog == 1023:
        return "SOG not available."
    elif sog == 1022:
        return "SOG exceeds 102.2 knots."
    else:
        return f"{sog} knots"

def course_over_ground_to_string(cog: Union[int, float]) -> str:
    if cog == -1:
        return "Missing from AIS message"
    elif cog == 3600:
        return "COG not available."
    else:
        return f"{cog}°"
