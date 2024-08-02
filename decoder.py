import time
from decode_CNB import decodeCNB

# Message Types List (in order of message type number)
messageTypes = [
    "Position Report Class A", # -- Supported
    "Position Report Class A (Assigned schedule)", # -- Supported
    "Position Report Class A (Response to interrogation)", # -- Supported
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

def getPayloadBinary(encodedPayload):
    decodedNumArray = [] # Array to store the decoded numbers in decimal
    for char in encodedPayload:
        subtracted = ord(char) - 48
        if subtracted > 40:
            subtracted -= 8
        decodedNumArray.append(bin(subtracted)[2:].zfill(6))
    binaryString = "".join(decodedNumArray)
    return binaryString

def getMessageTypeString(payload):
    messageTypeInt = int(payload[0:6], 2)
    return messageTypes[messageTypeInt]

def decodePayload(payload, messageTypeInt):
    if messageTypeInt in [1,2,3]:
        return decodeCNB(payload)
    else:
        return ({"Error: unsupported message type"}, {"Error: unsupported message type"})


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
