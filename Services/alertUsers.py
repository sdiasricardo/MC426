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
from email_sender import EmailSender

class AlertUsers:
    def __init__(self):
        self.dbconnection = DatabaseConnection()
        self.users = self.dbconnection.get_all_users()

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

    def manage_alerts(self, user, alert_list):
        #se diferenca de tempo com expired for positiva -> tira o alerta
        #se diferenca de tempo com effective for <= -1 -> nao faz nada
        #se diferenca de tempo com effective for >= 0 e diferenca de tempo com expired for <= 0 -> manda o alerta
        #teste = [{'expires': "2024-05-20T12:00:00-03:00", 'effective': "2024-05-20T12:00:00-03:00"}]
        for alert in alert_list:
            #expired_date = alert["expires"]
            effective_date = alert["effective"]
            #get utc offset
            effective_date = effective_date[:-3]
            utc = (int(effective_date[-1]) + int((10 * effective_date[-2])))
            if effective_date[-3] == "-":
                utc = -utc
            #remove last 5 digits of string
            #expired_date = expired_date[:-3]
            effective_date = effective_date[:-3]
            #expired_delta = self.calculate_time_difference(expired_date, utc)
            effective_delta = self.calculate_time_difference(effective_date, utc)
            if effective_delta.days == 0:
                print("mandar alert")
                EmailSender.send_email(user, alert[0], alert[1])
                #TODO -> mandar alerta
                #ver oq tem q passar pro email, e lançar no email_sender.py
            #se passou do elif, ambos sao negativos, ainda nao esta na hora de mandar o alerta, deixa ficar na cache


    def check_notification(self):  
        for user in self.users:
            alert_list = list()
            if user.ReceiveNotifications:
                processor = DataProcessor()
                for city in user.Cities:
                    alerts = processor.get_alerts(city)
                    for alert in alerts:
                        alert_list.append(tuple([alert, city]))
                self.manage_alerts(user, alert_list)

if __name__ == "__main__":
    alert = AlertUsers()
    alert.check_notification()
    