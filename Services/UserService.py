import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory + "/Entities")
sys.path.append(parent_directory + "/ExternalConnections/database")

from DatabaseConnection import DatabaseConnection
from Enums.user_signup_situation import user_signup_situation


class UserService:

    def __init__(self, connection):
        self.Connection = connection

    def register(self, user):

        situation = self.Connection.validate_user_signup(user.Name, user.Email)

        if situation is not user_signup_situation.SUCCESS:
            return situation

        self.Connection.create_user(user)

        return situation

    def validate_user(self, username, password):

        situation = self.Connection.validate_user_login(username, password)

        return situation
