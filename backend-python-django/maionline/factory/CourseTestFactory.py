from typing import Union
from maionline.models import CourseTest, Course
from maionline.viewmodel.CourseTestViewModel import CourseTestLiteViewModel, CourseTestUserLiteViewModel

class CourseTestFactory():

    def create_lite(self, courseTest: CourseTest, course: Course, courseTestUserLiteViewModel: Union[CourseTestUserLiteViewModel, None]) -> CourseTestLiteViewModel:
        return CourseTestLiteViewModel(
            id=courseTest.id,
            course_id=course.id,
            name=courseTest.name,
            points_to_pass=courseTest.points_to_pass,

            courseTestUserLiteViewModel=courseTestUserLiteViewModel
        )