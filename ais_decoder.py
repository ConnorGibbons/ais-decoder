import time
import argparse
from statistics import mean
from decode_CNB import decode_CNB
from decode_BSR import decode_BSR
from decode_VRD import decode_VRD
from constants import MESSAGE_TYPES, PAYLOAD_BINARY_LOOKUP
from typing import Dict, Tuple, Optional, List

def get_payload_binary(encodedPayload, fill_bits = 0):
    return ''.join(map(PAYLOAD_BINARY_LOOKUP.get, encodedPayload)) + '0'*int(fill_bits)

def decodePayload(payload, message_type_int):
    if message_type_int in [1,2,3]:
        return decode_CNB(payload)
    elif message_type_int == 4:
        return decode_BSR(payload)
    elif message_type_int == 5:
        return decode_VRD(payload)
    else:
        return ({"Error: unsupported message type"}, {"Error: unsupported message type"})


# Class representing an AIS message. Contents of the "payload_info" dictionary will vary depending on the message type.
class AISMessage:

    def __init__(self, sentences):
        self.raw_sentences = []
        self.encoded_sentences = []
        self.payload_bitstrings = []
        self.checksums = []
        self.current_fragment_number = 1
        self.fragment_count = -1
        self.sequence_ID = -1
        self.message_type_int = -1
        self.channel = "N/A"
        self.message_complete = False
        try:
            if type(sentences) == str:
                self.addSentence(sentences)
            else:
                for sentence in sentences:
                    self.addSentence(sentence)
        except Exception as e: 
            raise Exception(f"Error parsing message: {e}")
        
    def toString(self):
        retString = ""
        retString += f"Raw Message(s): {self.raw_sentences}\n"
        retString += f"Fragment Count: {self.fragment_count}\n"
        retString += f"Sequence ID: {self.sequence_ID}\n"
        retString += f"Channel: {self.channel}\n"
        retString += f"Encoded Messages: {self.encoded_sentences}\n"
        retString += f"Message Type: {MESSAGE_TYPES[self.message_type_int-1]}\n"
        retString += f"Payload Info: {self.payload_info_stringified}\n"
        return retString
    
    def decode(self):
        decodedPayload = decodePayload("".join(self.payload_bitstrings), self.message_type_int)
        self.payload_info = decodedPayload[0]
        self.payload_info_stringified = decodedPayload[1]
        return self
    
    def addSentence(self, sentence):
        self.raw_sentences.append(sentence)
        sentence_parts = sentence.split(",")
        self.fragment_count = int(sentence_parts[1]) if self.fragment_count == -1 else self.fragment_count
        self.current_fragment_number = int(sentence_parts[2])
        if self.current_fragment_number == self.fragment_count:
            self.message_complete = True
        self.sequence_ID = sentence_parts[3] if self.sequence_ID == -1 else self.sequence_ID
        self.channel = sentence_parts[4] if self.channel == "N/A" else self.channel
        self.encoded_sentences.append(sentence_parts[5])
        end_of_sentence_components = sentence_parts[6].split("*")
        self.payload_bitstrings.append(get_payload_binary(sentence_parts[5],end_of_sentence_components[0]))
        self.checksums.append(end_of_sentence_components[1])
        self.message_type_int = int(self.payload_bitstrings[0][0:6], 2) if self.message_type_int == -1 else self.message_type_int
        if self.message_type_int < 0 or self.message_type_int > 27:
            raise Exception(f"Unsupported message type: {self.message_type_int}")
        return self
       


        





# --- Main Program --- #
def parse_ais_messages(file_path, delimiter = '\n'):
    AIS_sentences = open(file_path, "r").read().split(delimiter)
    messages = []
    errors = []
    current_message = None
    for sentence in AIS_sentences:
        if sentence == "":
            continue
        try:
            new_message = AISMessage(sentence)
            if current_message is None:
                if new_message.message_complete:
                    messages.append(new_message.decode())
                else: 
                    current_message = new_message
            else:
                if (new_message.sequence_ID == current_message.sequence_ID) and (new_message.fragment_count == current_message.fragment_count) and (new_message.current_fragment_number == current_message.current_fragment_number + 1):
                    current_message.addSentence(sentence)
                    if current_message.message_complete:
                        messages.append(current_message.decode())
                        current_message = None
                else:
                    errors.append(f"Error: Receieved non-sequential message when expecting message with sequence ID {current_message.sequence_ID}")
                    current_message = None
        except Exception as e:
            errors.append(f"Error parsing message: {e}")
    return (messages, errors)

def main():
    parser = argparse.ArgumentParser(description="AIS Message Decoder")
    parser.add_argument("--file_path", help="Path to the file containing AIS messages")
    parser.add_argument("--benchmark", action="store_true", help="Run in benchmark mode")
    parser.add_argument("--iterations", type=int, default=100, help="Number of iterations for benchmark (default: 100)")
    parser.add_argument("--outfile", help="Path to the file to write the decoded messages to")
    args = parser.parse_args()

    if args.benchmark:
        print(f"Running benchmark with {args.iterations} iterations...")
        times = []
        for _ in range(args.iterations):
            start_time = time.time()
            messages = parse_ais_messages(args.file_path)[0]
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = mean(times)
        print(f"Average runtime over {args.iterations} iterations: {(avg_time * 1000):.6f} ms")
        print(f"Total messages parsed in each iteration: {len(messages)} (Total: {len(messages) * args.iterations})")
        print(f"Average time per message: {(avg_time * 1000) / len(messages):.6f} ms")
    else:
        start_time = time.time()
        messages, errors = parse_ais_messages(args.file_path)
        end_time = time.time()
        if args.outfile:
            with open(args.outfile, "w") as f:
                for message in messages:
                    f.write(message.toString())
                    f.write("\n")
        else:
            for message in messages:
                print(message.toString())
        
        print(f"Runtime: {(end_time - start_time) * 1000:.2f}ms")
        print(f"Total messages parsed: {len(messages)-len(errors)}")
        print(f"Errors: {len(errors)}")

if __name__ == "__main__":
    main()
