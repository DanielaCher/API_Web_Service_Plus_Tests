import unittest
from app import app, db, FormData

class AppTests(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client() #A test client (self.app) is created to make requests to the Flask application without running the server.
        
        # Initialize the test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Remove the test database after each test
        with app.app_context(): #manually activate an application context
            db.drop_all()



    def test_home_page(self):
        # home page loads correctly
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200) #response status code is 200 (OK)
        self.assertIn('text/html', response.content_type) #response status code is 200 (OK)
    
    
    def test_form_submission(self):
        # form submission process
        response = self.app.post('/process_input', data={
            'user_id': '123',
            'problem_description': 'Test problem',
            'device_serial_number': '24-X-125447-DC',
            'light1': 'off',
            'light2': 'off',
            'light3': 'off'
        })
        self.assertEqual(response.status_code, 200)
        
        # verify data was saved to the database
        with app.app_context():
            entry = FormData.query.first()
            self.assertIsNotNone(entry) #data was saved
            self.assertEqual(entry.user_id, '123') #checks that the user_id matches the submitted value.
        

if __name__ == '__main__':
    unittest.main()