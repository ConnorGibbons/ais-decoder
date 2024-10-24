import time
import argparse
import json
from statistics import mean
from decoders import *
from constants import MESSAGE_TYPES, PAYLOAD_BINARY_LOOKUP
from typing import Dict, Tuple, Optional, List, Union, Callable


"""Mapping for decoder functions"""
DECODER_MAP: Dict[int, Callable] = {
    1: decode_position_report_class_a, #
    2: decode_position_report_class_a, #
    3: decode_position_report_class_a, #
    4: decode_base_station_report, #
    5: decode_static_and_voyage_data, #
    6: decode_binary_addressed_messsage, #
    7: decode_binary_acknowledge, # ?
    8: decode_binary_broadcast_message, 
    9: decode_standard_sar_aircraft_position,
    10: decode_utc_date_inquiry,
    11: decode_base_station_report,
    13: decode_binary_acknowledge,
    14: decode_safety_related_broadcast,
    15: decode_interrogation,
    16: decode_assignment_mode_command,
    18: decode_position_report_class_b,
    19: decode_position_report_class_b_ext,
    21: decode_aid_to_navigation,
    24: decode_static_data_report, 
    25: decode_single_slot_binary_message,
    26: decode_multi_slot_binary_message,
    27: decode_long_range_broadcast
}


def get_payload_binary(encodedPayload: str, fill_bits: int = 0) -> str:
    try:
        return ''.join(map(PAYLOAD_BINARY_LOOKUP.get, encodedPayload)) + '0'*int(fill_bits)
    except KeyError as e:
       raise Exception(f"Error decoding payload: {e}")

def decodePayload(payload: str, message_type_int: int) -> Tuple[Dict, Dict]:
    decoder = DECODER_MAP.get(message_type_int)
    if decoder:
        return decoder(payload)
    else:
        error_message = "Error: unsupported message type"
        return ({"Error": error_message}, {"Error": error_message})


# Class representing an AIS message. Contents of the "payload_info" dictionary will vary depending on the message type.
class AISMessage:

    def __init__(self, sentences: Union[str, List[str]]):
        self.raw_sentences: List[str] = []
        self.encoded_sentences: List[str] = []
        self.payload_bitstrings: List[str] = []
        self.checksums: List[str] = []
        self.seen_fragment_numbers: List[int] = []
        self.current_fragment_number: int = 1
        self.fragment_count: int = -1
        self.sequence_ID: str = "-1"
        self.message_type_int: int = -1
        self.channel: str = "N/A"
        self.message_complete: bool = False
        try:
            if isinstance(sentences, str):
                self.addSentence(sentences)
            elif isinstance(sentences, list):
                for sentence in sentences:
                    self.addSentence(sentence)
            else:
                raise Exception("Invalid input type: expected string or list")
        except Exception as e: 
            raise Exception(f"Error parsing message: {e}")
        self.payload_info: Dict = {}
        self.payload_info_stringified: Dict = {}

    def __dict__(self) -> Dict:
        return {
            "Raw Message(s)": self.raw_sentences,
            "Fragment Count": self.fragment_count,
            "Sequence ID": self.sequence_ID,
            "Channel": self.channel,
            "Encoded Messages": self.encoded_sentences,
            "Message Type": MESSAGE_TYPES[self.message_type_int-1],
            "Payload Info": self.payload_info,
            "Payload Info (Stringified)": self.payload_info_stringified
        }
        
    def __str__(self) -> str:
        retString = ""
        retString += f"Raw Message(s): {self.raw_sentences}\n"
        retString += f"Fragment Count: {self.fragment_count}\n"
        retString += f"Sequence ID: {self.sequence_ID}\n"
        retString += f"Channel: {self.channel}\n"
        retString += f"Encoded Messages: {self.encoded_sentences}\n"
        retString += f"Message Type: {MESSAGE_TYPES[self.message_type_int-1]} ({self.message_type_int})\n"
        retString += f"Payload Info: {self.payload_info_stringified}\n"
        return retString
    
    def decode(self) -> 'AISMessage':
        decodedPayload = decodePayload("".join(self.payload_bitstrings), self.message_type_int)
        self.payload_info = decodedPayload[0]
        self.payload_info_stringified = decodedPayload[1]
        return self
    
    def addSentence(self, sentence: str) -> None:
        self.raw_sentences.append(sentence)
        components = self.extract_sentence_components(sentence)
        self.update_states(components)
        self.validate_message_type()
        
    def extract_sentence_components(self, sentence: str) -> Dict[str, Union[int, str]]:
        sentence_parts = sentence.split(",")
        components = {
            "fragment_count": int(sentence_parts[1]),
            "current_fragment_number": int(sentence_parts[2]),
            "sequence_ID": sentence_parts[3],
            "channel": sentence_parts[4],
            "encoded_sentence": sentence_parts[5],
            "payload": get_payload_binary(sentence_parts[5]),
            "checksum": sentence_parts[6].split("*")[1]
        }
        return components
    
    def update_states(self, components: Dict[str, Union[int, str]]) -> None:
        self.fragment_count = components["fragment_count"] if self.fragment_count == -1 else self.fragment_count
        self.current_fragment_number = components["current_fragment_number"]
        self.seen_fragment_numbers.append(self.current_fragment_number)
        self.sequence_ID = components["sequence_ID"] if self.sequence_ID == "-1" else self.sequence_ID
        self.channel = components["channel"] if self.channel == "N/A" else self.channel
        self.encoded_sentences.append(components["encoded_sentence"])
        self.payload_bitstrings.append(components["payload"])
        self.checksums.append(components["checksum"])
        self.message_type_int = int(self.payload_bitstrings[0][0:6], 2)
        self.message_complete = self.seen_fragment_numbers == list(range(1, self.fragment_count + 1))

    def validate_message_type(self) -> None:
        if self.message_type_int < 1 or self.message_type_int > 28:
            raise Exception(f"Unsupported message type: {self.message_type_int}")
    
    def is_complete(self) -> bool:
        return self.message_complete


