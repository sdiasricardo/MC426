import unittest
from RegistrationHandler import RegistrationHandler
from Enums.UserSituation import UserSituation


class RegistrationHandlerTest:
    def setUp(self):
        self.registration_handler = RegistrationHandler(DatabaseConnectionMock())







class DatabaseConnectionMock:

    def __init__(self):
        user_list = []

    def test_create_profile(self):
        # Test if a profile is successfully created
        profile_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        result = self.profile_handler.create_profile(profile_data)
        self.

    def user_exists(self, name, email):

        for user in self.user_list:
            if user.email == email:
                return UserSituation.EMAIL_TAKEN

            elif user.name == name:
                return UserSituation.USERNAME_TAKEN

        return UserSituation.USER_UNREGISTERED

    def create_user(self, user):
        self.user_list.append(user)
