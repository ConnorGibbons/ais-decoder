# decode_BPR.py - Logic for decoding class B position reports. (Message type 18)
from typing import Dict, Tuple, List, Optional
from constants import safe_int, get_segment, get_val, error_tuple, calculate_course_over_ground, calculate_latitude, calculate_longitude, calculate_speed_over_ground, calculate_timestamp, calculate_heading, speed_over_ground_to_string, course_over_ground_to_string, heading_to_string, latitude_to_string, longitude_to_string, timestamp_to_string

def decode_BPR(binary_string: str):
    """
    Decode a class B position report (BPR), message type 18

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """
    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Spare": safe_int(get_segment(binary_string, 38, 46)),
            "Speed Over Ground": calculate_speed_over_ground(safe_int(get_segment(binary_string, 46, 56))),
            "Position Accuracy": safe_int(get_segment(binary_string, 56, 57)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 57, 85), signed= True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 85, 112), signed = True)),
            "Course Over Ground": calculate_course_over_ground(safe_int(get_segment(binary_string, 112, 124))),
            "True Heading": calculate_heading(safe_int(get_segment(binary_string, 124, 133))),
            "Timestamp": calculate_timestamp(safe_int(get_segment(binary_string, 133, 139))),
            "Spare 2": safe_int(get_segment(binary_string, 139, 146)),
            "Assigned Mode Flag": safe_int(get_segment(binary_string, 146, 147)),
            "RAIM Flag": safe_int(get_segment(binary_string, 147, 148)),
            "Communication State": safe_int(get_segment(binary_string, 148, 168))
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "Speed Over Ground": f"{speed_over_ground_to_string(get_val(decoded_data['Speed Over Ground']))}",
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low",
            "Longitude": f"{longitude_to_string(get_val(decoded_data['Longitude']))}",
            "Latitude": f"{latitude_to_string(get_val(decoded_data['Latitude']))}",
            "Course Over Ground": f"{course_over_ground_to_string(get_val(decoded_data['Course Over Ground']))}",
            "True Heading": f"{heading_to_string(get_val(decoded_data['True Heading']))}",
            "Timestamp": f"{timestamp_to_string(get_val(decoded_data['Timestamp']))}",
            "Spare 2": f"{get_val(decoded_data['Spare 2'])}",
            "Assigned Mode Flag": "Station operating in autonomous mode" if decoded_data["Assigned Mode Flag"] == 0 else "Station operating in assigned mode" if decoded_data["Assigned Mode Flag"] == 1 else "Missing from AIS message",
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message"
        }
    
    except Exception as e:
        return error_tuple(e)

    return (decoded_data, stringified_data)