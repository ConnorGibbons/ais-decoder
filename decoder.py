import time

# Message Types List (in order of message type number)
messageTypes = [
    "Position Report Class A", #01
    "Position Report Class A (Assigned schedule)",
    "Position Report Class A (Response to interrogation)",
    "Base Station Report",
    "Static and Voyage Related Data",
    "Binary Addressed Message",
    "Binary Acknowledge",
    "Binary Broadcast Message",
    "Standard SAR Aircraft Position Report",
    "UTC and Date Inquiry",
    "UTC and Date Response",
    "Addressed Safety Related Message",
    "Safety Related Acknowledge",
    "Safety Related Broadcast Message",
    "Interrogation",
    "Assignment Mode Command",
    "DGNSS Binary Broadcast Message",
    "Standard Class B CS Position Report",
    "Extended Class B Equipment",
    "Data Link Management",
    "Aid-to-Navigation Report",
    "Channel Management",
    "Group Assignment Command",
    "Static Data Report",
    "Single Slot Binary Message",
    "Multiple Slot Binary Message",
    "Long Range AIS Broadcast Message"
]

# Navigation Status List
navigationStatus = [
    "Under way (Power)",
    "At anchor",
    "Not under command",
    "Restricted maneuverability",
    "Draft Constrained",
    "Moored",
    "Aground",
    "Engaged in fishing",
    "Under way (Sailing)",
    "---", # Reserved for future use
    "---", # Reserved for future use
    "Towing Astern", # Regional use
    "Towing Alongside", # Regional use
    "---", # Reserved for future use
    "AIS-SART is active",
    "Undefined"
]

# Rate of Turn calculation -- input = 4.733 * sqrt(rateOfTurn).
# Output is the rate of turn in degrees per minute.
def rotCalc(rawRot):
    if rawRot == 128 or rawRot is None:
        return -1
    elif rawRot > 126:
        return 127
    elif rawRot < -126:
        return -127
    elif rawRot == 0:
        return rawRot
    elif rawRot > 0 and rawRot <= 126:
        return (rawRot/4.733) ** 2
    elif rawRot < 0 and rawRot >= -126:
        return -((rawRot/4.733) ** 2)

# Speed over ground calculation -- input is sog in 0.1 knot units.
# Output is the speed over ground in knots.
def sogCalc(rawSOG):
    if rawSOG == 1023 or rawSOG is None:
        return -1
    else:
        return rawSOG / 10

# Longitude calculation -- input is in 1/600000 minutes.
# Output is the longitude in degrees.
def longitudeCalc(rawLongitude):
    if rawLongitude == 181 or rawLongitude is None:
        return -1 # Longitude not available
    else:
        return rawLongitude / 600000

# Latitude calculation -- input is in 1/600000 minutes.
# Output is the latitude in degrees.
def latitudeCalc(rawLatitude):
    if rawLatitude == 91 or rawLatitude is None:
        return -1 # Latitude not available
    else:
        return rawLatitude / 600000

# Course over ground calculation -- input is in 0.1 degrees.
# Output is the course over ground in degrees.
def cogCalc(rawCOG):
    if rawCOG == 3600 or rawCOG is None:
        return -1 # COG not available
    else:
        return rawCOG / 10

# Heading calculation -- input is in degrees.
# Output is the heading in degrees (just here to check if heading is available).
def headingCalc(rawHeading):
    if rawHeading == 511 or rawHeading is None:
        return -1 # Heading not available
    else:
        return rawHeading
    


def rotToString(rot):
    if rot > 126:
        return "Turning right at more than 5 degrees per 30 seconds (No turn information available)"
    elif rot < -126:
        return "Turning left at more than 5 degrees per 30 seconds (No turn information available)"
    elif rot == 128 or rot == -1:
        return "Turning information not available"
    elif rot == 0:
        return "Not turning"
    else:
        return "N/A"
    
def getVal(val):
    if val == -1:
        return "N/A"
    else:
        return val

    
# Class representing an AIS message. Contents of the "payloadInfo" dictionary will vary depending on the message type.
class AISMessage:

    def __init__(self, message):
        self.rawMessage = message
        message = message.split(",")
        if len(message) < 7:
            raise Exception("Invalid message format")
        endOfMessageComponents = message[6].split("*")
        self.fragmentCount = int(message[1]) # Number of fragments
        self.currentFragment = int(message[2])
        self.sequenceID = message[3] if message[3] != "" else "None" # Sequence ID (probably not used)
        self.channel = message[4]
        self.encodedMessage = message[5]
        self.fillBits = endOfMessageComponents[0]
        self.checksum = endOfMessageComponents[1]
        self.payloadbitstring = getPayloadBinary(self.encodedMessage)
        self.messageTypeInt = int(self.payloadbitstring[0:6], 2)
        decodedPayload = decodePayload(self.payloadbitstring, self.messageTypeInt)
        self.payloadInfo = decodedPayload[0]
        self.payloadInfoStringified = decodedPayload[1]

    def toString(self):
        retString = ""
        retString += f"Raw Message: {self.rawMessage}\n"
        retString += f"Fragment Count: {self.fragmentCount}\n"
        retString += f"Current Fragment: {self.currentFragment}\n"
        retString += f"Sequence ID: {self.sequenceID}\n"
        retString += f"Channel: {self.channel}\n"
        retString += f"Encoded Message: {self.encodedMessage}\n"
        retString += f"Fill Bits: {self.fillBits}\n"
        retString += f"Checksum: {self.checksum}\n"
        #retString += f"Payload Bitstring: {self.payloadbitstring}\n"
        retString += f"Message Type: {getMessageTypeString(self.payloadbitstring)}\n"
        retString += f"Payload Info: {self.payloadInfoStringified}\n"
        return retString
    

