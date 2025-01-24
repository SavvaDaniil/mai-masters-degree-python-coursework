from maionline.abstracts.NotCriticalAbstractException import NotCriticalAbstractException


class CourseLessonNotFoundException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Урок не найден")


class CourseLessonNotConnectedToCourseException(NotCriticalAbstractException):
    def __init__(self):
        super().__init__("Урок не относится к курсу")