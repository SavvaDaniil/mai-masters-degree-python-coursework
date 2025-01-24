from typing import List, Union
from django.contrib.auth.models import User

from maionline.models import CourseTest, CourseTestUserAction, CourseTestQuestion


class CourseTestUserActionRepository():

    def find_by_user_with_course_test_with_course_test_question(self, user: User, courseTest: CourseTest, courseTestQuestion: CourseTestQuestion) -> Union[CourseTestUserAction, None]:
        try:
            return CourseTestUserAction.objects.get(user=user, courseTest=courseTest, courseTestQuestion=courseTestQuestion)
        except CourseTestUserAction.DoesNotExist:
            return None
    
    def list_by_user_with_course_test(self, user: User, courseTest: CourseTest) -> List[CourseTestUserAction]:
        return CourseTestUserAction.objects.filter(user=user, courseTest=courseTest).all()