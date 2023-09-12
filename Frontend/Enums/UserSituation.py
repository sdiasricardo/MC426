from enum import Enum

class UserSituation(Enum):
    USER_UNREGISTERED = 0
    USERNAME_TAKEN = 1
    EMAIL_TAKEN = 2