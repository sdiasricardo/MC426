from enum import Enum

class user_login_situation(Enum):
    SUCCESS = 0
    USERNAME_TAKEN = 1
    WRONG_PASSWORD = 2