# --- String Helper Functions --- #

# Function to convert the encoded payload to binary string
# Input: ASCII encoded payload
# Output: Binary string of the payload (each character in original ASCII is converted to 6-bit binary)
def getPayloadBinary(encodedPayload):
    decodedNumArray = [] # Array to store the decoded numbers in decimal
    for char in encodedPayload:
        subtracted = ord(char) - 48
        if subtracted > 40:
            subtracted -= 8
        decodedNumArray.append(bin(subtracted)[2:].zfill(6))
    binaryString = "".join(decodedNumArray)
    return binaryString

def getMessageTypeString(binaryString):
    messageTypeInt = int(binaryString[0:6], 2)-1
    if(messageTypeInt > 26) or (messageTypeInt < 0):
        return f"Unknown Message Type {messageTypeInt+1}"
    messageTypeString = messageTypes[messageTypeInt]
    return messageTypeString + f" ({messageTypeInt+1})"

def decodePayload(encodedPayload, messageTypeInt):
    if messageTypeInt in [1, 2, 3]: # Position Report Class A
        return decodeCNB(encodedPayload)
    else:
        return ("Couldn't decode: Unsupported Message Type", "Couldn't decode: Unsupported Message Type")

# Decodes a Class A Position Report (Message Types 1, 2, 3)
def decodeCNB(binaryString):
    try:
        def safe_int(value, base=2):
            return int(value, base) if value else None
    
        def get_segment(binaryString, start, end):
            return binaryString[start:end] if len(binaryString) >= end else None
    
        CNBDict = {
            "MMSI": safe_int(get_segment(binaryString, 8, 38)),
            "Navigation Status": safe_int(get_segment(binaryString, 38, 42)),
            "Rate of Turn": rotCalc(safe_int(get_segment(binaryString, 42, 50))),
            "SOG": sogCalc(safe_int(get_segment(binaryString, 50, 60))),
            "Position Accuracy": safe_int(get_segment(binaryString, 60, 61)),
            "Longitude": longitudeCalc(safe_int(get_segment(binaryString, 61, 89))),
            "Latitude": latitudeCalc(safe_int(get_segment(binaryString, 89, 116))),
            "COG": cogCalc(safe_int(get_segment(binaryString, 116, 128))),
            "True Heading": headingCalc(safe_int(get_segment(binaryString, 128, 137))),
        }
    
        CNBDictStringified = {
            "MMSI": str(CNBDict["MMSI"]) if CNBDict["MMSI"] is not None else "N/A",
            "Navigation Status": navigationStatus[CNBDict["Navigation Status"]] if CNBDict["Navigation Status"] is not None else "N/A",
            "Rate of Turn": rotToString(CNBDict["Rate of Turn"]) if CNBDict["Rate of Turn"] is not None else "N/A",
            "SOG": str(getVal(CNBDict["SOG"])) + " knots" if CNBDict["SOG"] is not None else "N/A",
            "Position Accuracy": "High" if CNBDict["Position Accuracy"] == 1 else "Low",
            "Longitude": str(getVal(CNBDict["Longitude"])) + "°" if CNBDict["Longitude"] is not None else "N/A",
            "Latitude": str(getVal(CNBDict["Latitude"])) + "°" if CNBDict["Latitude"] is not None else "N/A",
            "COG": str(getVal(CNBDict["COG"])) + "°" if CNBDict["COG"] is not None else "N/A",
        }

    except Exception as e:
        CNBDict = {
            "Error": "Couldn't decode message"
        }
        CNBDictStringified = {
            "Error": "Couldn't decode message"
        }
        print(e)

    return (CNBDict, CNBDictStringified)
    




# --- Main Program --- #

startTime = time.time()
AISSentences = open("nmea-sample", "r").read().split("\n")
#AISSentences = open("AISSample7,28,24.txt", "r").read().split("\n")
outfile = open("AISoutput.txt", "w")
messages = []  
for sentence in AISSentences:
    try:
        message = AISMessage(sentence)
        messages.append(message)
        outfile.write(message.toString() + "\n\n")
    except:
        outfile.write("Error decoding message: " + sentence + "\n\n")
outfile.close()
endTime = time.time()
print(f"Runtime: {(endTime-startTime)* 1000}ms")
