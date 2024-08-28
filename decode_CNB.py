# decode_class_a_position.py -- logic for decoding Class A Position Reports (Message Types 1, 2, 3)
from typing import Tuple, Dict, Optional, Union
from constants import NAVIGATION_STATUS, safe_int, get_segment, get_val, calculate_longitude, calculate_latitude

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
    if raw_cog == 3600 or raw_cog is None:
        return -1  # COG not available
    else:
        return raw_cog / 10

def calculate_heading(raw_heading: Optional[int]) -> int:
    """Calculate heading in degrees."""
    if raw_heading == 511 or raw_heading is None:
        return -1  # Heading not available
    else:
        return raw_heading

def calculate_timestamp(raw_timestamp: Optional[int]) -> int:
    """Calculate timestamp."""
    if raw_timestamp == 60 or raw_timestamp is None:
        return -1  # Timestamp not available
    else:
        return raw_timestamp

# -- String conversion functions --

def rate_of_turn_to_string(rot: Union[int, float]) -> str:
    """Convert rate of turn to string representation."""
    if rot > 126:
        return "Turning right at more than 5 degrees per 30 seconds (No turn information available)"
    elif rot < -126:
        return "Turning left at more than 5 degrees per 30 seconds (No turn information available)"
    elif rot in (128, -1):
        return "Turning information not available"
    elif rot == 0:
        return "Not turning"
    else:
        return f"{rot}° per minute"

def timestamp_to_string(timestamp: int) -> str:
    """Convert timestamp to string representation."""
    if timestamp == 61:
        return "POS in manual input mode (61)"
    elif timestamp == 62:
        return "POS in dead reckoning mode (62)"
    elif timestamp == 63:
        return "System inoperative (63)"
    elif timestamp == -1:
        return "Missing from AIS message"
    else:
        return str(timestamp)

def maneuver_indicator_to_string(maneuver_indicator: int) -> str:
    """Convert maneuver indicator to string representation."""
    if maneuver_indicator == 0:
        return "Not available"
    elif maneuver_indicator == 1:
        return "No special maneuver"
    elif maneuver_indicator == 2:
        return "Special maneuver"
    elif maneuver_indicator == -1:
        return "Missing from AIS message"
    else:
        return str(maneuver_indicator)

def speed_over_ground_to_string(sog: Union[int, float]) -> str:
    """Convert speed over ground to string representation."""
    if sog == -1:
        return "Missing from AIS message"
    elif sog == 1023:
        return "SOG not available."
    elif sog == 1022:
        return "SOG exceeds 102.2 knots."
    else:
        return f"{sog} knots"

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
            "Rate of Turn": calculate_rate_of_turn(safe_int(get_segment(binary_string, 42, 50), signed=True)),
            "Speed Over Ground": calculate_speed_over_ground(safe_int(get_segment(binary_string, 50, 60))),
            "Position Accuracy": safe_int(get_segment(binary_string, 60, 61)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 61, 89), signed=True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 89, 116), signed=True)),
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
            "Longitude": f"{get_val(decoded_data['Longitude'])}°",
            "Latitude": f"{get_val(decoded_data['Latitude'])}°",
            "Course Over Ground": f"{get_val(decoded_data['Course Over Ground'])}°",
            "True Heading": f"{get_val(decoded_data['True Heading'])}°",
            "Timestamp": f"{timestamp_to_string(get_val(decoded_data['Timestamp']))}s",
            "Maneuver Indicator": maneuver_indicator_to_string(get_val(decoded_data["Maneuver Indicator"])),
            "Spare": str(get_val(decoded_data["Spare"])),
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "N/A"
        }

    except Exception as e:
        decoded_data = {"Error": "Couldn't decode message"}
        stringified_data = {"Error": "Couldn't decode message"}
        print(e)

    return (decoded_data, stringified_data)