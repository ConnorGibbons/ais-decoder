# decode_static_and_voyage_data.py -- logic for decoding Static and Voyage Related Data (Message Type 5)
from typing import Dict, Tuple, Optional
from constants import safe_int, get_segment, get_val, bitstring_to_ascii, EFIX_TYPES, SHIP_TYPE, AIS_TYPES, MONTHS, error_tuple

def decode_static_and_voyage_data(binary_string: str) -> Tuple[Dict[str, Optional[int]], Dict[str, str]]:
    """
    Decode a static and voyage related data (VRD) message, message type 5.
    
    Args:
    binary_string (str): The binary payload as a string.
    fragment_number (int): The fragment number for the message (message type 5 comes in two parts.)
    
    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values
    and a dictionary of the stringified values.
    """
    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "AIS Version": safe_int(get_segment(binary_string, 38, 40)),
            "IMO Number": safe_int(get_segment(binary_string, 40, 70)),
            "Call Sign": bitstring_to_ascii(get_segment(binary_string, 70, 112)).split('@')[0].strip(),
            "Vessel Name": bitstring_to_ascii(get_segment(binary_string, 112, 232)).split('@')[0].strip(),
            "Type of Ship and Cargo": safe_int(get_segment(binary_string, 232, 240)),
            "Dimensions to Bow": safe_int(get_segment(binary_string, 240, 249)),
            "Dimensions to Stern": safe_int(get_segment(binary_string, 249, 258)),
            "Dimensions to Port": safe_int(get_segment(binary_string, 258, 264)),
            "Dimensions to Starboard": safe_int(get_segment(binary_string, 264, 270)),
            "Position Fixing Device": safe_int(get_segment(binary_string, 270, 274)),
            "ETA Month": safe_int(get_segment(binary_string, 274, 278)),
            "ETA Day": safe_int(get_segment(binary_string, 278, 283)),
            "ETA Hour": safe_int(get_segment(binary_string, 283, 288)),
            "ETA Minute": safe_int(get_segment(binary_string, 288, 294)),
            "Draught": safe_int(get_segment(binary_string, 294, 302)) / 10,
            "Destination": bitstring_to_ascii(get_segment(binary_string, 302, 422)).split('@')[0].strip(),
            "Data Terminal Ready": safe_int(get_segment(binary_string, 422, 423)),
            "Spare": safe_int(get_segment(binary_string, 423, 424))
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "AIS Version": f"{AIS_TYPES[decoded_data['AIS Version']] if decoded_data['AIS Version'] in AIS_TYPES else 'Unknown'}",
            "IMO Number": f"{get_val(decoded_data['IMO Number'])}",
            "Call Sign": decoded_data['Call Sign'],
            "Vessel Name": decoded_data['Vessel Name'],
            "Type of Ship and Cargo": f"{SHIP_TYPE[decoded_data['Type of Ship and Cargo']] if decoded_data['Type of Ship and Cargo'] in SHIP_TYPE else 'Unknown'}",
            "Dimensions to Bow": f"{get_val(decoded_data['Dimensions to Bow'])} m",
            "Dimensions to Stern": f"{get_val(decoded_data['Dimensions to Stern'])} m",
            "Dimensions to Port": f"{get_val(decoded_data)['Dimensions to Port']} m",
            "Dimensions to Starboard": f"{get_val(decoded_data)['Dimensions to Starboard']} m",
            "Position Fixing Device": f"{EFIX_TYPES[decoded_data['Position Fixing Device']] if decoded_data['Position Fixing Device'] in EFIX_TYPES else 'Unknown'}",
            "ETA Month": f"{MONTHS[decoded_data['ETA Month']] if decoded_data['ETA Month'] in MONTHS else 'N/A'}",
            "ETA Day": f"{get_val(decoded_data['ETA Day'])}" if decoded_data['ETA Day'] != 0 else 'N/A',
            "ETA Hour": f"{get_val(decoded_data['ETA Hour'])}" if decoded_data['ETA Hour'] != 24 else 'N/A',
            "ETA Minute": f"{get_val(decoded_data['ETA Minute'])}" if decoded_data['ETA Minute'] != 60 else 'N/A',
            "Draught": f"{get_val(decoded_data['Draught'])} m",
            "Destination": f"{decoded_data['Destination']}",
            "Data Terminal Ready": f"{get_val(decoded_data['Data Terminal Ready'])}",
            "Spare": f"{get_val(decoded_data['Spare'])}",
        }
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)

