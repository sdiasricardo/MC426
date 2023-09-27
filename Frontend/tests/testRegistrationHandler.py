import unittest
import sys
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
sys.path.append(parent_directory + "/Models")
from Models.User import User
from RegistrationHandler import RegistrationHandler
from Enums.UserSituation import UserSituation


class RegistrationHandlerTest(unittest.TestCase):
    def setUp(self):
        self.registration_handler = RegistrationHandler(DatabaseConnectionMock())

    def test_register_duplicate_username(self):
        user1 = User("nome1", "email1", "senha1", "", True)
        user2 = User("nome1", "email2", "senha2", "", True)

        response1 = self.registration_handler.register(user1)
        response2 = self.registration_handler.register(user2)

        self.assertEqual(UserSituation.USERNAME_TAKEN, response2)

    def test_register_duplicate_email(self):
        user1 = User("nome1", "email1", "senha1", "", True)
        user2 = User("nome2", "email1", "senha2", "", True)

        response1 = self.registration_handler.register(user1)
        response2 = self.registration_handler.register(user2)

        self.assertEqual(UserSituation.EMAIL_TAKEN, response2)

    def test_register_valid_user(self):
        user = User("nome1", "email1", "senha1", "", True)

        response = self.registration_handler.register(user)

        self.assertEqual(UserSituation.SUCCESS, response)


class DatabaseConnectionMock:

    def __init__(self):
        self.user_list = []

    def user_exists(self, name, email):

        for user in self.user_list:
            if user.Email == email:
                return UserSituation.EMAIL_TAKEN

            elif user.Name == name:
                return UserSituation.USERNAME_TAKEN

        return UserSituation.SUCCESS

    def create_user(self, user):
        self.user_list.append(user)


if __name__ == '__main__':
    unittest.main()
