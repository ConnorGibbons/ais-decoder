# decode_ATN.py -- Logic for decoding Aid-to-Navigation messages (message type 21)
from typing import Dict, Tuple, Optional
from constants import *

def decode_ATN(binary_string: str):
    """
    Decode Aid-to-Navigation (message type 21)

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Aid Type": safe_int(get_segment(binary_string, 38, 43)),
            "Name": bitstring_to_ascii(get_segment(binary_string, 43, 163)).split("@")[0].strip(),
            "Position Accuracy": safe_int(get_segment(binary_string, 163, 164)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 164, 192), signed=True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 192, 219), signed=True)),
            "Dimension to Bow": safe_int(get_segment(binary_string, 219, 228)),
            "Dimension to Stern": safe_int(get_segment(binary_string, 228, 237)),
            "Dimension to Port": safe_int(get_segment(binary_string, 237, 243)),
            "Dimension to Starboard": safe_int(get_segment(binary_string, 243, 249)),
            "Position Fix Type": safe_int(get_segment(binary_string, 249, 253)),
            "UTC Second": calculate_timestamp(safe_int(get_segment(binary_string, 253, 259))),
            "Off Position Indicator": safe_int(get_segment(binary_string, 259, 260)),
            "Spare": safe_int(get_segment(binary_string, 260, 268)),
            "RAIM Flag": safe_int(get_segment(binary_string, 268, 269)),
            "Virtual Aid Flag": safe_int(get_segment(binary_string, 269, 270)),
            "Assigned Mode Flag": safe_int(get_segment(binary_string, 270, 271)),
            "Spare 2": safe_int(get_segment(binary_string, 271, 272)),
            "Name Extension": bitstring_to_ascii(get_segment(binary_string, 272, len(binary_string))).split("@")[0].strip()
        }

        stringified_data = {
            "MMSI": str(get_val(decoded_data["MMSI"])),
            "Aid Type": NAVAID_TYPES[decoded_data["Aid Type"]] if decoded_data["Aid Type"] in NAVAID_TYPES else "Unknown",
            "Name": str(decoded_data["Name"]),
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low",
            "Longitude": longitude_to_string(get_val(decoded_data["Longitude"])),
            "Latitude": latitude_to_string(get_val(decoded_data["Latitude"])),
            "Dimension to Bow": f"{get_val(decoded_data['Dimension to Bow'])} m",
            "Dimension to Stern": f"{get_val(decoded_data['Dimension to Stern'])} m",
            "Dimension to Port": f"{get_val(decoded_data['Dimension to Port'])} m",
            "Dimension to Starboard": f"{get_val(decoded_data['Dimension to Starboard'])} m",
            "Position Fix Type": EFIX_TYPES[decoded_data["Position Fix Type"]] if decoded_data["Position Fix Type"] in EFIX_TYPES else "Unknown",
            "UTC Second": timestamp_to_string(get_val(decoded_data["UTC Second"])),
            "Off Position Indicator": "Yes" if decoded_data["Off Position Indicator"] == 1 else "No",
            "Spare": str(get_val(decoded_data["Spare"])),
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message",
            "Virtual Aid Flag": "Yes" if decoded_data["Virtual Aid Flag"] == 1 else "No",
            "Assigned Mode Flag": "Station operating in autonomous mode" if decoded_data["Assigned Mode Flag"] == 0 else "Station operating in assigned mode" if decoded_data["Assigned Mode Flag"] == 1 else "Missing from AIS message",
            "Spare 2": str(get_val(decoded_data["Spare 2"])),
            "Name Extension": str(decoded_data["Name Extension"])
        }

    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)

