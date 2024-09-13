# decode_SRM.py - logic for decoding Addressed Safety-Related Messages (Message Type 14)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, bitstring_to_ascii, error_tuple

def decode_SRM(binary_payload: str):
    """
    Decode an addressed safety-related message (SRM), message type 14

    Args:
    binary_payload (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_payload, 8, 38)),
            "Sequence Number": safe_int(get_segment(binary_payload, 38, 40)),
            "Destination MMSI": safe_int(get_segment(binary_payload, 40, 70)),
            "Retransmit Flag": safe_int(get_segment(binary_payload, 70, 71)),
            "Spare": safe_int(get_segment(binary_payload, 71, 72)),
            "Text": bitstring_to_ascii(get_segment(binary_payload, 72, len(binary_payload)))
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Sequence Number": f"{get_val(decoded_data['Sequence Number'])}",
            "Destination MMSI": f"{get_val(decoded_data['Destination MMSI'])}",
            "Retransmit Flag": "Retransmitted" if decoded_data["Retransmit Flag"] == 1 else "Initial transmission",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "Text": f"{decoded_data['Text']}"
        }

    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)
        

