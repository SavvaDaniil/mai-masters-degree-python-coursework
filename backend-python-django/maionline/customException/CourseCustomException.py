from maionline.abstracts.NotCriticalAbstractException import NotCriticalAbstractException



class CourseNotFoundException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Курс не найден")

class CourseAccessDeniedForUserException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Доступ к курсу закрыт. Если это ошибка, обратитесь пожалуйста к преподавателю или администратору системы.")
