from typing import List, Union
from maionline.models import CourseTest, CourseTestQuestion


class CourseTestQuestionRepository():

    def find_by_id(self, id: int) -> Union[CourseTestQuestion, None]:
        try:
            return CourseTestQuestion.objects.get(id=id)
        except CourseTestQuestion.DoesNotExist:
            return None
        
    def list_by_course_test(self, courseTest: CourseTest) -> List[CourseTestQuestion]:
        return CourseTestQuestion.objects.filter(courseTest=courseTest).order_by("order_in_list").all()