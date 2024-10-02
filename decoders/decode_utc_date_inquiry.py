# decode_utc_date_inquiry.py -- logic for decoding UTC/Date Inquiry Messages (type 10)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, error_tuple

def decode_utc_date_inquiry(binary_string: str):
    """
    Decode a UTC/Date Inquiry message (DTI), message type 10

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try:
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Spare": safe_int(get_segment(binary_string, 38, 40)),
            "Destination MMSI": safe_int(get_segment(binary_string, 40, 70)),
            "Spare": safe_int(get_segment(binary_string, 70, 72))
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Destination MMSI": f"{get_val(decoded_data['Destination MMSI'])}",
        }

    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)