import os
from email.message import EmailMessage
import ssl
import smtplib
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory) 

from Entities.User import User
from Services.DataPlot.DataProcessor import DataProcessor
from ExternalConnections.database.DatabaseConnection import DatabaseConnection
from tests.create_mock_users import create_mock_users

# Constants to send email
EMAIL_SENDER = 'weatherforecastunicamp@gmail.com'
PASSWORD = "qvko zxsn zaqy fjyu"
EMAIL_TO_FIND = 'viniciusseidel2@gmail.com'

db = create_mock_users()

# Using the DatabaseCOnnection get all users
users = DatabaseConnection.get_all_users(db)

print(users[0].City)

def send_email(user):
    """Given an valid WeatherForecast user this function sends an email to the user with the weather forecast."""

    print("Sending email to user: ", user.Name)
    
    # Email subject and body
    subject = '[ATENÇÃO] Risco de chuva {RISCO_ATUAL} em sua região'

    body = """ 
    Caro usuário {NOME} do Weather Forecast Unicamp \n
    Enviamos por meio deste email um alerta de risco {RISCO_ATUAL} de chuva em sua região {CIDADE}.
    Para mais informações, acesse o site do Weather Forecast Unicamp em https://weather-forecast-unicamp.herokuapp.com/ \n
    """

    # Check if the user wants to receive emails
    if user.ReceiveNotifications == True:

        # Format the subject and body of the email
        
        processor = DataProcessor()
        alert_dict = processor.get_alerts(user.City)
        print(alert_dict)
        
        # subject = subject.format(RISCO_ATUAL=RISCO[user.get_user_risk()])
        
        # body = body.format(NOME=user.Name, 
        #                     RISCO_ATUAL=RISCO[user.get_user_risk()], 
        #                     CIDADE=user.City())

        em = EmailMessage()
        em['From'] = EMAIL_SENDER
        em['To'] = user.Email()
        em['Subject'] = subject
        em.set_content(body)

        # Send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, PASSWORD)
            smtp.sendmail(EMAIL_SENDER, user.Email(), em.as_string())

        return 1

    else:
        return -1

