# decode_BSR.py -- logic for decoding Base Station Reports (Message Type 4)
from typing import Dict, Tuple, Optional
from constants import safe_int, get_segment, get_val, calculate_latitude, calculate_longitude

def decode_BSR(binary_string: str) -> Tuple[Dict[str, Optional[int]], Dict[str, str]]:
    """
    Decode a base station report (BSR) message, message type 4.
    
    Args:
    binary_string (str): The binary payload as a string.
    
    Returns:
    Tuple[Dict[str, Optional[int]], Dict[str, str]]: A tuple containing a dictionary of the decoded values
    and a dictionary of the stringified values.
    """
    try:
        BSRDict = {
            "MMSI": safe_int(get_segment(binary_string, 8, 38)),
            "Year (UTC)": safe_int(get_segment(binary_string, 38, 52)),
            "Month (UTC)": safe_int(get_segment(binary_string, 52, 56)),
            "Day (UTC)": safe_int(get_segment(binary_string, 56, 61)),
            "Hour (UTC)": safe_int(get_segment(binary_string, 61, 66)),
            "Minute (UTC)": safe_int(get_segment(binary_string, 66, 72)),
            "Second (UTC)": safe_int(get_segment(binary_string, 72, 78)),
            "Position Accuracy": safe_int(get_segment(binary_string, 78, 79)),
            "Longitude": calculate_longitude(safe_int(get_segment(binary_string, 79, 107), signed=True)),
            "Latitude": calculate_latitude(safe_int(get_segment(binary_string, 107, 134), signed=True)),
        }

        BSRDictStringified = {
            "MMSI": f"{get_val(BSRDict['MMSI'])}",
            "Year (UTC)": f"{get_val(BSRDict['Year (UTC)'])}",
            "Month (UTC)": f"{get_val(BSRDict['Month (UTC)'])}",
            "Day (UTC)": f"{get_val(BSRDict['Day (UTC)'])}",
            "Hour (UTC)": f"{get_val(BSRDict['Hour (UTC)'])}",
            "Minute (UTC)": f"{get_val(BSRDict['Minute (UTC)'])}",
            "Second (UTC)": f"{get_val(BSRDict['Second (UTC)'])}",
            "Position Accuracy": "High" if BSRDict["Position Accuracy"] == 1 else "Low",
            "Longitude": f"{get_val(BSRDict['Longitude'])}°",
            "Latitude": f"{get_val(BSRDict['Latitude'])}°",
        }
    
    except Exception as e:
        BSRDict = {
            "Error": "Couldn't decode message"
        }
        BSRDictStringified = {
            "Error": "Couldn't decode message"
        }
        print(e)
    
    return (BSRDict, BSRDictStringified)