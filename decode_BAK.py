# decode_BAK.py -- logic for decoding Binary Acknowledge Messages (type 7)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val

def decode_BAK(binary_string: str):
    """
    Decode a binary acknowledge message (BAK) message, type 7

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try: 
        decoded_data = {
            "Source MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Spare": safe_int(get_segment(binary_string, 38, 40)),
            "MMSI 1": safe_int(get_segment(binary_string, 40, 70)),
            "Sequence Number 1": safe_int(get_segment(binary_string, 70, 72)),
            "MMSI 2": safe_int(get_segment(binary_string, 72, 102)),
            "Sequence Number 2": safe_int(get_segment(binary_string, 102, 104)),
            "MMSI 3": safe_int(get_segment(binary_string, 104, 134)),
            "Sequence Number 3": safe_int(get_segment(binary_string, 134, 136)),
            "MMSI 4": safe_int(get_segment(binary_string, 136, 166)),
            "Sequence Number 4": safe_int(get_segment(binary_string, 166, 168)),
        }

        stringified_data = {
            "Source MMSI": f"{get_val(decoded_data['Source MMSI'])}",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "MMSI 1": f"{get_val(decoded_data['MMSI 1'])}",
            "Sequence Number 1": f"{get_val(decoded_data['Sequence Number 1'])}",
            "MMSI 2": f"{get_val(decoded_data['MMSI 2'])}",
            "Sequence Number 2": f"{get_val(decoded_data['Sequence Number 2'])}",
            "MMSI 3": f"{get_val(decoded_data['MMSI 3'])}",
            "Sequence Number 3": f"{get_val(decoded_data['Sequence Number 3'])}",
            "MMSI 4": f"{get_val(decoded_data['MMSI 4'])}",
            "Sequence Number 4": f"{get_val(decoded_data['Sequence Number 4'])}",
        }

    except Exception as e:
        decoded_data = {
            "Error": "Couldn't decode message"
        }
        stringified_data = {
            "Error": "Couldn't decode message"
        }
        print(e)
    
    return (decoded_data, stringified_data)