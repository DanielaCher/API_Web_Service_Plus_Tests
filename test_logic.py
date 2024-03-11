import unittest
from app import app, db, FormData, calculate_response_status

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class TestLogic(unittest.TestCase):

    # test cases for calculate_response_status
    def test_calculate_response_status(self):
        
        # Case 1: device_serial_number starts with "24-X"
        self.assertEqual(calculate_response_status("24-X-123", "on", "on", "on"), "Please upgrade your device")
        self.assertEqual(calculate_response_status("24-X-123", "on", "off", "off"), "Please upgrade your device")
        self.assertEqual(calculate_response_status("24-X-123", "blinking", "on", "on"), "Please upgrade your device")
        
        # Case 2: device_serial_number starts with "36-X"
        self.assertEqual(calculate_response_status("36-X-123", "off", "off", "off"), "Turn on the device")
        self.assertEqual(calculate_response_status("36-X-123", "on", "on", "on"), "ALL is ok")
        self.assertEqual(calculate_response_status("36-X-123", "blinking", "blinking", "off"), "Please wait")
        
        # Case 3: device_serial_number starts with "51-B"
        self.assertEqual(calculate_response_status("51-B-123", "off", "off", "off"), "Turn on the device")
        self.assertEqual(calculate_response_status("51-B-123", "blinking", "off", "off"), "Please wait")
        self.assertEqual(calculate_response_status("51-B-123", "on", "on", "off"), "ALL is ok")
        
        # Case 4: Unknown device
        self.assertEqual(calculate_response_status("36-X-123", "off", "on", "on"), "Unknown device")

    # specific scenarios
    def test_device_upgrade(self):
       
        self.assertEqual(calculate_response_status("24-X-123456", "on", "off", "blinking"), "Please upgrade your device")
    
    def test_turn_on_device(self):
        self.assertEqual(calculate_response_status("36-X-789012", "off", "off", "off"), "Turn on the device")
    
    def test_please_wait(self):
        self.assertEqual(calculate_response_status("36-X-345678", "blinking", "on", "blinking"), "Please wait")

if __name__ == '__main__':
    unittest.main()
