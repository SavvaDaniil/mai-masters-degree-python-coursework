from maionline.abstracts.NotCriticalAbstractException import NotCriticalAbstractException


class UserCourseAccessNotFoundException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Доступ пользователя не найден")
