from maionline.abstracts.NotCriticalAbstractException import NotCriticalAbstractException


class CourseTestNotFoundException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Тест не найден")

class CourseTestNotSetForCourseException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Тест для курса не установлен")

class CourseTestQuestionNotFoundException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Вопроса теста не найден")