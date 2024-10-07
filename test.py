import unittest
import ais_decoder
import math

class test_AIS_decoder(unittest.TestCase):
    def assert_close(self, a, b, abs_tol=0.1):
        if not math.isclose(a, b, abs_tol=abs_tol):
            raise AssertionError(f"{a} and {b} are not close enough")
        
class test_decode_position_report_class_a(test_AIS_decoder):
    def setUp(self):
        self.testMessage = "!AIVDM,1,1,,A,13QWhR012COJ`0TDSdkCS2ph0@=j,0*6C"
        self.testMessage2 = "!AIVDM,1,1,,B,11mg=5OP00Pdu`JI>lS59Ov<0<0g,0*49"
        self.aisMessage = ais_decoder.AISMessage(self.testMessage).decode()
        self.aisMessage2 = ais_decoder.AISMessage(self.testMessage2).decode()
    
    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payload_info["MMSI"], 236581000)
        self.assertEqual(self.aisMessage2.payload_info["MMSI"], 123456789)

    def test_decode_navigation_status(self):
        self.assertEqual(self.aisMessage.payload_info["Navigation Status"], 0)
        self.assertEqual(self.aisMessage2.payload_info["Navigation Status"], 15)

    def test_decode_rate_of_turn(self):
        self.assert_close(self.aisMessage.payload_info["Rate of Turn"], 0.7)
        self.assert_close(self.aisMessage2.payload_info["Rate of Turn"], -127)

    def test_decode_speed_over_ground(self):
        self.assert_close(self.aisMessage.payload_info["Speed Over Ground"], 14.7)

    def test_decode_position_accuracy(self):
        self.assertEqual(self.aisMessage.payload_info["Position Accuracy"], 0)
        self.assertEqual(self.aisMessage2.payload_info["Position Accuracy"], 1)

    def test_decode_longitude(self):
        self.assert_close(self.aisMessage.payload_info["Longitude"], -8.16)
        self.assert_close(self.aisMessage2.payload_info["Longitude"], 9.82)

    def test_decode_latitude(self):
        self.assert_close(self.aisMessage.payload_info["Latitude"], 35.9)
        self.assert_close(self.aisMessage2.payload_info["Latitude"], 44.09)

    def test_decode_course_over_ground(self):
        self.assert_close(self.aisMessage.payload_info["Course Over Ground"], 90.8)
        self.assert_close(self.aisMessage2.payload_info["Course Over Ground"], 131.7)

    def test_decode_true_heading(self):
        self.assertEqual(self.aisMessage.payload_info["True Heading"], 92)
        self.assertEqual(self.aisMessage2.payload_info["True Heading"], 511)


