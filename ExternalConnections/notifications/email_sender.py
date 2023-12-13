import os
from email.message import EmailMessage
import ssl
import smtplib
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory) 

from Services.DataPlot.DataProcessor import DataProcessor
from tests.create_mock_users import create_mock_users
# Constants to send email
EMAIL_SENDER = 'weatherforecastunicamp@gmail.com'
PASSWORD = "qvko zxsn zaqy fjyu"


class EmailSender:

    @staticmethod
    def send_email(user, alert, city):

        
        """Given an valid WeatherForecast user this function sends an email to the user with the weather forecast."""

        print("Sending email to user: ", user.Name)
        
        # Email subject and body
        subject = '[WEATHER ALERT] {NOTE}'

        body = """ 
        Dear {NAME},

        Be advised that a {SEVERITY} weather condition has been reported at: {AREAS}

        Certainty: {CERTAINTY}\n
        Recommended Actions:
        {INSTRUCTIONS}\n
        Kind regards,
        Weather426 Team

        Note: You are receiving this email because you have subscribed to weather alerts on our app. If this message has reached you in error, please disregard it, and we apologize for any inconvenience caused.
        """

        # Check if the user wants to receive emails
        if user.ReceiveNotifications == True:

            # Format the subject and body of the email
            
            subject = subject.format(NOTE = alert['note'])
            
            INSTRUCTIONS = alert['instruction'].replace('\n', ' ')
            body = body.format(NAME=user.Name,
                                AREAS = alert['areas'],
                                SEVERITY= alert['severity'], 
                                CERTAINTY= alert['certainty'],
                                DESC = alert['desc'],
                                INSTRUCTIONS = INSTRUCTIONS)
            
            em = EmailMessage()
            em['From'] = EMAIL_SENDER
            em['To'] = user.Email
            em['Subject'] = subject
            em.set_content(body)

            # Send email
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(EMAIL_SENDER, PASSWORD)
                smtp.sendmail(EMAIL_SENDER, user.Email, em.as_string())

            # returns para testes
            return 1 

        else:
            return -1