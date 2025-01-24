
from django.contrib.auth.models import User
#from django.db.models import Q
from typing import Union

from maionline.customException.UserCustomException import UserNotFoundException

class UserRepository():

    def is_exists_by_username_except_id(self, user_id: int, username: str) -> bool:
        return User.objects.exclude(id=user_id).filter(username=username).exists()


    def find_by_id(self, user_id: int) -> Union[User, None]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    def find_by_username(self, username: str) -> Union[User, None]:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
            