class test_decode_base_station_report(test_AIS_decoder):
    def setUp(self):
        self.testMessage = "!AIVDM,1,1,,B,403t?hAuho;N>`Pc:j>Kgq700D2D,0*2C"
        self.testMessage2 = "!AIVDM,1,1,,A,4020tPiuho;N@PoHAPO027G00@9S,0*5B"
        self.aisMessage = ais_decoder.AISMessage(self.testMessage).decode()
        self.aisMessage2 = ais_decoder.AISMessage(self.testMessage2).decode()
    
    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payload_info["MMSI"], 4132801)
        self.assertEqual(self.aisMessage2.payload_info["MMSI"], 2112643)
    
    def test_decode_year(self):
        self.assertEqual(self.aisMessage.payload_info["Year (UTC)"], 2012)
        self.assertEqual(self.aisMessage2.payload_info["Year (UTC)"], 2012)
    
    def test_decode_month(self):
        self.assertEqual(self.aisMessage.payload_info["Month (UTC)"], 3)
        self.assertEqual(self.aisMessage2.payload_info["Month (UTC)"], 3)

    def test_decode_day(self):
        self.assertEqual(self.aisMessage.payload_info["Day (UTC)"], 14)
        self.assertEqual(self.aisMessage2.payload_info["Day (UTC)"], 14)
    
    def test_decode_hour(self):
        self.assertEqual(self.aisMessage.payload_info["Hour (UTC)"], 11)
        self.assertEqual(self.aisMessage2.payload_info["Hour (UTC)"], 11)
    
    def test_decode_minute(self):
        self.assertEqual(self.aisMessage.payload_info["Minute (UTC)"], 30)
        self.assertEqual(self.aisMessage2.payload_info["Minute (UTC)"], 30)
    
    def test_decode_second(self):
        self.assertEqual(self.aisMessage.payload_info["Second (UTC)"], 14)
        self.assertEqual(self.aisMessage2.payload_info["Second (UTC)"], 16)
    
    def test_decode_position_accuracy(self):
        self.assertEqual(self.aisMessage.payload_info["Position Accuracy"], 1)
        self.assertEqual(self.aisMessage2.payload_info["Position Accuracy"], 1)
    
    def test_decode_longitude(self):
        self.assert_close(self.aisMessage.payload_info["Longitude"], 118.98)
        self.assert_close(self.aisMessage2.payload_info["Longitude"], 12.09)
    
    def test_decode_latitude(self):
        self.assert_close(self.aisMessage.payload_info["Latitude"], 25.22)
        self.assert_close(self.aisMessage2.payload_info["Latitude"], 54.17)

    def test_decode_type_of_electronic_position_fixing_device(self):
        self.assertEqual(self.aisMessage.payload_info["Type of Electronic Position Fixing Device"], 7)
        self.assertEqual(self.aisMessage2.payload_info["Type of Electronic Position Fixing Device"], 7)
    
    def test_decode_raim_flag(self):
        self.assertEqual(self.aisMessage.payload_info["RAIM Flag"], 0)
        self.assertEqual(self.aisMessage2.payload_info["RAIM Flag"], 0)

class test_decode_static_and_voyage_data(test_AIS_decoder):
    def setUp(self):
        self.testMessages = ['!AIVDM,2,1,5,A,53uuBt02<Tg1<<Tv220HTpplThj222222222221?1rc<>Ho<0@0TQCADR0EQ,0*58', '!AIVDM,2,2,5,A,C`888888880,2*02']
        self.testMessages2 = ['!AIVDM,2,1,6,A,55S:>H000000Q3CGW:1@Dp@E:0EQ18E=>222220j1@62240Ht5RBSEBA1C`8,0*1B', '!AIVDM,2,2,6,A,88888888880,2*22']
        self.aisMessage = ais_decoder.AISMessage(self.testMessages).decode()
        self.aisMessage2 = ais_decoder.AISMessage(self.testMessages2).decode()
    
    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payload_info["MMSI"], 266294000)
        self.assertEqual(self.aisMessage2.payload_info["MMSI"], 372412000)
    
    def test_decode_AIS_version(self):
        self.assertEqual(self.aisMessage.payload_info["AIS Version"], 0)
        self.assertEqual(self.aisMessage2.payload_info["AIS Version"], 0)
    
    def test_decode_IMO_number(self):
        self.assertEqual(self.aisMessage.payload_info["IMO Number"], 9212656)
        self.assertEqual(self.aisMessage2.payload_info["IMO Number"], 0)

    def test_decode_call_sign(self):
        self.assertEqual(self.aisMessage.payload_info["Call Sign"], "SCIO")
        self.assertEqual(self.aisMessage2.payload_info["Call Sign"], "HP4592")
    
    def test_decode_vessel_name(self):
        self.assertEqual(self.aisMessage.payload_info["Vessel Name"], "FINNMILL")
        self.assertEqual(self.aisMessage2.payload_info["Vessel Name"], "TENDER EXPRESS")
    
    def test_decode_type_of_ship_and_cargo(self):
        self.assertEqual(self.aisMessage.payload_info["Type of Ship and Cargo"], 79)
        self.assertEqual(self.aisMessage2.payload_info["Type of Ship and Cargo"], 50)
    
    def test_decode_dimensions_to_bow(self):
        self.assertEqual(self.aisMessage.payload_info["Dimensions to Bow"], 15)
        self.assertEqual(self.aisMessage2.payload_info["Dimensions to Bow"], 10)
    
    def test_decode_dimensions_to_stern(self):
        self.assertEqual(self.aisMessage.payload_info["Dimensions to Stern"], 171)
        self.assertEqual(self.aisMessage2.payload_info["Dimensions to Stern"], 6)

    def test_decode_dimensions_to_port(self):
        self.assertEqual(self.aisMessage.payload_info["Dimensions to Port"], 12)
        self.assertEqual(self.aisMessage2.payload_info["Dimensions to Port"], 2)
    
    def test_decode_dimensions_to_starboard(self):
        self.assertEqual(self.aisMessage.payload_info["Dimensions to Starboard"], 14)
        self.assertEqual(self.aisMessage2.payload_info["Dimensions to Starboard"], 2)
    
    def test_decode_position_fixing_device(self):
        self.assertEqual(self.aisMessage.payload_info["Position Fixing Device"], 6)
        self.assertEqual(self.aisMessage2.payload_info["Position Fixing Device"], 1)
    
    def test_decode_ETA_month(self):
        self.assertEqual(self.aisMessage.payload_info["ETA Month"], 3)
        self.assertEqual(self.aisMessage2.payload_info["ETA Month"], 0)    
    
    def test_decode_ETA_day(self):
        self.assertEqual(self.aisMessage.payload_info["ETA Day"], 14)
        self.assertEqual(self.aisMessage2.payload_info["ETA Day"], 0)
    
    def test_decode_ETA_hour(self):
        self.assertEqual(self.aisMessage.payload_info["ETA Hour"], 12)
        self.assertEqual(self.aisMessage2.payload_info["ETA Hour"], 24)
    
    def test_decode_ETA_minute(self):
        self.assertEqual(self.aisMessage.payload_info["ETA Minute"], 0)
        self.assertEqual(self.aisMessage2.payload_info["ETA Minute"], 60)
    
    def test_decode_draught(self):
        self.assert_close(self.aisMessage.payload_info["Draught"], 6.4)
        self.assert_close(self.aisMessage2.payload_info["Draught"], 2.2)
    
    def test_decode_destination(self):
        self.assertEqual(self.aisMessage.payload_info["Destination"], "BREMERHAVEN")
        self.assertEqual(self.aisMessage2.payload_info["Destination"], "IJMUIDEN")

