import unittest
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
absolute_directory = os.path.dirname(parent_directory)
sys.path.append(absolute_directory)

# Go to the parent directory and import the module
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Entities.User import User
from Entities.Enums.UserSignupSituation import UserSignupSituation
from Services.UserService import UserService

class DatabaseConnectionMock:

    def __init__(self):
        self.user_list = []

    def create_user(self, user):
        self.user_list.append(user)

    def validate_user_signup(self, username, email):
        for user in self.user_list:
            if user.Name == username:
                return UserSignupSituation.USERNAME_TAKEN

            if user.Email == email:
                return UserSignupSituation.EMAIL_TAKEN

        return UserSignupSituation.SUCCESS

    def validate_user_login(self, username, password):
        for user in self.user_list:
            if user.Name == username and user.Password == password:
                return UserSignupSituation.SUCCESS
            
        return False

class TestUserService(unittest.TestCase):

    def setUp(self):
        # Configuração inicial, se necessário
        self.connection = DatabaseConnectionMock() 
        self.userService = UserService(self.connection)

    def tearDown(self):
        # Limpeza após cada teste, se necessário
        pass

    def test_register_user_success(self):
        # Classe de equivalência: Registro de usuário com sucesso
        user = User(id=1, name="John Doe", email="john.doe@example.com", password="password123", receive_notifications=True)
        result = self.userService.register(user)
        self.connection.validate_user_signup(user.Name, user.Password)
        self.assertEqual(result, UserSignupSituation.SUCCESS)

    def test_register_user_username_taken(self):
        # Classe de equivalência: Nome de usuário já registrado
        user1 = User(id=1, name="John Doe", email="john1.doe@example.com", password="password123", receive_notifications=True)
        user2 = User(id=1, name="John Doe", email="john2.doe@example.com", password="password123", receive_notifications=True)

        self.connection.create_user(user1)
        result = self.userService.register(user2)

        self.assertEqual(result, UserSignupSituation.USERNAME_TAKEN)

    def test_register_user_email_taken(self):
        # Classe de equivalência: E-mail já registrado
        user1 = User(id=1, name="John Doe1", email="john.doe@example.com", password="password123", receive_notifications=True)
        user2 = User(id=1, name="John Doe2", email="john.doe@example.com", password="password123", receive_notifications=True)

        self.connection.create_user(user1)
        result = self.userService.register(user2)

        self.assertEqual(result, UserSignupSituation.EMAIL_TAKEN)

    def test_login_user_success(self):
        # Classe de equivalência: Login de usuário com sucesso
        user1 = User(id=1, name="john.doe", email="john.doe@example.com", password="password123", receive_notifications=True)
        self.connection.create_user(user1)

        username = "john.doe"
        password = "password123"
    
        result = self.userService.login(username, password)
        self.assertEqual(result, UserSignupSituation.SUCCESS)

    def test_login_user_invalid_credentials(self):
        # Classe de equivalência: Credenciais de login inválidas
        user1 = User(id=1, name="john", email="john.doe@example.com", password="password123", receive_notifications=True)
        self.connection.create_user(user1)

        username = "john.doe"
        password = "password123"
    
        result = self.userService.login(username, password)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()