class User:
    def __init__(self, name, email, password):
        self.Name = name
        self.Email = email
        self.Password = password

    def is_same_user(self, user):

        if user.Email == self.Email or user.Name == self.Name:
            return False

        return True
