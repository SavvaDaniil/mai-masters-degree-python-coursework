
from typing import Union, List
from dataclasses import dataclass
from datetime import datetime



@dataclass
class CourseTestUserLiteViewModel():
    id: int
    user_id: int
    course_test_id: int
    points_to_pass: int = 0

    points: int = 0
    is_finished: bool = False
    is_passed: bool = False

@dataclass
class CourseTestLiteViewModel():
    id: int
    course_id: int
    name: Union[str, None] = None
    points_to_pass: int = 0
    courseTestUserLiteViewModel: Union[CourseTestUserLiteViewModel, None] = None

@dataclass
class CourseTestQiestionUserAnswer():
    """Возможный ответ на вопрос для пользователя"""
    id: int
    content: Union[str, None] = None
    number: int = 0
    is_checked: bool = False

@dataclass
class CourseTestQuestionUserLiteViewModel():
    """Вопрос для пользователя"""

    id: int
    content: Union[str, None] = None
    answers: Union[List[CourseTestQiestionUserAnswer], None] = None

@dataclass
class CourseTestUserStatusViewModel():
    """Объект, передающий информацию о текущем состоянии прохождения теста пользователем"""

    course_test_id: int
    course_test_question_numbers: int
    course_test_question_current_number: int
    is_first: bool = False
    is_last: bool = False
    question: Union[CourseTestQuestionUserLiteViewModel, None] = None
    courseTestUserLiteViewModel: Union[CourseTestUserLiteViewModel, None] = None