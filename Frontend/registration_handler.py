import database_connection


class RegistrationHandler:

    def __init__(self, connection):
        self.Connection = connection

    def register(self, user):
        return self.Connection.user_exists(user.Name, user.Email)

