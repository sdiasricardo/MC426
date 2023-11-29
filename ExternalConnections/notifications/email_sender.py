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
from Services.DataPlot.DataHandler import DataHandler

# Constants to send email
EMAIL_SENDER = 'weatherforecastunicamp@gmail.com'
PASSWORD = "qvko zxsn zaqy fjyu"
EMAIL_TO_FIND = 'viniciusseidel2@gmail.com'

# Risk level in the dictionary
RISCO = {
    0: 'BAIXO',
    1: 'MÉDIO',
    2: 'ALTO'
}


def send_email(user: User):
    """Given an valid WeatherForecast user this function sends an email to the user with the weather forecast."""
    
    # Email subject and body
    subject = '[ATENÇÃO] Risco de chuva {RISCO_ATUAL} em sua região'

    body = """ 
    Caro usuário {NOME} do Weather Forecast Unicamp \n
    Enviamos por meio deste email um alerta de risco {RISCO_ATUAL} de chuva em sua região {CIDADE}.
    Para mais informações, acesse o site do Weather Forecast Unicamp em https://weather-forecast-unicamp.herokuapp.com/ \n
    """

    # Check if the user wants to receive emails
    if user.ReceiveNotifications() == True:

        # Format the subject and body of the email

        alert_dict = DataHandler.get_alerts(user.City())
        
        
        subject = subject.format(RISCO_ATUAL=RISCO[user.get_user_risk()])
        
        body = body.format(NOME=user.Name, 
                            RISCO_ATUAL=RISCO[user.get_user_risk()], 
                            CIDADE=user.City())

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