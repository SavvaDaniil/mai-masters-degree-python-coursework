
from maionline.abstracts.NotCriticalAbstractException import NotCriticalAbstractException

class UserLoginWrongException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Неправильно введены логин или пароль")


class UserNotFoundException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Пользователь не найден")

class UsernameIsAlreadyExistsException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Логин уже существует в базе")

class PasswordCurrentWrongExists(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Текущий пароль введён неверно")