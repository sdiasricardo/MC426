from enum import Enum

class UserSituation(Enum):
    SUCCESS = 0
    USERNAME_TAKEN = 1
    EMAIL_TAKEN = 2