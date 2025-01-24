


class NotCriticalAbstractException(Exception):
    """Условно абстрактный класс для ошибок, текст который позволительно обрабатывать на стороне frontend"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)