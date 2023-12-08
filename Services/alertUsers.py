# Pegar todos os usuarios

# Pra cada usuario: ler cada uma das cidades

# Pra cada alerta: ver se ja nao enviou -> se enviou, ignorar

# Se tiver que mandar o alerta, mandar o email com as parada do seidel
import os, sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

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

if __name__ == "__main__":
    check_notification()
    