import os
from email.message import EmailMessage
import ssl
import smtplib
from notifications.userclass import WeatherForecastUser 


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

def verify_data_email(csv_file_path = 'user_data_sample.csv', email_to_find=EMAIL_TO_FIND):
    # Get user data from the class WeatherForecastUser
    if os.path.exists(csv_file_path):
        if csv_file_path.endswith('.csv'):
            user = WeatherForecastUser(csv_file_path=csv_file_path, email=email_to_find)

        else:
            raise TypeError('The file must be a csv file.')
    
    else:
        raise FileNotFoundError('The file does not exist.')
    
    return user, 1

def send_email(user: WeatherForecastUser):
    """Given an valid WeatherForecast user this function sends an email to the user with the weather forecast."""
    
    # Email subject and body
    subject = '[ATENÇÃO] Risco de chuva {RISCO_ATUAL} em sua região'

    body = """ 
    Caro usuário {NOME} do Weather Forecast Unicamp \n
    Enviamos por meio deste email um alerta de risco {RISCO_ATUAL} de chuva em sua região {CIDADE}.
    Para mais informações, acesse o site do Weather Forecast Unicamp em https://weather-forecast-unicamp.herokuapp.com/ \n
    """

    # Check if the user wants to receive emails and if the email exists in the user database
    if user.get_user_receive_email() == True and user.get_user_email() is not None:

        # Format the subject and body of the email
        subject = subject.format(RISCO_ATUAL=RISCO[user.get_user_risk()])
        
        body = body.format(NOME=user.get_user_name(), 
                            RISCO_ATUAL=RISCO[user.get_user_risk()], 
                            CIDADE=user.get_user_city())

        em = EmailMessage()
        em['From'] = EMAIL_SENDER
        em['To'] = user.get_user_email()
        em['Subject'] = subject
        em.set_content(body)

        # Send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, PASSWORD)
            smtp.sendmail(EMAIL_SENDER, user.get_user_email(), em.as_string())

        return 1

    else:
        return -1