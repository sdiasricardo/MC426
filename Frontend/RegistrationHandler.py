from DatabaseConnection import DatabaseConnection
from Enums.UserSituation import UserSituation


class RegistrationHandler:

    def __init__(self, connection):
        self.Connection = connection

    def register(self, user):

        situation = self.Connection.user_exists(user.Name, user.Email)

        if situation is not UserSituation.SUCCESS:
            return situation

        self.Connection.create_user(user)

        return situation

