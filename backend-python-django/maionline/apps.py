from django.apps import AppConfig


class MaionlineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maionline'
    
    def ready(self):
        pass
        # from typing import Union
        # from django.contrib.auth.models import User
        # from maionline.repository.UserRepository import UserRepository

        # userRepository: UserRepository = UserRepository()
        # userDefault: Union[User, None] = userRepository.find_by_username("admin")
        # if userDefault is None:
        #     userDefault = User()
        #     userDefault.is_active = True
        #     userDefault.is_authenticated = True
        #     userDefault.is_superuser = True
        #     userDefault.set_password("master")
        #     userDefault.save()
