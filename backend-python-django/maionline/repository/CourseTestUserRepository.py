from typing import List, Union
from django.contrib.auth.models import User

from maionline.models import CourseTest, CourseTestUser


class CourseTestUserRepository():

    def find_by_user_with_course_test(self, user: User, courseTest: CourseTest) -> Union[CourseTestUser, None]:
        try:
            return CourseTestUser.objects.get(user=user, courseTest=courseTest)
        except CourseTestUser.DoesNotExist:
            return None