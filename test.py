import unittest
import ais_decoder
import math

class TestAISDecoder(unittest.TestCase):
    def assert_close(self, a, b, abs_tol=0.1):
        if not math.isclose(a, b, abs_tol=abs_tol):
            raise AssertionError(f"{a} and {b} are not close enough")
        
class TestAISDecodeCNB(TestAISDecoder):
    def setUp(self):
        self.testMessage = "!AIVDM,1,1,,A,13QWhR012COJ`0TDSdkCS2ph0@=j,0*6C"
        self.aisMessage = ais_decoder.AISMessage(self.testMessage)
    
    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payloadInfo["MMSI"], 236581000)

    def test_decode_navigation_status(self):
        self.assertEqual(self.aisMessage.payloadInfo["Navigation Status"], 0)

    def test_decode_rate_of_turn(self):
        self.assert_close(self.aisMessage.payloadInfo["Rate of Turn"], 0.7)

    def test_decode_speed_over_ground(self):
        self.assert_close(self.aisMessage.payloadInfo["Speed Over Ground"], 14.7)

    def test_decode_position_accuracy(self):
        self.assertEqual(self.aisMessage.payloadInfo["Position Accuracy"], 0)
    
    def test_decode_longitude(self):
        self.assert_close(self.aisMessage.payloadInfo["Longitude"], 8.16)

    def test_decode_latitude(self):
        self.assert_close(self.aisMessage.payloadInfo["Latitude"], 35.9)

    def test_decode_course_over_ground(self):
        self.assert_close(self.aisMessage.payloadInfo["Course Over Ground"], 90.8)

    def test_decode_true_heading(self):
        self.assertEqual(self.aisMessage.payloadInfo["True Heading"], 92)


if __name__ == '__main__':
    unittest.main()