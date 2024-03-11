import unittest
from app import app, db
from bs4 import BeautifulSoup


class TestInputValidation(unittest.TestCase):

    #setUp and tearDown are used to prepare the test environment before each test method

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def submit_and_validate(self, form_data, expected_errors):
        response = self.app.post('/process_input', data=form_data)
        soup = BeautifulSoup(response.data, 'html.parser')
        error_messages = [li.text for li in soup.find_all('li')] 

        for expected_error in expected_errors:
            self.assertIn(expected_error, error_messages, f"Expected error message not found: {expected_error}")

    def test_user_id_validation(self):
    # Non-digit user ID
        form_data = {
            'user_id': 'abc',
            'problem_description': 'Test Problem',
            'device_serial_number': '24-X-125447-DC',
            'light1': 'on', 'light2': 'on', 'light3': 'off'
        }
        expected_errors = ['Invalid user ID.']
        self.submit_and_validate(form_data, expected_errors)

    def test_user_id_validation_2(self):
    # None user ID
        form_data = {
            'user_id': None,
            'problem_description': 'Test Problem',
            'device_serial_number': '24-X-125447-DC',
            'light1': 'on', 'light2': 'on', 'light3': 'off'
        }
        expected_errors = ['Invalid user ID.']
        self.submit_and_validate(form_data, expected_errors)

    def test_problem_description_validation(self):
    # Problem_description exceeding 300 characters
        long_description = 'a' * 301
        form_data = {
            'user_id': '123',
            'problem_description': long_description,
            'device_serial_number': '24-X-125447-DC',
            'light1': 'on', 'light2': 'on', 'light3': 'off'
        }
        expected_errors = ['Problem description cannot exceed 300 characters.']
        self.submit_and_validate(form_data, expected_errors)

    def test_device_serial_number_validation(self):
    # Device_serial_number exceeding 64 characters
        long_serial_number = 'X' * 65
        form_data = {
            'user_id': '123',
            'problem_description': 'Test Problem',
            'device_serial_number': long_serial_number,
            'light1': 'on', 'light2': 'on', 'light3': 'off'
        }
        expected_errors = ['Device serial number cannot exceed 64 characters.']
        self.submit_and_validate(form_data, expected_errors)

    def test_lights_status_validation(self):
    # Missing status for all indicator lights
        form_data = {
            'user_id': '123',
            'problem_description': 'Test Problem',
            'device_serial_number': '24-X-125447-DC',
            'light1': None, 'light2': 'on', 'light3': 'off'
        }
        expected_errors = ['Please select a status for all indicator lights.']
        self.submit_and_validate(form_data, expected_errors)

    def test_multiple_errors(self):
    # Multiple validation errors
        form_data = {
            'user_id': 'abc',  # Invalid user ID (non-digit)
            'problem_description': 'a' * 301,  # Exceeds 300 characters
            'device_serial_number': 'X' * 65,  # Exceeds 64 characters
            'light1': 'on', 'light2': None, 'light3': 'off'  # Missing status for light2
        }
                
        expected_errors = [
            'Invalid user ID.',
            'Problem description cannot exceed 300 characters.',
            'Device serial number cannot exceed 64 characters.',
            'Please select a status for all indicator lights.'
            ]
        self.submit_and_validate(form_data, expected_errors)
                   

    def test_invalid_serial_number_and_light_status(self):
    # 2 validation errors    
        form_data = {
                'user_id': '123',
                'problem_description': 'Valid description',
                'device_serial_number': '',  # Invalid empty serial number
                'light1': 'on', 'light2': None, 'light3': 'off'  # Invalid light status
            }
        expected_errors = [
                'Device serial number is required.',
                'Please select a status for all indicator lights.'
            ]
        self.submit_and_validate(form_data, expected_errors)
            

     

if __name__ == '__main__':
    unittest.main()
