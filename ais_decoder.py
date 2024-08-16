import time
from decode_CNB import decodeCNB
from decode_BSR import decodeBSR
from constants import MESSAGE_TYPES, PAYLOAD_BINARY_LOOKUP

def getPayloadBinary(encodedPayload):
    return ''.join(PAYLOAD_BINARY_LOOKUP[char] for char in encodedPayload)

def decodePayload(payload, messageTypeInt):
    if messageTypeInt in [1,2,3]:
        return decodeCNB(payload)
    elif messageTypeInt == 4:
        return decodeBSR(payload)
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
        if(self.messageTypeInt < 1 or self.messageTypeInt > 27):
            raise Exception("Invalid message type")
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
        retString += f"Longitude Bitstring: {self.payloadbitstring[61:89]}\n"
        retString += f"Message Type: {MESSAGE_TYPES[self.messageTypeInt-1]}\n"
        retString += f"Payload Info: {self.payloadInfoStringified}\n"
        return retString


# --- Main Program --- #
def main():
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

if __name__ == "__main__":
    main()
