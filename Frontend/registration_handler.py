import database_connection


class RegistrationHandler:

    def __init__(self, connection):
        self.Connection = connection

    def register(self, user):
        if not self.Connection.user_exists(user.Name, user.Email):

            self.Connection.create_user(user)
            return True

        return False
