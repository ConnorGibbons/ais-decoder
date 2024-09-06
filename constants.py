from typing import Optional, Union, List, Dict, Any


# -- Constants --

"""EFIX Types List (in order of EFIX type number)"""
"""EFIX = Electronic Fixing Device, this describes which GNSS system the device uses"""
EFIX_TYPES: List[str] = [
    "Undefined",
    "GPS",
    "GLONASS",
    "Combined GPS/GLONASS",
    "Loran-C",
    "Chayka",
    "Integrated Navigation System",
    "Surveyed",
    "Galileo",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Internal GNSS"
]

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
            print("Error:", e)
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
    return "".join(map(BINARY_ASCII_LOOKUP.get, [bitstring[i:i+6] for i in range(0, len(bitstring), 6)]))    