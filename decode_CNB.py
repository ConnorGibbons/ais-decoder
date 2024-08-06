#decode_CNB.py -- logic for decoding Class A Position Reports (Message Types 1, 2, 3)
from typing import Tuple, Dict, Optional, Union
from constants import NAVIGATION_STATUS, safe_int, get_segment

# -- Calculation functions --

# Rate of Turn calculation -- input = 4.733 * sqrt(rateOfTurn).
# Output is the rate of turn in degrees per minute.
def rotCalc(rawRot: Optional[int]) -> Union[int,float]:
    if rawRot == 128 or rawRot is None:
        return -1
    elif rawRot > 126:
        return 127
    elif rawRot < -126:
        return -127
    elif rawRot == 0:
        return rawRot
    elif rawRot > 0 and rawRot <= 126:
        return (rawRot/4.733) ** 2
    elif rawRot < 0 and rawRot >= -126:
        return -((rawRot/4.733) ** 2)

# Speed over ground calculation -- input is sog in 0.1 knot units.
# Output is the speed over ground in knots.
def sogCalc(rawSOG: Optional[int]) -> Union[int,float]:
    if rawSOG == 1023 or rawSOG is None:
        return -1
    else:
        return rawSOG / 10

# Longitude calculation -- input is in 1/600000 minutes.
# Output is the longitude in degrees.
def longitudeCalc(rawLongitude: Optional[int]) -> Union[int,float]:
    if rawLongitude == 181 or rawLongitude is None:
        return -1 # Longitude not available
    else:
        return rawLongitude / 600000

# Latitude calculation -- input is in 1/600000 minutes.
# Output is the latitude in degrees.
def latitudeCalc(rawLatitude : Optional[int]) -> Union[int,float]:
    if rawLatitude == 91 or rawLatitude is None:
        return -1 # Latitude not available
    else:
        return rawLatitude / 600000

# Course over ground calculation -- input is in 0.1 degrees.
# Output is the course over ground in degrees.
def cogCalc(rawCOG: Optional[int]) -> Union[int,float]:
    if rawCOG == 3600 or rawCOG is None:
        return -1 # COG not available
    else:
        return rawCOG / 10

# Heading calculation -- input is in degrees.
# Output is the heading in degrees (just here to check if heading is available).
def headingCalc(rawHeading: Optional[int]) -> int:
    if rawHeading == 511 or rawHeading is None:
        return -1 # Heading not available
    else:
        return rawHeading
    
def timestampCalc(rawTimestamp: Optional[int]) -> int:
    if rawTimestamp == 60 or rawTimestamp is None:
        return -1 # Timestamp not available
    else:
        return rawTimestamp
    
    
# -- String conversion functions -- 

def rotToString(rot: Union[int,float]) -> str:
    if rot > 126:
        return "Turning right at more than 5 degrees per 30 seconds (No turn information available)"
    elif rot < -126:
        return "Turning left at more than 5 degrees per 30 seconds (No turn information available)"
    elif rot == 128 or rot == -1:
        return "Turning information not available"
    elif rot == 0:
        return "Not turning"
    else:
        return "N/A"
    
def timestampToString(timestamp: int) -> str:
    if timestamp == 61:
        return "POS in manual input mode (61)"
    elif timestamp == 62:
        return "POS in dead reckoning mode (62)"
    elif timestamp == 63:
        return "System inoperative (63)"
    else:
        return str(timestamp)

def maneuverIndicatorToString(maneuverIndicator: int) -> str:
    if maneuverIndicator == 0:
        return "Not available"
    elif maneuverIndicator == 1:
        return "No special maneuver"
    elif maneuverIndicator == 2:
        return "Special maneuver"
    else:
        return str(maneuverIndicator)

# Filter function for returning "N/A" if the value is -1
def getVal(val: Union[int,float]) -> Union[int,float,str]:
    if val == -1:
        return "N/A"
    else:
        return val
    

# Decodes a Class A Position Report (Message Types 1, 2, 3)
# Input is the binary payload as a string.
# Output is a tuple containing a dictionary of the decoded values and a dictionary of the stringified values.
def decodeCNB(binaryString: str) -> Tuple[Dict[str,Optional[int]], Dict[str,str]]:
    try:

        CNBDict = {
            "MMSI": safe_int(get_segment(binaryString, 8, 38)),
            "Navigation Status": safe_int(get_segment(binaryString, 38, 42)),
            "Rate of Turn": rotCalc(safe_int(get_segment(binaryString, 42, 50))),
            "SOG": sogCalc(safe_int(get_segment(binaryString, 50, 60))),
            "Position Accuracy": safe_int(get_segment(binaryString, 60, 61)),
            "Longitude": longitudeCalc(safe_int(get_segment(binaryString, 61, 89))),
            "Latitude": latitudeCalc(safe_int(get_segment(binaryString, 89, 116))),
            "COG": cogCalc(safe_int(get_segment(binaryString, 116, 128))),
            "True Heading": headingCalc(safe_int(get_segment(binaryString, 128, 137))),
            "Timestamp": safe_int(get_segment(binaryString, 137, 143)),
            "Maneuver Indicator": safe_int(get_segment(binaryString, 143, 145)),
            "Spare": safe_int(get_segment(binaryString, 145, 148)),
            "RAIM Flag": safe_int(get_segment(binaryString, 148, 149)),
            "Radio Status": safe_int(get_segment(binaryString, 149, 168)) # Not adding a stringified verison yet -- resource here: http://www.ialathree.org/iala/pages/AIS/IALATech1.5.pdf
        }
    
        CNBDictStringified = {
            "MMSI": str(CNBDict["MMSI"]) if CNBDict["MMSI"] is not None else "N/A",
            "Navigation Status": NAVIGATION_STATUS[CNBDict["Navigation Status"]] if CNBDict["Navigation Status"] is not None else "N/A",
            "Rate of Turn": rotToString(CNBDict["Rate of Turn"]) if CNBDict["Rate of Turn"] is not None else "N/A",
            "SOG": str(getVal(CNBDict["SOG"])) + " knots" if CNBDict["SOG"] is not None else "N/A",
            "Position Accuracy": "High" if CNBDict["Position Accuracy"] == 1 else "Low",
            "Longitude": str(getVal(CNBDict["Longitude"])) + "°" if CNBDict["Longitude"] is not None else "N/A",
            "Latitude": str(getVal(CNBDict["Latitude"])) + "°" if CNBDict["Latitude"] is not None else "N/A",
            "COG": str(getVal(CNBDict["COG"])) + "°" if CNBDict["COG"] is not None else "N/A",
            "True Heading": str(getVal(CNBDict["True Heading"])) + "°" if CNBDict["True Heading"] is not None else "N/A",
            "Timestamp": timestampToString(getVal(CNBDict["Timestamp"])) + "s" if CNBDict["Timestamp"] is not None else "N/A",
            "Maneuver Indicator": maneuverIndicatorToString(getVal(CNBDict["Maneuver Indicator"])) if CNBDict["Maneuver Indicator"] is not None else "N/A",
            "Spare": str(getVal(CNBDict["Spare"])) if CNBDict["Spare"] is not None else "N/A",
            "RAIM Flag": "In use" if CNBDict["RAIM Flag"] == 1 else "Not in use" if CNBDict["RAIM Flag"] == 0 else "N/A"
        }

    except Exception as e:
        CNBDict = {
            "Error": "Couldn't decode message"
        }
        CNBDictStringified = {
            "Error": "Couldn't decode message"
        }
        print(e)

    return (CNBDict, CNBDictStringified)