from enum import Enum

class user_signup_situation(Enum):
    SUCCESS = 0
    USERNAME_TAKEN = 1
    EMAIL_TAKEN = 2