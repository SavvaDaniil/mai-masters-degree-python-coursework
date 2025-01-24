from django.contrib.auth.models import User

from maionline.models import UserData
from typing import Union


class UserDataRepository():

    def find_by_user(self, user: User) -> Union[UserData, None]:
        try:
            return UserData.objects.filter().get(user=user)
        except UserData.DoesNotExist:
            return None