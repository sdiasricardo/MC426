import os
from email.message import EmailMessage
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(parent_directory)

from Entities.User import User
from Services.DataPlot.DataHandler import DataHandler
from ExternalConnections.database.DatabaseConnection import DatabaseConnection
from Entities.Enums.user_signup_situation import user_signup_situation

# This file creates mock users to be used in the tests

class DatabaseConnectionMock:

    def __init__(self):
        self.user_list = []

    def user_exists(self, name, email):

        for user in self.user_list:
            if user.Email == email:
                return user_signup_situation.EMAIL_TAKEN

            elif user.Name == name:
                return user_signup_situation.USERNAME_TAKEN

        return user_signup_situation.SUCCESS

    def create_user(self, user):
        self.user_list.append(user)


def create_mock_users():

    db = DatabaseConnectionMock()

    user1 = User("Galo", "email1", "senha1", "Campinas", True)
    user2 = User("Saia", "email2", "senha2", "Manaus", True)
    user3 = User("Lofi", "email3", "senha3", "Fortaleza", True)

    db.create_user(user1)
    db.create_user(user2)
    db.create_user(user3)

    return db