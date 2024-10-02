# decode_position_report_class_b_ext.py -- logic for decoding extended class B position reports. (Message type 19)
from typing import Dict, Tuple, List, Optional
from constants import *

def decode_position_report_class_b_ext(binary_string: str):
    """
    Decode an extended class B position report (BPR), message type 19

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values
    """

    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8 , 38)),
            "Spare": safe_int(get_segment(binary_string, 38, 46)),
            "Speed Over Ground": calculate_speed_over_ground(safe_int(get_segment(binary_string, 46, 56))),
            "Position Accuracy": safe_int(get_segment(binary_string, 56, 57)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 57, 85), signed=True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 85, 112), signed=True)),
            "Course Over Ground": calculate_course_over_ground(safe_int(get_segment(binary_string, 112, 124))),
            "True Heading": calculate_heading(safe_int(get_segment(binary_string, 124, 133))),
            "Timestamp": calculate_timestamp(safe_int(get_segment(binary_string, 133, 139))),
            "Spare 2": safe_int(get_segment(binary_string, 139, 143)),
            "Name": bitstring_to_ascii(get_segment(binary_string, 143, 263)).split("@")[0].strip(),
            "Type of Ship and Cargo": safe_int(get_segment(binary_string, 263, 271)),
            "Dimension to Bow": safe_int(get_segment(binary_string, 271, 280)),
            "Dimension to Stern": safe_int(get_segment(binary_string, 280, 289)),
            "Dimension to Port": safe_int(get_segment(binary_string, 289, 295)),
            "Dimension to Starboard": safe_int(get_segment(binary_string, 295, 301)),
            "Position Fix Type": safe_int(get_segment(binary_string, 301, 305)),
            "RAIM Flag": safe_int(get_segment(binary_string, 305, 306)),
            "DTE": safe_int(get_segment(binary_string, 306, 307)),
            "Assigned Mode Flag": safe_int(get_segment(binary_string, 307, 308)),
            "Spare 3": safe_int(get_segment(binary_string, 308, 311)),
        }

        stringified_data = {
            "MMSI": str(get_val(decoded_data["MMSI"])),
            "Spare": str(get_val(decoded_data["Spare"])),
            "Speed Over Ground": speed_over_ground_to_string(get_val(decoded_data["Speed Over Ground"])),
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low",
            "Longitude": longitude_to_string(get_val(decoded_data["Longitude"])),
            "Latitude": latitude_to_string(get_val(decoded_data["Latitude"])),
            "Course Over Ground": course_over_ground_to_string(get_val(decoded_data["Course Over Ground"])),
            "True Heading": heading_to_string(get_val(decoded_data["True Heading"])),
            "Timestamp": timestamp_to_string(get_val(decoded_data["Timestamp"])),
            "Spare 2": str(get_val(decoded_data["Spare 2"])),
            "Name": str(decoded_data["Name"]),
            "Type of Ship and Cargo": SHIP_TYPE[decoded_data["Type of Ship and Cargo"]] if decoded_data["Type of Ship and Cargo"] in SHIP_TYPE else "Unknown",
            "Dimension to Bow": str(get_val(decoded_data["Dimension to Bow"])),
            "Dimension to Stern": str(get_val(decoded_data["Dimension to Stern"])),
            "Dimension to Port": str(get_val(decoded_data["Dimension to Port"])),
            "Dimension to Starboard": str(get_val(decoded_data["Dimension to Starboard"])),
            "Position Fix Type": EFIX_TYPES[decoded_data["Position Fix Type"]] if decoded_data["Position Fix Type"] in EFIX_TYPES else "Unknown",
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message",
            "DTE": "Ready" if decoded_data["DTE"] == 0 else "Not ready" if decoded_data["DTE"] == 1 else "Missing from AIS message",
            "Assigned Mode Flag": "Station operating in autonomous mode" if decoded_data["Assigned Mode Flag"] == 0 else "Station operating in assigned mode" if decoded_data["Assigned Mode Flag"] == 1 else "Missing from AIS message",
            "Spare 3": str(get_val(decoded_data["Spare 3"])),
        }
    
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)