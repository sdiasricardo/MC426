import unittest
import json
import email_sender
import userclass

class TestEmailSender(unittest.TestCase):

    def test_verify_data_email(self):
        """Test if the file is a csv file."""
        
        with self.assertRaises(FileNotFoundError):
            email_sender.verify_data_email(csv_file_path='user_data_sample.txt')
            email_sender.verify_data_email(csv_file_path='user_data_sample.json')
    
    def test_email_exists(self):
        """Test if the email exists in the database."""
        
        with self.assertRaises(ValueError):
            email_sender.verify_data_email(email_to_find='vinicius@notgmail.com')

    def test_email_is_sent(self):
        """Test if the email is sent."""
        self.assertEqual(email_sender.send_email(user=userclass.WeatherForecastUser()), 1)

    def test_email_is_not_sent(self):
        """Test if the email is not sent because notification is off"""
        self.assertEqual(email_sender.send_email(user=userclass.WeatherForecastUser(email='weatherforecastunicamp@gmail.com')), -1)

if __name__ == '__main__':
    unittest.main()