class test_decode_binary_addressed_message(test_AIS_decoder):
    def setUp(self):
        self.testMessage = "!AIVDM,1,1,,A,6h2E:p66B2SR04<0@00000000000,0*4C"
        self.testMessage2 = "!AIVDM,1,1,,A,601uEP@tH;3j<P<j00,4*51"
        self.aisMessage = ais_decoder.AISMessage(self.testMessage).decode()
        self.aisMessage2 = ais_decoder.AISMessage(self.testMessage2).decode()

    def test_decode_MMSI(self):
        self.assertEqual(self.aisMessage.payload_info["MMSI"], 2444000)
        self.assertEqual(self.aisMessage2.payload_info["MMSI"], 2053505)
    
    def test_decode_sequence_number(self):
        self.assertEqual(self.aisMessage.payload_info["Sequence Number"], 1)
        self.assertEqual(self.aisMessage2.payload_info["Sequence Number"], 0)

    def test_decode_destination_MMSI(self):
        self.assertEqual(self.aisMessage.payload_info["Destination MMSI"], 563219000)
        self.assertEqual(self.aisMessage2.payload_info["Destination MMSI"], 253242428)

    def test_decode_retransmit_flag(self):
        self.assertEqual(self.aisMessage.payload_info["Retransmit Flag"], 1)
        self.assertEqual(self.aisMessage2.payload_info["Retransmit Flag"], 1)

    def test_decode_designated_area_code(self):
        self.assertEqual(self.aisMessage.payload_info["Designated Area Code"], 1)
        self.assertEqual(self.aisMessage2.payload_info["Designated Area Code"], 200)
    
    def test_functional_ID(self):
        self.assertEqual(self.aisMessage.payload_info["Functional ID"], 3)
        self.assertEqual(self.aisMessage2.payload_info["Functional ID"], 3)
    
    def test_data(self):
        self.assertEqual(self.aisMessage.payload_info["Data"], "@D@@@@@@@@@@@")
        self.assertEqual(self.aisMessage2.payload_info["Data"], "L @")

    
if __name__ == '__main__':
    unittest.main()
