from enum import Enum


class UserSignupSituation(Enum):
    SUCCESS = 0
    USERNAME_TAKEN = 1
    EMAIL_TAKEN = 2