# --- Main Program --- #
def parse_ais_messages(source: Union[str, List[str]], delimiter: str = '\n') -> Tuple[List[AISMessage], List[str]]:

    if(isinstance(source, str)):
        AIS_sentences = open(source, "r").read().split(delimiter)
    elif(isinstance(source, list)):
        AIS_sentences = source
    else:
        raise Exception("Invalid input type: expected string or list")
    
    messages: List[AISMessage] = []
    errors: List[str] = []
    current_message: Optional[AISMessage] = None
    for sentence in AIS_sentences:
        if sentence == "":
            continue
        try:
            new_message = AISMessage(sentence)
            if current_message is None:
                if new_message.is_complete():
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

def main() -> None:
    parser = argparse.ArgumentParser(description="AIS Message Decoder")
    parser.add_argument("--file_path", help="Path to the file containing AIS messages")
    parser.add_argument("--benchmark", action="store_true", help="Run in benchmark mode")
    parser.add_argument("--iterations", type=int, default=100, help="Number of iterations for benchmark (default: 100)")
    parser.add_argument("--outfile", help="Path to the file to write the decoded messages to")
    parser.add_argument("--json", help="Output as array of JSON objects", default=False, type=bool)
    args = parser.parse_args()

    if args.benchmark:
        print(f"Running benchmark with {args.iterations} iterations...")
        times: List[float] = []
        AIS_sentences = open(args.file_path, "r").read().split("\n")
        for _ in range(args.iterations):
            start_time = time.time()
            messages, _ = parse_ais_messages(AIS_sentences)
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
                if args.json:
                    f.write(json.dumps([message.__dict__() for message in messages], indent=4))
                else:
                    for message in messages:
                        f.write(message.__str__())
                        f.write("\n")
        else:
            if args.json:
                print(json.dumps([message.__dict__() for message in messages], indent=4))
            else:
                for message in messages:
                    print(message)
        
        print(f"Runtime: {(end_time - start_time) * 1000:.2f}ms")
        print(f"Total messages parsed: {len(messages)}")
        print(f"Errors: {len(errors)}")

if __name__ == "__main__":
    main()