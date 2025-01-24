from typing import List
from maionline.models import CourseLesson
from maionline.viewmodel.CourseLessonViewModel import CourseLessonPreviewViewModel, CourseLessonInfoViewModel
from maionline.viewmodel.CourseLessonSlideViewModel import CourseLessonSlideLiteViewModel


class CourseLessonFactory():

    def create_info(
            self, 
            courseLesson: CourseLesson, 
            courseLessonPreviewViewModels: List[CourseLessonPreviewViewModel],
            #courseLessonSlideLiteViewModels: List[CourseLessonSlideLiteViewModel]
            slides: List[str]
        ) -> CourseLessonInfoViewModel:
        return CourseLessonInfoViewModel(
            id=courseLesson.id,
            name=courseLesson.name,
            order_in_list=courseLesson.order_in_list,
            course_id=courseLesson.course.id if courseLesson.course is not None else 0,
            course_name=courseLesson.course.name if courseLesson.course is not None else None,
            content=courseLesson.content,
            courseLessonPreviewViewModels=courseLessonPreviewViewModels,
            slides=slides,
        )

    def create_preview(self, courseLesson: CourseLesson) -> CourseLessonPreviewViewModel:
        return CourseLessonPreviewViewModel(
            id=courseLesson.id,
            name=courseLesson.name,
            order_in_list=courseLesson.order_in_list
        )