# decode_SDR.py -- logic for decoding static data reports (Message type 24)
from typing import Dict, Tuple, Optional, List, Union
from constants import safe_int, get_segment, bitstring_to_ascii, get_val, error_tuple

def decode_SDR(encodedPayload: str) -> Tuple[Dict, Dict]:
    """
    Function to decode static data reports (Message type 24)

    Args:
    encodedPayload (str): The binary payload of the AIS message
    
    Returns:
    Tuple[Dict, Dict] A tuple containing two dictionaries. The first dictionary contains the decoded values, while the second dictionary contains the field names.
    """

    try:
        decoded_data_1 = {
            "MMSI": safe_int(get_segment(encodedPayload, 8, 38)),
            "Part Number": safe_int(get_segment(encodedPayload, 38, 40)),
        }

        part_number = decoded_data_1["Part Number"]
        if(part_number == 0):
            decoded_data_2 = {
                "Vessel Name": bitstring_to_ascii(get_segment(encodedPayload, 40, 160)).split("@")[0],
                "Spare": safe_int(get_segment(encodedPayload, 160, 168)),
            }

            stringified_data = {
                "MMSI": get_val(decoded_data_1["MMSI"]),
                "Vessel Name": decoded_data_2["Vessel Name"],
                "Spare": get_val(decoded_data_2["Spare"]),
            }

        elif(part_number == 1):
            decoded_data_2 = {
                "Ship Type": safe_int(get_segment(encodedPayload, 40, 48)),
                "Vendor ID": bitstring_to_ascii(get_segment(encodedPayload, 48, 66)).split("@")[0],
                "Unit Model Code": safe_int(get_segment(encodedPayload, 66, 70)),
                "Serial Number": safe_int(get_segment(encodedPayload, 70, 90)),
                "Call Sign": bitstring_to_ascii(get_segment(encodedPayload, 90, 132)).split("@")[0],
                "Dimension to Bow": safe_int(get_segment(encodedPayload, 132, 141)),
                "Dimension to Stern": safe_int(get_segment(encodedPayload, 141, 150)),
                "Dimension to Port": safe_int(get_segment(encodedPayload, 150, 156)),
                "Dimension to Starboard": safe_int(get_segment(encodedPayload, 156, 162)),
                "Spare": safe_int(get_segment(encodedPayload, 162, 168)),
            }

            stringified_data = {
                "MMSI": get_val(decoded_data_1["MMSI"]),
                "Ship Type": get_val(decoded_data_2["Ship Type"]),
                "Vendor ID": decoded_data_2["Vendor ID"],
                "Unit Model Code": get_val(decoded_data_2["Unit Model Code"]),
                "Serial Number": get_val(decoded_data_2["Serial Number"]),
                "Call Sign": decoded_data_2["Call Sign"],
                "Dimension to Bow": get_val(decoded_data_2["Dimension to Bow"]),
                "Dimension to Stern": get_val(decoded_data_2["Dimension to Stern"]),
                "Dimension to Port": get_val(decoded_data_2["Dimension to Port"]),
                "Dimension to Starboard": get_val(decoded_data_2["Dimension to Starboard"]),
                "Spare": get_val(decoded_data_2["Spare"]),
            }
        else:
            decodeed_data_2 = {
                "Spare": safe_int(get_segment(encodedPayload, 40, 168)),
            }
            stringified_data = {
                "MMSI": get_val(decoded_data_1["MMSI"]),
                "Spare": get_val(decoded_data_2["Spare"]),
            }
    except Exception as e:
        return error_tuple(e)
    
    return (decoded_data_1.update(decoded_data_2), stringified_data)

