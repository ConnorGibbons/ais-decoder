import time

messageTypes = ["Position Report Class A", #01
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

class AISMessage:
    def __init__(self, message):
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
        self.messageType = getMessageType(self.payloadbitstring)
    def toString(self):
        return f"Fragment Count: {self.fragmentCount}\nCurrent Fragment: {self.currentFragment}\nSequence ID: {self.sequenceID}\nChannel: {self.channel}\nEncoded Message: {self.encodedMessage}\nFill Bits: {self.fillBits}\nChecksum: {self.checksum}\nPayload: {self.payloadbitstring}\nMessage Type: {self.messageType}"

def getPayloadBinary(encodedPayload):
    decodedNumArray = [] # Array to store the decoded numbers in decimal
    for char in encodedPayload:
        subtracted = ord(char) - 48
        if subtracted > 40:
            subtracted -= 8
        decodedNumArray.append(bin(subtracted)[2:].zfill(6))
    binaryString = "".join(decodedNumArray)
    return binaryString

def getMessageType(binaryString):
    messageTypeInt = int(binaryString[0:6], 2)-1
    messageTypeString = messageTypes[messageTypeInt]
    return messageTypeString + f" ({messageTypeInt+1})"
    
    
startTime = time.time()
AISSentences = open("AISSample7,28,24.txt", "r").read().split("\n")
messages = []  
for sentence in AISSentences:
    messages.append(AISMessage(sentence))
for message in messages:
    print(message.toString())
    print("\n")
endTime = time.time()
print(f"Runtime: {(endTime-startTime)* 1000}ms")
