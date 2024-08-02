#decode_BSR.py -- logic for decoding Base Station Reports (Message Type 4)

# -- Calculation functions --




# Decodes a Base Station Report (Message Type 4)    
def decodeBSR(binaryString):
    try:
        def safe_int(value, base=2):
            return int(value, base) if value else None
    
        def get_segment(binaryString, start, end):
            return binaryString[start:end] if len(binaryString) >= end else None
        
        BSRDict = {
            "MMSI": safe_int(get_segment(binaryString, 8, 38)),
            "Year (UTC)": safe_int(get_segment(binaryString, 38, 52)),
            "Month (UTC)": safe_int(get_segment(binaryString, 52, 56)),
            "Day (UTC)": safe_int(get_segment(binaryString, 56, 61)),
            "Hour (UTC)": safe_int(get_segment(binaryString, 61, 66)),
            "Minute (UTC)": safe_int(get_segment(binaryString, 66, 72)),
            "Second (UTC)": safe_int(get_segment(binaryString, 72, 78)),
        }

        BSRDictStringified = {
        
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