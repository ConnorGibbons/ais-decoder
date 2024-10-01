# decode_BSR.py -- logic for decoding Base Station Reports (Message Type 4)
from typing import Dict, Tuple, Optional, List
from constants import EFIX_TYPES, safe_int, get_segment, get_val, calculate_latitude, calculate_longitude, latitude_to_string, longitude_to_string, error_tuple


def decode_base_station_report(binary_string: str) -> Tuple[Dict[str, Optional[int]], Dict[str, str]]:
    """
    Decode a base station report (BSR) message, message type 4.
    
    Args:
    binary_string (str): The binary payload as a string.
    
    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values
    and a dictionary of the stringified values.
    """
    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Year (UTC)": safe_int(get_segment(binary_string, 38, 52)),
            "Month (UTC)": safe_int(get_segment(binary_string, 52, 56)),
            "Day (UTC)": safe_int(get_segment(binary_string, 56, 61)),
            "Hour (UTC)": safe_int(get_segment(binary_string, 61, 66)),
            "Minute (UTC)": safe_int(get_segment(binary_string, 66, 72)),
            "Second (UTC)": safe_int(get_segment(binary_string, 72, 78)),
            "Position Accuracy": safe_int(get_segment(binary_string, 78, 79)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 79, 107), signed=True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 107, 134), signed=True)),
            "Type of Electronic Position Fixing Device": safe_int(get_segment(binary_string, 134, 138)),
            "Spare": safe_int(get_segment(binary_string, 138, 148)),
            "RAIM Flag": safe_int(get_segment(binary_string, 148, 149)),
            "Radio Status": safe_int(get_segment(binary_string, 149, 168)) # No plan to decode this yet
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Year (UTC)": f"{get_val(decoded_data['Year (UTC)'])}",
            "Month (UTC)": f"{get_val(decoded_data['Month (UTC)'])}",
            "Day (UTC)": f"{get_val(decoded_data['Day (UTC)'])}",
            "Hour (UTC)": f"{get_val(decoded_data['Hour (UTC)'])}",
            "Minute (UTC)": f"{get_val(decoded_data['Minute (UTC)'])}",
            "Second (UTC)": f"{get_val(decoded_data['Second (UTC)'])}",
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low",
            "Longitude": f"{longitude_to_string(decoded_data['Longitude'])}",
            "Latitude": f"{latitude_to_string(decoded_data['Latitude'])}",
            "Type of Electronic Position Fixing Device": f"{EFIX_TYPES[decoded_data['Type of Electronic Position Fixing Device']] if decoded_data['Type of Electronic Position Fixing Device'] in EFIX_TYPES else 'Unknown'}",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message"
        }
    
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)