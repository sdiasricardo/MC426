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

        Be advised that a {SEVERITY} weather condition has been reported at: {AREAS}\n\n

        Certainty:\n
            {CERTAINTY}
        Recommended Actions:\n
        {INSTRUCTIONS}
        Kind regards,\n
        Weather426 Team\n

        Note: You are receiving this email because you have subscribed to weather alerts on our app. If this message has reached you in error, please disregard it, and we apologize for any inconvenience caused.
        """

        # Check if the user wants to receive emails
        if user.ReceiveNotifications == True:

            # Format the subject and body of the email
            
            subject = subject.format(NOTE = alert['note'])
            
            body = body.format(NAME=user.Name,
                               AREAS = alert['areas'],
                                SEVERITY= alert['severity'], 
                                CERTAINTY= alert['certainty'],
                                DESC = alert['desc'],
                                INSTRUCTIONS = alert['instruction'])
            
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

db = create_mock_users()
user = db.get_user_list()[0]

alert = {
        "headline":"Flood Warning issued January 05 at 9:47PM EST until January 07 at 6:15AM EST by NWS",
        "msgtype":"Alert",
        "severity":"Moderate",
        "urgency":"Expected",
        "areas":"Calhoun; Lexington; Richland",
        "category":"Met",
        "certainty":"Likely",
        "event":"Flood Warning",
        "note":"Alert for Calhoun; Lexington; Richland (South Carolina) Issued by the National Weather Service",
        "effective":"2021-01-05T21:47:00-05:00",
        "expires":"2021-01-07T06:15:00-05:00",
        "desc":"...The Flood Warning continues for the following rivers in South\nCarolina...\nCongaree River At Carolina Eastman affecting Richland, Calhoun\nand Lexington Counties.\nCongaree River At Congaree National Park-Gadsden affecting\nCalhoun and Richland Counties.\nNorth Fork Edisto River At Orangeburg affecting Orangeburg County.\n...The Flood Warning is now in effect until Thursday morning...\nThe Flood Warning continues for\nthe Congaree River At Carolina Eastman.\n* Until Thursday morning.\n* At 9:28 PM EST Tuesday the stage was 115.6 feet.\n* Flood stage is 115.0 feet.\n* Minor flooding is occurring and minor flooding is forecast.\n* Recent Activity...The maximum river stage in the 24 hours ending\nat 9:28 PM EST Tuesday was 118.2 feet.\n* Forecast...The river will rise to 115.7 feet just after midnight\ntonight. It will then fall below flood stage tomorrow morning to\n114.2 feet and begin rising again tomorrow evening. It will rise\nto 114.3 feet early Thursday morning. It will then fall again and\nremain below flood stage.\n* Impact...At 115.0 feet, Flooding occurs in low lying areas of the\nCarolina Eastman Facility and at the Congaree National Park.\n* Flood History...This crest compares to a previous crest of 116.3\nfeet on 12/03/2020.\n&&",
        "instruction":"A Flood Warning means that flooding is imminent or occurring. All\ninterested parties should take necessary precautions immediately.\nMotorists should not attempt to drive around barricades or drive\ncars through flooded areas.\nCaution is urged when walking near riverbanks.\nAdditional information is available at www.weather.gov.\nThe next statement will be issued Wednesday morning at 1000 AM EST."
        }

EmailSender.send_email(user, alert, 'teste')