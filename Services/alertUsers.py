# Pegar todos os usuarios

# Pra cada usuario: ler cada uma das cidades

# Pra cada alerta: ver se ja nao enviou -> se enviou, ignorar

# Se tiver que mandar o alerta, mandar o email com as parada do seidel
import os, sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from datetime import datetime, timedelta
from Services.DataPlot.DataProcessor import DataProcessor
from ExternalConnections.database.DatabaseConnection import DatabaseConnection
from tests.create_mock_users import create_mock_users

db = create_mock_users()
users = DatabaseConnection.get_all_users(db)

def check_notification():
    for user in users:
        print(user.Name)
        print(user.Email)
        print(user.City)
        print(user.ReceiveNotifications)
        print("")
        if user.ReceiveNotifications:
            processor = DataProcessor()
            for city in user.City:
                alerts = processor.get_alerts(city)
                for alert in alerts:
                    if alert not in user.NotificationCache:
                        user.NotificationCache.append(alert)
            check_alerts(user)

def calculate_time_difference(date_str, timezone_offset):
    # Parse the input date string
    input_date = datetime.fromisoformat(date_str)

    # Apply the time zone offset to the input date
    input_date_utc = input_date - timedelta(hours=timezone_offset)

    # Get the current UTC time
    current_utc_time = datetime.utcnow()

    # Apply the time zone offset to the current UTC time
    current_time_with_offset = current_utc_time - timedelta(hours=timezone_offset)

    # Calculate the time difference
    time_difference = current_time_with_offset - input_date_utc

    return time_difference

def check_alerts(user):
    #se diferenca de tempo com expired for positiva -> tira o alerta
    #se diferenca de tempo com effective for <= -1 -> nao faz nada
    #se diferenca de tempo com effective for >= 0 e diferenca de tempo com expired for <= 0 -> manda o alerta
    #teste = [{'expires': "2024-05-20T12:00:00-03:00", 'effective': "2024-05-20T12:00:00-03:00"}]
    for alert in user.NotificationCache:
        expired_date = alert["expires"]
        effective_date = alert["effective"]
        #get utc offset
        expired_date = expired_date[:-3]
        utc = (int(expired_date[-1]) + int((10 * expired_date[-2])))
        if expired_date[-3] == "-":
            utc = -utc
        #remove last 5 digits of string
        expired_date = expired_date[:-3]
        effective_date = effective_date[:-6]
        expired_delta = calculate_time_difference(expired_date, utc)
        effective_delta = calculate_time_difference(effective_date, utc)
        if expired_delta.days >= 0:
            user.NotificationCache.remove(alert)
        elif effective_delta.days >= 0:
            print("mandar alert")
            #TODO -> mandar alerta
            #ver oq tem q passar pro email, e lançar no email_sender.py

            user.NotificationCache.remove(alert)
        #se passou do elif, ambos sao negativos, ainda nao esta na hora de mandar o alerta, deixa ficar na cache

if __name__ == "__main__":
    check_alerts()
    