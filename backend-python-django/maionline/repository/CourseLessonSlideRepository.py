from typing import List
from maionline.models import CourseLessonSlide, CourseLesson

class CourseLessonSlideRepository():

    def list_by_course_lesson(self, courseLesson: CourseLesson) -> List[CourseLessonSlide]:
        return CourseLessonSlide.objects.filter(courseLesson=courseLesson).all()