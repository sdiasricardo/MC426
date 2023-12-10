class User:

    def __init__(self, id=None, name=None, email=None, password=None, receive_notifications=False):
        self.Id = id
        self.Name = name
        self.Email = email
        self.Password = password
        self.Cities = []
        self.ReceiveNotifications = receive_notifications

    def is_same_user(self, user):

        if user.Email == self.Email or user.Name == self.Name:
            return False

        return True
