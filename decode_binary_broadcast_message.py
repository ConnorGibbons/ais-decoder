# decode_BBM.py - logic for decoding Binary Broadcast Messages (Message Type 8)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, bitstring_to_ascii, error_tuple

def decode_binary_broadcast_message(binary_payload: str):
    """
    Decode a binary broadcast message (BBM), message type 8

    Args:
    binary_payload (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try: 
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_payload, 8, 38)),
            "Designated Area Code": safe_int(get_segment(binary_payload, 40, 50)),
            "Functional ID": safe_int(get_segment(binary_payload, 50, 56)),
            "Data": bitstring_to_ascii(get_segment(binary_payload, 56, len(binary_payload)))
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Designated Area Code": f"{get_val(decoded_data['Designated Area Code'])}",
            "Functional ID": f"{get_val(decoded_data['Functional ID'])}",
            "Data": f"{decoded_data['Data']}"
        }
    
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)