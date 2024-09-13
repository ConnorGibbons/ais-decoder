# decode_BAD.py -- logic for decoding Binary Addressed Messages (type 6)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, bitstring_to_ascii, error_tuple

def decode_BAD(binary_string: str):
    """
    Decode a binary addressed message (BAD) message
    
    Args:
    binary_string (str): The binary payload as a string.
    
    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values
    and a dictionary of the stringified values.
    """
    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Sequence Number": safe_int(get_segment(binary_string, 38, 40)),
            "Destination MMSI": safe_int(get_segment(binary_string, 40, 70)),
            "Retransmit Flag": safe_int(get_segment(binary_string, 70, 71)),
            "Spare": safe_int(get_segment(binary_string, 71, 72)),
            "Designated Area Code": safe_int(get_segment(binary_string, 72, 82)),
            "Functional ID": safe_int(get_segment(binary_string, 82, 88)),
            "Data": bitstring_to_ascii(get_segment(binary_string, 88, len(binary_string)))
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Sequence Number": f"{get_val(decoded_data['Sequence Number'])}",
            "Destination MMSI": f"{get_val(decoded_data['Destination MMSI'])}",
            "Retransmit Flag": "Retransmitted" if decoded_data["Retransmit Flag"] == 1 else "Initial transmission",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "Designated Area Code": f"{get_val(decoded_data['Designated Area Code'])}",
            "Functional ID": f"{get_val(decoded_data['Functional ID'])}",
            "Data": f"{decoded_data['Data']}"
        }
    
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)