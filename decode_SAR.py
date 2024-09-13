# decode_SAR.py -- logic for decoding Standard SAR Aircraft Position Reports (Message Type 9)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, calculate_longitude, calculate_latitude, longitude_to_string, latitude_to_string, speed_over_ground_to_string, calculate_speed_over_ground, calculate_course_over_ground, course_over_ground_to_string, error_tuple

# -- String conversion functions --
def altitude_to_string(altitude: int) -> str:
    if altitude == -1:
        return "Missing from AIS message"
    elif altitude == 4095:
        return "Not available"
    elif altitude == 4094:
        return "Greater than 4094 meters"
    else:
        return f"{altitude} meters"

def decode_SAR(binary_payload: str):
    """
    Decode a Standard SAR Aircraft Position Report (Message Type 9)

    Args:
    binary_payload (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_payload, 8, 38)),
            "Altitude": safe_int(get_segment(binary_payload, 38, 50)),
            "Speed Over Ground": calculate_speed_over_ground(safe_int(get_segment(binary_payload, 50, 60))) * 10,
            "Position Accuracy": safe_int(get_segment(binary_payload, 60, 61)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_payload, 61, 89), signed=True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_payload, 89, 116), signed=True)),
            "Course Over Ground": calculate_course_over_ground(safe_int(get_segment(binary_payload, 116, 128))),
            "Time Stamp": safe_int(get_segment(binary_payload, 128, 134)),
            "Regional Reserved": safe_int(get_segment(binary_payload, 134, 142)),
            "DTE": safe_int(get_segment(binary_payload, 142, 143)),
            "Spare": safe_int(get_segment(binary_payload, 143, 146)),
            "Assigned Mode Flag": safe_int(get_segment(binary_payload, 146, 147)),
            "RAIM Flag": safe_int(get_segment(binary_payload, 147, 148)),
            "Radio Status": safe_int(get_segment(binary_payload, 148, 168))
        }
 
        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Altitude": f"{altitude_to_string(get_val(decoded_data['Altitude']))}",
            "Speed Over Ground": f"{speed_over_ground_to_string(decoded_data['Speed Over Ground'])}",
            "Position Accuracy": "High" if decoded_data["Position Accuracy"] == 1 else "Low",
            "Longitude": f"{longitude_to_string(decoded_data['Longitude'])}",
            "Latitude": f"{latitude_to_string(decoded_data['Latitude'])}",
            "Course Over Ground": f"{course_over_ground_to_string(get_val(decoded_data['Course Over Ground']))}",
            "Time Stamp": f"{get_val(decoded_data['Time Stamp'])}",
            "Regional Reserved": f"{get_val(decoded_data['Regional Reserved'])}",
            "DTE": f"{get_val(decoded_data['DTE'])}",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "Assigned Mode Flag": get_val(decoded_data["Assigned Mode Flag"]),
            "RAIM Flag": "In use" if decoded_data["RAIM Flag"] == 1 else "Not in use" if decoded_data["RAIM Flag"] == 0 else "Missing from AIS message"
        }

    except Exception as e:
        return error_tuple(e)

    return (decoded_data, stringified_data)