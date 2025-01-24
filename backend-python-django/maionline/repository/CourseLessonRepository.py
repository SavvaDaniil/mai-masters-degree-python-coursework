
from typing import List, Union
from maionline.models import CourseLesson, Course


class CourseLessonRepository():

    def find_by_id(self, course_lesson_id: int) -> Union[CourseLesson, None]:
        try:
            return CourseLesson.objects.get(id=course_lesson_id)
        except CourseLesson.DoesNotExist:
            return None

    def list_active_by_course(self, course: Course) -> List[CourseLesson]:
        return CourseLesson.objects.filter(is_active=True, course=course).order_by("order_in_list").all()