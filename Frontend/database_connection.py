class DatabaseConnection:
    def __init__(self, connection_string):

        self.ConnectionString = connection_string

    def user_exists(self, name, email):
        return False

    def create_user(self, user):
        return
