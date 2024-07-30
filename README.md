Python script for decoding AIS (Automatic Identification System) sentences. AIS sees regular use in maritime applicaitons, where modules installed on vessels
will emit signals in NMEA 0813 format providing information such as position, heading, speed, etc.

An example sentence looks like this: !AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23

Currently, the script is able to extract this information from the sentence:
Raw Message: !AIVDM,1,1,,A,13HOI:0P0000VOHLCnHQKwvL05Ip,0*23
Fragment Count: 1
Current Fragment: 1
Sequence ID: None
Channel: A
Encoded Message: 13HOI:0P0000VOHLCnHQKwvL05Ip
Fill Bits: 0
Checksum: 23
Message Type: Position Report Class A (1)
Payload Info: {'MMSI': '227006760', 'Navigation Status': 'Under way (Power)', 'Rate of Turn': 'Turning information not available', 'SOG': '0.0 knots', 'Position Accuracy': 'Low', 'Longitude': '0.13138', 'Latitude': '49.47557666666667', 'COG': '36.7'}

This script is based on the information provided here: https://gpsd.gitlab.io/gpsd/AIVDM.html
