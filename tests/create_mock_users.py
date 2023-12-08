import os
from email.message import EmailMessage
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory) 

from Entities.User import User
from Services.DataPlot.DataHandler import DataHandler
from ExternalConnections.database.DatabaseConnection import DatabaseConnection

# This file creates mock users to be used in the tests

class DatabaseConnectionMock:

    def __init__(self):
        self.user_list = []

    def user_exists(self, name, email):

        for user in self.user_list:
            if user.Email == email:
                return UserSituation.EMAIL_TAKEN

            elif user.Name == name:
                return UserSituation.USERNAME_TAKEN

        return UserSituation.SUCCESS

    def create_user(self, user):
        self.user_list.append(user)


def create_mock_users():

    db = DatabaseConnectionMock()

    user1 = User("nome1", "email1", "senha1", "", True)
    user2 = User("nome2", "email2", "senha2", "", True)
    user3 = User("nome3", "email3", "senha3", "", True)

    db.create_user(user1)
    db.create_user(user2)
    db.create_user(user3)

    return db