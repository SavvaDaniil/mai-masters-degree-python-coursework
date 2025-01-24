
from django.forms import Form, CharField


class UserLoginForm(Form):
    """Форма для аутентификации пользователя"""
    username: CharField = CharField(max_length=512, required=True)
    password: CharField = CharField(max_length=512, required=True)

class UserProfileForm(Form):
    """Форма редактирования профиля пользователя"""
    username: CharField = CharField(max_length=512, required=True)
    firstname: CharField = CharField(max_length=512, required=False)
    lastname: CharField = CharField(max_length=512, required=False)
    patronymic: CharField = CharField(max_length=512, required=False)

    password_new: CharField = CharField(max_length=512, required=False)
    password_new_again: CharField = CharField(max_length=512, required=False)
    password: CharField = CharField(max_length=512, required=False)
