# decode_interrogation.py - decode interrogations (message type 15)
from constants import *
from typing import Dict, Tuple, Optional
def decode_interrogation(binary_string: str):
    """
    Decode Interrogation (message type 15)

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try:
        decoded_data: Dict[str, int] = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Spare": safe_int(get_segment(binary_string, 38, 40)),
            "Interrogated MMSI 1": safe_int(get_segment(binary_string, 40, 70)),
            "Message Type 1": safe_int(get_segment(binary_string, 70, 76)),
            "Slot Offset 1": safe_int(get_segment(binary_string, 76, 88)),
            "Spare 2": safe_int(get_segment(binary_string, 88, 90)),
            "Message Type 2": safe_int(get_segment(binary_string, 90, 96)),
            "Slot Offset 2": safe_int(get_segment(binary_string, 96, 108)),
            "Spare 3": safe_int(get_segment(binary_string, 108, 110)),
            "Interrogated MMSI 2": safe_int(get_segment(binary_string, 110, 140)),
            "Message Type 3": safe_int(get_segment(binary_string, 140, 146)),
            "Slot Offset 3": safe_int(get_segment(binary_string, 146, 158)),
            "Spare 4": safe_int(get_segment(binary_string, 158, 160)),
        }

        stringified_data: Dict[str, str] = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Interrogated MMSI": f"{get_val(decoded_data['Interrogated MMSI'])}",
            "Message Type 1": f"{get_val(decoded_data['Message Type 1'])}",
            "Slot Offset 1": f"{get_val(decoded_data['Slot Offset 1'])}",
            "Message Type 2": f"{get_val(decoded_data['Message Type 2'])}",
            "Slot Offset 2": f"{get_val(decoded_data['Slot Offset 2'])}",
            "Message Type 3": f"{get_val(decoded_data['Message Type 3'])}",
            "Slot Offset 3": f"{get_val(decoded_data['Slot Offset 3'])}",
        }

    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)
