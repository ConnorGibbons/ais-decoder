class AISMessage:
    def __init__(self, message):
        message = message.split(",")
        self.fragmentCount = int(message[1]) # Number of fragments
        self.currentFragment = int(message[2])
        self.sequenceID = message[3] if message[3] != "" else "None" # Sequence ID (probably not used)
        self.channel = message[4]
        self.encodedMessage = message[5]
        self.fillBits = message[6].split("*")[0]
        self.checksum = message[6].split("*")[1]
        self.payloadbitstring = getPayloadBinary(self.encodedMessage)
        self.messageType = getMessageType(self.payloadbitstring)
    def toString(self):
        return "Fragment Count: " + str(self.fragmentCount) + "\nCurrent Fragment: " + str(self.currentFragment) + "\nSequence ID: " + self.sequenceID + "\nChannel: " + self.channel + "\nEncoded Message: " + self.encodedMessage + "\nFill Bits: " + self.fillBits + "\nChecksum: " + self.checksum + "\nPayload: " + self.payloadbitstring

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
    messageTypeInt = int(binaryString[0:6], 2)
    messageTypeString = ""
    

AISSentences = open("AISSample7,28,24.txt", "r").read().split("\n")
messages = []  
for sentence in AISSentences:
    messages.append(AISMessage(sentence))
for message in messages:
    print(message.toString() + "\n")

