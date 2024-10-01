# decode_long_range_broadcast.py -- logic for decoding long range broadcast messages (Message type 27).
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, error_tuple, calculate_longitude, calculate_latitude, calculate_speed_over_ground, calculate_course_over_ground, NAVAID_TYPES

def decode_long_range_broadcast(encodedPayload: str) -> Tuple[Dict, Dict]:
    """
    Function to decode long range broadcast messages (Message type 27)

    Args:
    encodedPayload (str): The binary payload of the AIS message

    Returns:
    Tuple[Dict, Dict] A tuple containing two dictionaries. The first dictionary contains the decoded values, while the second dictionary contains the field names.
    """
    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(encodedPayload, 8, 38)),
            "Position Accuracy": safe_int(get_segment(encodedPayload, 38, 39)),
            "RAIM Flag": safe_int(get_segment(encodedPayload, 39, 40)),
            "Status": safe_int(get_segment(encodedPayload, 40, 44)),
            "Longitude": calculate_longitude(safe_int(get_segment(encodedPayload, 44, 62))),
            "Latitude": calculate_latitude(safe_int(get_segment(encodedPayload, 62, 79))),
            "Speed Over Ground": calculate_speed_over_ground(safe_int(get_segment(encodedPayload, 79, 85))),
            "Course Over Ground": calculate_course_over_ground(safe_int(get_segment(encodedPayload, 85, 94))),
            "GNSS Position Status": safe_int(get_segment(encodedPayload, 94, 95)),
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low" if decoded_data["Position Accuracy"] == 0 else "Missing from AIS message",
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message",
            "Status": NAVAID_TYPES[decoded_data["Status"]] if decoded_data["Status"] in NAVAID_TYPES else "Unknown",
            "Longitude": calculate_longitude(decoded_data["Longitude"]),
            "Latitude": calculate_latitude(decoded_data["Latitude"]),
            "Speed Over Ground": calculate_speed_over_ground(decoded_data["Speed Over Ground"]),
            "Course Over Ground": calculate_course_over_ground(decoded_data["Course Over Ground"]),
            "GNSS Position Status": "Current" if decoded_data["GNSS Position Status"] == 1 else "Outdated" if decoded_data["GNSS Position Status"] == 0 else "Missing from AIS message",
        }
        
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)
