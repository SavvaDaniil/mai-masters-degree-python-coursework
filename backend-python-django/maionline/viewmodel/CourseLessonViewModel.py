
from typing import Union, List
from dataclasses import dataclass
from maionline.viewmodel.CourseLessonSlideViewModel import CourseLessonSlideLiteViewModel

@dataclass
class CourseLessonPreviewViewModel():
    id: int
    name: Union[str, None] = None
    order_in_list: int = 0


@dataclass
class CourseLessonInfoViewModel(CourseLessonPreviewViewModel):
    course_id: int = 0
    course_name: Union[str, None] = None
    content: Union[str, None] = None
    courseLessonPreviewViewModels: Union[List[CourseLessonPreviewViewModel], None] = None
    #courseLessonSlideLiteViewModels: Union[List[CourseLessonSlideLiteViewModel], None] = None
    slides: Union[List[str], None] = None