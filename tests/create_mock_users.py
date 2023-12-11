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
from Entities.Enums.UserSignupSituation import UserSignupSituation

# This file creates mock users to be used in the tests

class DatabaseConnectionMock:

    def __init__(self):
        self.user_list = []

    def user_exists(self, name, email):

        for user in self.user_list:
            if user.Email == email:
                return UserSignupSituation.EMAIL_TAKEN

            elif user.Name == name:
                return UserSignupSituation.USERNAME_TAKEN

        return UserSignupSituation.SUCCESS

    def create_user(self, user):
        self.user_list.append(user)

    def get_user_list(self):
        return self.user_list


def create_mock_users():

    db = DatabaseConnectionMock()

    user1 = User("id", "Galo", "fernandomarqs12@gmail.com", "senha1", True)


    db.create_user(user1)
    return db
