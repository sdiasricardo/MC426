import os
from email.message import EmailMessage
import ssl
import smtplib
from userclass import WeatherForecastUser 


EMAIL_SENDER = 'weatherforecastunicamp@gmail.com'
PASSWORD = "qvko zxsn zaqy fjyu"
EMAIL_TO_FIND = 'viniciusseidel2@gmail.com'

RISCO = {
    0: 'BAIXO',
    1: 'MEDIO',
    2: 'ALTO'
}

# Get user data
user = WeatherForecastUser(csv_file_path='user_data_sample.csv', email=EMAIL_TO_FIND)

subject = 'Risco de chuva em sua regiao'

body = """
Prezado(a) usuario(a) {NOME} do Weather Forecast Unicamp \n\n 
Enviamos por meio deste email um alerta de risco {RISCO_ATUAL} de chuva em sua regiao {CIDADE}.
"""

if user.get_user_receive_email() == True and user.get_user_email() is not None:

    body = body.format(NOME=user.get_user_name(), RISCO_ATUAL=RISCO[user.get_user_risk()], CIDADE=user.get_user_city())

    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = user.get_user_email()
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, PASSWORD)
        smtp.sendmail(EMAIL_SENDER, user.get_user_email(), em.as_string())

    print('Email sent to user.')

else:
    print('Email not sent to user because the user does not want to receive emails or email is not valid.')