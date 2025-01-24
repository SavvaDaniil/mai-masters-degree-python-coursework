

from dataclasses import dataclass
from typing import Union, List

from maionline.viewmodel.CourseLessonViewModel import CourseLessonPreviewViewModel

@dataclass
class CoursePreviewViewModel():
    id: int
    name: Union[str, None] = None

    user_status: Union[str, None] = None
    """Статус доступа курса для пользователя"""


@dataclass
class CourseInfoViewModel(CoursePreviewViewModel):
    description: Union[str, None] = None
    courseLessonPreviewViewModels: Union[List[CourseLessonPreviewViewModel], None] = None
    is_need_test: bool = False
    course_test_id: int = 0
