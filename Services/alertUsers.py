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
from ExternalConnections.notifications.email_sender import EmailSender

class AlertUsers:
    def __init__(self):
        self.dbconnection = DatabaseConnection()
        self.users = self.dbconnection.get_all_users()

    def calculate_time_difference(date_str, timezone_offset):
        input_date = datetime.fromisoformat(date_str)
        input_date_utc = input_date - timedelta(hours=timezone_offset)
        current_utc_time = datetime.utcnow()
        current_time_with_offset = current_utc_time - timedelta(hours=timezone_offset)
        time_difference = current_time_with_offset - input_date_utc

        return time_difference
    
    def get_utc(self, date_str):
        aux_date = date_str[:-3]
        utc = (int(aux_date[-1]) + int((10 * aux_date[-2])))
        if aux_date[-3] == "-":
            utc = -utc
        return utc

    def manage_alerts(self, user, alert_list):
        for alert in alert_list:
            effective_date = alert["effective"]
            utc = self.get_utc(effective_date)
            effective_date = effective_date[:-6]
            effective_delta = self.calculate_time_difference(effective_date, utc)
            if effective_delta.days == 0:
                print("Enviando email")
                EmailSender.send_email(user, alert[0], alert[1])


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