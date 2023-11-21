import unittest
import os, sys


current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
sys.path.append(parent_directory + "/ExternalConnections/notifications")

from email_sender import verify_data_email, send_email
from userclass import WeatherForecastUser

class TestEmailSender(unittest.TestCase):

    def test_verify_data_email(self):
        """Test if the file is a csv file."""
        
        with self.assertRaises(FileNotFoundError):
            verify_data_email(csv_file_path='user_data_sample.txt')
            verify_data_email(csv_file_path='user_data_sample.json')
    
    def test_email_exists(self):
        """Test if the email exists in the database."""
        
        with self.assertRaises(ValueError):
            verify_data_email(email_to_find='vinicius@notgmail.com')

    def test_email_is_sent(self):
        """Test if the email is sent."""
        self.assertEqual(send_email(user=WeatherForecastUser()), 1)

    def test_email_is_not_sent(self):
        """Test if the email is not sent because notification is off"""
        self.assertEqual(send_email(user=WeatherForecastUser(email='weatherforecastunicamp@gmail.com')), -1)

if __name__ == '__main__':
    unittest.main()