from typing import List, Union
from maionline.models import CourseTest, CourseTestQuestionAnswer


class CourseTestQuestionAnswerRepository:

    def list_by_course_test(self, courseTest: CourseTest) -> List[CourseTestQuestionAnswer]:
        return CourseTestQuestionAnswer.objects.filter(courseTest=courseTest).order_by("order_in_list").all()