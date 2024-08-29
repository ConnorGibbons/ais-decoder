import unittest
import ais_decoder
import math
# Hi
class TestAISDecoder(unittest.TestCase):
    def assert_close(self, a, b, abs_tol=0.1):
        if not math.isclose(a, b, abs_tol=abs_tol):
            raise AssertionError(f"{a} and {b} are not close enough")
        
class TestAISDecodeCNB(TestAISDecoder):
    def setUp(self):
        self.testMessage = "!AIVDM,1,1,,A,13QWhR012COJ`0TDSdkCS2ph0@=j,0*6C"
        self.testMessage2 = "!AIVDM,1,1,,B,11mg=5OP00Pdu`JI>lS59Ov<0<0g,0*49"
        self.aisMessage = ais_decoder.AISMessage(self.testMessage)
        self.aisMessage2 = ais_decoder.AISMessage(self.testMessage2)
    
    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payloadInfo["MMSI"], 236581000)
        self.assertEqual(self.aisMessage2.payloadInfo["MMSI"], 123456789)

    def test_decode_navigation_status(self):
        self.assertEqual(self.aisMessage.payloadInfo["Navigation Status"], 0)
        self.assertEqual(self.aisMessage2.payloadInfo["Navigation Status"], 15)

    def test_decode_rate_of_turn(self):
        self.assert_close(self.aisMessage.payloadInfo["Rate of Turn"], 0.7)
        self.assert_close(self.aisMessage2.payloadInfo["Rate of Turn"], -127)

    def test_decode_speed_over_ground(self):
        self.assert_close(self.aisMessage.payloadInfo["Speed Over Ground"], 14.7)

    def test_decode_position_accuracy(self):
        self.assertEqual(self.aisMessage.payloadInfo["Position Accuracy"], 0)
        self.assertEqual(self.aisMessage2.payloadInfo["Position Accuracy"], 1)

    def test_decode_longitude(self):
        self.assert_close(self.aisMessage.payloadInfo["Longitude"], -8.16)
        self.assert_close(self.aisMessage2.payloadInfo["Longitude"], 9.82)

    def test_decode_latitude(self):
        self.assert_close(self.aisMessage.payloadInfo["Latitude"], 35.9)
        self.assert_close(self.aisMessage2.payloadInfo["Latitude"], 44.09)

    def test_decode_course_over_ground(self):
        self.assert_close(self.aisMessage.payloadInfo["Course Over Ground"], 90.8)
        self.assert_close(self.aisMessage2.payloadInfo["Course Over Ground"], 131.7)

    def test_decode_true_heading(self):
        self.assertEqual(self.aisMessage.payloadInfo["True Heading"], 92)
        self.assertEqual(self.aisMessage2.payloadInfo["True Heading"], 511)

class TestAISDecodeBSR(TestAISDecoder):
    def setUp(self):
        self.testMessage = "!AIVDM,1,1,,B,403t?hAuho;N>`Pc:j>Kgq700D2D,0*2C"
        self.testMessage2 = "!AIVDM,1,1,,A,4020tPiuho;N@PoHAPO027G00@9S,0*5B"
        self.aisMessage = ais_decoder.AISMessage(self.testMessage)
        self.aisMessage2 = ais_decoder.AISMessage(self.testMessage2)
    
    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payloadInfo["MMSI"], 4132801)
        self.assertEqual(self.aisMessage2.payloadInfo["MMSI"], 2112643)
    
    def test_decode_year(self):
        self.assertEqual(self.aisMessage.payloadInfo["Year (UTC)"], 2012)
        self.assertEqual(self.aisMessage2.payloadInfo["Year (UTC)"], 2012)
    
    def test_decode_month(self):
        self.assertEqual(self.aisMessage.payloadInfo["Month (UTC)"], 3)
        self.assertEqual(self.aisMessage2.payloadInfo["Month (UTC)"], 3)

    def test_decode_day(self):
        self.assertEqual(self.aisMessage.payloadInfo["Day (UTC)"], 14)
        self.assertEqual(self.aisMessage2.payloadInfo["Day (UTC)"], 14)
    
    def test_decode_hour(self):
        self.assertEqual(self.aisMessage.payloadInfo["Hour (UTC)"], 11)
        self.assertEqual(self.aisMessage2.payloadInfo["Hour (UTC)"], 11)
    
    def test_decode_minute(self):
        self.assertEqual(self.aisMessage.payloadInfo["Minute (UTC)"], 30)
        self.assertEqual(self.aisMessage2.payloadInfo["Minute (UTC)"], 30)
    
    def test_decode_second(self):
        self.assertEqual(self.aisMessage.payloadInfo["Second (UTC)"], 14)
        self.assertEqual(self.aisMessage2.payloadInfo["Second (UTC)"], 16)
    
    def test_decode_position_accuracy(self):
        self.assertEqual(self.aisMessage.payloadInfo["Position Accuracy"], 1)
        self.assertEqual(self.aisMessage2.payloadInfo["Position Accuracy"], 1)
    
    def test_decode_longitude(self):
        self.assert_close(self.aisMessage.payloadInfo["Longitude"], 118.98)
        self.assert_close(self.aisMessage2.payloadInfo["Longitude"], 12.09)
    
    def test_decode_latitude(self):
        self.assert_close(self.aisMessage.payloadInfo["Latitude"], 25.22)
        self.assert_close(self.aisMessage2.payloadInfo["Latitude"], 54.17)

    def test_decode_type_of_electronic_position_fixing_device(self):
        self.assertEqual(self.aisMessage.payloadInfo["Type of Electronic Position Fixing Device"], 7)
        self.assertEqual(self.aisMessage2.payloadInfo["Type of Electronic Position Fixing Device"], 7)
    
    def test_decode_raim_flag(self):
        self.assertEqual(self.aisMessage.payloadInfo["RAIM Flag"], 0)
        self.assertEqual(self.aisMessage2.payloadInfo["RAIM Flag"], 0)

if __name__ == '__main__':
    unittest.main()
