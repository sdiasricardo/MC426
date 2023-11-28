import unittest
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory + "/Entities")
sys.path.append(parent_directory + "/Entities/Enums")
sys.path.append(parent_directory + "/Services")
#sys.path.append(parent_directory + "/Frontend" + "/Models")
from User import User
from UserService import UserService
from Enums.user_signup_situation import user_signup_situation


class UserServiceTest(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService(DatabaseConnectionMock())

    def test_register_duplicate_username(self):
        user1 = User("nome1", "email1", "senha1", "", True)
        user2 = User("nome1", "email2", "senha2", "", True)

        response1 = self.user_service.register(user1)
        response2 = self.user_service.register(user2)

        self.assertEqual(user_signup_situation.USERNAME_TAKEN, response2)

    def test_register_duplicate_email(self):
        user1 = User("nome1", "email1", "senha1", "", True)
        user2 = User("nome2", "email1", "senha2", "", True)

        response1 = self.user_service.register(user1)
        response2 = self.user_service.register(user2)

        self.assertEqual(user_signup_situation.EMAIL_TAKEN, response2)

    def test_register_valid_user(self):
        user = User("nome1", "email1", "senha1", "", True)

        response = self.user_service.register(user)

        self.assertEqual(user_signup_situation.SUCCESS, response)

    def test_login_wrong_password(self):
        user = User("nome1", "email1", "senha1", "", True)

        self.user_service.register(user)

        response = self.user_service.login(user.Name, "")

        self.assertFalse(response)

    def test_login_wrong_username(self):
        user = User("nome1", "email1", "senha1", "", True)

        self.user_service.register(user)

        response = self.user_service.login("", "senha1")

        self.assertFalse(response)

    def test_login_success(self):
        user = User("nome1", "email1", "senha1", "", True)

        self.user_service.register(user)

        response = self.user_service.login(user.Name, user.Password)

        self.assertTrue(response)

class DatabaseConnectionMock:

    def __init__(self):
        self.user_list = []

    def create_user(self, user):
        self.user_list.append(user)


    def validate_user_signup(self, username, email):
        for user in self.user_list:

            if user.Name == username:

                return user_signup_situation.USERNAME_TAKEN

            if user.Email == email:

                return user_signup_situation.EMAIL_TAKEN

        return user_signup_situation.SUCCESS

    def validate_user_login(self, username, password):

        for user in self.user_list:

            if user.Name == username and user.Password == password:

                return True

        return False

if __name__ == '__main__':
    unittest.main()
