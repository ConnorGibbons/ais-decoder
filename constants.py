from typing import Optional, Union, List, Dict, Any
import traceback
# Message Types List (in order of message type number)
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

# Navigation Status List
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
            print("Erorr:", e)
            return -1
    else:
        return -1

def get_segment(binaryString: str, start: int, end: int) -> Optional[str]:
    return binaryString[start:end] if len(binaryString) >= end else None

# Filter function for returning "N/A" if the value is -1
def get_val(val: Any) -> Union[str, Any]:
    if val == -1:
        return "N/A"
    else:
        return val

# -- Calculation Functions -- For properties shared by multiple message types

def longitudeCalc(rawLongitude: Optional[str]) -> Union[int, float]:
    if rawLongitude is None or rawLongitude == "1" * 28:  # All 1s represent unavailable
        return -1  # Longitude not available
    else:
        return rawLongitude / 600000

# Latitude calculation -- input is in 1/600000 minutes.
# Output is the latitude in degrees.
def latitudeCalc(rawLatitude: Optional[int]) -> Union[int, float]:
    if rawLatitude == 91 or rawLatitude is None:
        return -1 # Latitude not available
    else:
        return rawLatitude / 600000