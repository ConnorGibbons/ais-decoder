#decode_BSR.py -- logic for decoding Base Station Reports (Message Type 4)
from constants import safe_int, get_segment, get_val, longitudeCalc, latitudeCalc



# Decodes a Base Station Report (Message Type 4)    
def decodeBSR(binaryString):
    try:

        BSRDict = {
            "MMSI": safe_int(get_segment(binaryString, 8, 38)),
            "Year (UTC)": safe_int(get_segment(binaryString, 38, 52)),
            "Month (UTC)": safe_int(get_segment(binaryString, 52, 56)),
            "Day (UTC)": safe_int(get_segment(binaryString, 56, 61)),
            "Hour (UTC)": safe_int(get_segment(binaryString, 61, 66)),
            "Minute (UTC)": safe_int(get_segment(binaryString, 66, 72)),
            "Second (UTC)": safe_int(get_segment(binaryString, 72, 78)),
            "Position Accuracy": safe_int(get_segment(binaryString, 78, 79)),
            "Longitude": longitudeCalc(safe_int(get_segment(binaryString, 79, 107))),
            "Latitude": latitudeCalc(safe_int(get_segment(binaryString, 107, 134))),
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