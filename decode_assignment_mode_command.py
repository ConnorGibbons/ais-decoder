# decode_AMC.py - Logic for decoding Assignment Mode Command messages (message type 16)
from typing import Dict, Tuple, Optional, List
from constants import safe_int, get_segment, get_val, error_tuple


def decode_assignment_mode_command(binary_string: str):
    """
    Decode Assignment Mode Command (message type 16)

    Args:
    binary_string (str): The binary payload as a string.

    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values, and a dictionary with stringified values.
    """

    try: 
        decoded_data = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Spare": safe_int(get_segment(binary_string, 38, 40)),
            "Destination A MMSI": safe_int(get_segment(binary_string, 40, 70)),
            "Offset A": safe_int(get_segment(binary_string, 70, 82)),
            "Increment A": safe_int(get_segment(binary_string, 82, 92)),
            "Destination B MMSI": safe_int(get_segment(binary_string, 92, 122)),
            "Offset B": safe_int(get_segment(binary_string, 122, 134)),
            "Increment B": safe_int(get_segment(binary_string, 134, 144)),
        }

        stringified_data = {
            "MMSI": f"{get_val(decoded_data['MMSI'])}",
            "Spare": f"{get_val(decoded_data['Spare'])}",
            "Destination A MMSI": f"{get_val(decoded_data['Destination A MMSI'])}",
            "Offset A": f"{get_val(decoded_data['Offset A'])}",
            "Increment A": f"{get_val(decoded_data['Increment A'])}",
            "Destination B MMSI": f"{get_val(decoded_data['Destination B MMSI'])}",
            "Offset B": f"{get_val(decoded_data['Offset B'])}",
            "Increment B": f"{get_val(decoded_data['Increment B'])}",
        }

    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data, stringified_data)