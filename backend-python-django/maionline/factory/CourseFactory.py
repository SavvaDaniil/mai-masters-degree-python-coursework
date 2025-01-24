
from typing import List
from maionline.models import Course
from maionline.viewmodel.CourseViewModel import CoursePreviewViewModel, CourseInfoViewModel
from maionline.viewmodel.CourseLessonViewModel import CourseLessonPreviewViewModel

class CourseFactory:

    def create_info_model(self, course: Course, user_status: str, courseLessonPreviewViewModels: List[CourseLessonPreviewViewModel]) -> CourseInfoViewModel:
        return CourseInfoViewModel(
            id=course.id,
            name=course.name,
            user_status=user_status,
            description=course.description,
            courseLessonPreviewViewModels=courseLessonPreviewViewModels,
            is_need_test=course.is_need_test,
            course_test_id=course.courseTest.id if course.courseTest is not None else 0
        )

    def create_preview_model(self, course: Course, user_status: str) -> CoursePreviewViewModel:
        return CoursePreviewViewModel(
            id=course.id,
            name=course.name,
            user_status=user_status
        )