# decode_CNB.py -- logic for decoding Class A Position Reports (Message Types 1, 2, 3)
from typing import Tuple, Dict, Optional, Union
from constants import NAVIGATION_STATUS, safe_int, get_segment, get_val, calculate_longitude, calculate_latitude, longitude_to_string, latitude_to_string, speed_over_ground_to_string, calculate_course_over_ground, calculate_speed_over_ground, course_over_ground_to_string, error_tuple


# -- Calculation functions --

def calculate_rate_of_turn(raw_rot: Optional[int]) -> Union[int, float]:
    """Calculate rate of turn in degrees per minute."""
    if raw_rot is None:
        return -1
    elif raw_rot in (128, 0):
        return raw_rot
    elif raw_rot > 126:
        return 127
    elif raw_rot < -126:
        return -127
    elif 0 < raw_rot <= 126:
        return (raw_rot / 4.733) ** 2
    elif -126 <= raw_rot < 0:
        return -((raw_rot / 4.733) ** 2)

def calculate_heading(raw_heading: Optional[int]) -> int:
    """Calculate heading in degrees."""
    if raw_heading is None:
        return -1
    else:
        return raw_heading

def calculate_timestamp(raw_timestamp: Optional[int]) -> int:
    """Calculate timestamp in seconds."""
    if raw_timestamp is None:
        return -1
    else:
        return raw_timestamp


# -- String conversion functions --

def rate_of_turn_to_string(rot: Union[int, float]) -> str:
    if rot == -1:
        return "Missing from AIS message"
    elif rot > 126:
        return "Turning right at more than 5 degrees per 30 seconds (Exact rate unavailable)"
    elif rot < -126:
        return "Turning left at more than 5 degrees per 30 seconds (Exact rate unavailable)"
    elif rot == 128:
        return "Turning information not available"
    elif rot == 0:
        return "Not turning"
    else:
        return f"{rot}° per minute"
        
    
def heading_to_string(heading: int) -> str:
    if heading == -1:
        return "Missing from AIS message"
    elif heading == 511:
        return "Not available"
    else:
        return f"{heading}°"

def timestamp_to_string(timestamp: int) -> str:
    if timestamp == -1:
        return "Missing from AIS message"
    elif timestamp == 60:
        return "Timestamp unvailable"
    elif timestamp == 61:
        return "POS in manual input mode"
    elif timestamp == 62:
        return "POS in dead reckoning mode"
    elif timestamp == 63:
        return "System inoperative"
    else:
        return f"{str(timestamp)}s"

def maneuver_indicator_to_string(maneuver_indicator: int) -> str:
    if maneuver_indicator == -1:
        return "Missing from AIS message"
    elif maneuver_indicator == 0:
        return "Not available"
    elif maneuver_indicator == 1:
        return "No special maneuver"
    elif maneuver_indicator == 2:
        return "Special maneuver"
    else:
        return str(maneuver_indicator)




def decode_CNB(binary_string: str) -> Tuple[Dict[str, Optional[int]], Dict[str, str]]:
    """
    Decode a Class A Position Report (Message Types 1, 2, 3).
    
    Args:
    binary_string (str): The binary payload as a string.
    
    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values
    and a dictionary of the stringified values.
    """
    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Navigation Status": safe_int(get_segment(binary_string, 38, 42)),
            "Rate of Turn": calculate_rate_of_turn(safe_int(get_segment(binary_string, 42, 50), signed = True)),
            "Speed Over Ground": calculate_speed_over_ground(safe_int(get_segment(binary_string, 50, 60))),
            "Position Accuracy": safe_int(get_segment(binary_string, 60, 61)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 61, 89), signed = True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 89, 116), signed = True)),
            "Course Over Ground": calculate_course_over_ground(safe_int(get_segment(binary_string, 116, 128))),
            "True Heading": calculate_heading(safe_int(get_segment(binary_string, 128, 137))),
            "Timestamp": safe_int(get_segment(binary_string, 137, 143)),
            "Maneuver Indicator": safe_int(get_segment(binary_string, 143, 145)),
            "Spare": safe_int(get_segment(binary_string, 145, 148)),
            "RAIM Flag": safe_int(get_segment(binary_string, 148, 149)),
            "Radio Status": safe_int(get_segment(binary_string, 149, 168))
        }

        stringified_data = {
            "MMSI": str(get_val(decoded_data["MMSI"])),
            "Navigation Status": NAVIGATION_STATUS[decoded_data["Navigation Status"]] if decoded_data["Navigation Status"] != -1 else "N/A",
            "Rate of Turn": rate_of_turn_to_string(decoded_data["Rate of Turn"]),
            "Speed Over Ground": speed_over_ground_to_string(decoded_data["Speed Over Ground"]),
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low",
            "Longitude": f"{longitude_to_string(decoded_data['Longitude'])}",
            "Latitude": f"{latitude_to_string(decoded_data['Latitude'])}",
            "Course Over Ground": f"{course_over_ground_to_string(get_val(decoded_data['Course Over Ground']))}",
            "True Heading": f"{heading_to_string(get_val(decoded_data['True Heading']))}",
            "Timestamp": f"{timestamp_to_string(get_val(decoded_data['Timestamp']))}",
            "Maneuver Indicator": maneuver_indicator_to_string(get_val(decoded_data["Maneuver Indicator"])),
            "Spare": str(get_val(decoded_data["Spare"])),
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message"
        }

    except Exception as e:
        return error_tuple(e)

    return (decoded_data, stringified_data)