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

rateOfTurn = {
    "0": "Not turning",
    "128": "Turning information not available",
    "127": "Turning right at more than 5 degrees per 30 seconds (No turn information available)",
    "-127": "Turning left at more than 5 degrees per 30 seconds (No turn information available)",
}

# Rate of Turn calculation -- input = 4.733 * sqrt(rateOfTurn).
# Output is the rate of turn in degrees per minute.
def rotCalc(rawRot):
    if rawRot > 126:
        return 127
    elif rawRot < -126:
        return -127
    elif rawRot == 128:
        return rawRot
    elif rawRot == 0:
        return rawRot
    elif rawRot > 0 and rawRot <= 126:
        return (rawRot/4.733) ** 2
    elif rawRot < 0 and rawRot >= -126:
        return -((rawRot/4.733) ** 2)
    
def sogCalc(rawSOG):
    if(rawSOG == 1023):
        return "N/A"
    elif(rawSOG == 1022):
        return "SOG exceeds 102.2"
    else:
        return rawSOG / 10

def rotToString(rot):
    if rot > 126:
        return rateOfTurn["127"]
    elif rot < -126:
        return rateOfTurn["-127"]
    elif rot == 128:
        return rateOfTurn["128"]
    elif rot == 0:
        return rateOfTurn["0"]
    else:
        return f"{rot} degrees per minute"
    
# Class representing an AIS message. Contents of the "payloadInfo" dictionary will vary depending on the message type.
class AISMessage:

    def __init__(self, message):
        self.rawMessage = message
        message = message.split(",")
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

def decodeCNB(binaryString):
    try:
        CNBDict = {
            "MMSI": int(binaryString[8:38], 2),
            "Navigation Status": int(binaryString[38:42], 2),
            "Rate of Turn": rotCalc(int(binaryString[42:50], 2)),
            "SOG": sogCalc(int(binaryString[50:60],2)),
            "Position Accuracy": int(binaryString[60], 2),
        }
        CNBDictStringified = {
            "MMSI": str(CNBDict["MMSI"]),
            "Navigation Status": navigationStatus[CNBDict["Navigation Status"]],
            "Rate of Turn": rotToString(CNBDict["Rate of Turn"]),
            "SOG": str(CNBDict["SOG"]) + " knots",
            "Position Accuracy": "High" if CNBDict["Position Accuracy"] == 1 else "Low"
        }
    except Exception as e:
        CNBDict = {
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
