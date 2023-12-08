class User:
    def __init__(self, name, email, password, city, receive_notifications, notification_cache):
        self.Name = name
        self.Email = email
        self.Password = password
        self.City = city
        self.ReceiveNotifications = receive_notifications
        self.NotificationsCache = notification_cache

    def is_same_user(self, user):

        if user.Email == self.Email or user.Name == self.Name:
            return False

        return True
