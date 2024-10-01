# decode_multi_slot_binary_message.py -- logic for decoding multi slot binary messages (Message type 26)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, error_tuple

def decode_multi_slot_binary_message(encodedPayload: str) -> Tuple[Dict, Dict]:
    """
    Function to decode multi slot binary messages (Message type 26)
    
    Args:
    encodedPayload (str): The binary payload of the AIS message

    Returns:
    Tuple[Dict, Dict] A tuple containing two dictionaries. The first dictionary contains the decoded values, while the second dictionary contains the field names.
    """

    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(encodedPayload, 8, 38)),
            "Addressed": safe_int(get_segment(encodedPayload, 38, 39)),
            "Structured": safe_int(get_segment(encodedPayload, 39, 40)),
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Addressed": "True" if decoded_data["Addressed"] == 1 else "False",
            "Structured": "True" if decoded_data["Structured"] == 1 else "False",
        }
    
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)