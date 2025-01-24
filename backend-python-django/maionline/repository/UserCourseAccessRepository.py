
from django.contrib.auth.models import User
from typing import Union, List

from maionline.models import UserCourseAccess, Course
from maionline.customException.UserCourseAccessCustomException import UserCourseAccessNotFoundException

class UserCourseAccessRepository:

    def find_by_user_with_course(self, user: User, course: Course) -> Union[UserCourseAccess, None]:
        try:
            return UserCourseAccess.objects.get(user = user, course = course)
        except UserCourseAccess.DoesNotExist:
            return None
        
    def list_by_user(self, user: User) -> List[UserCourseAccess]:
        """Список всех доступов пользователя"""
        return UserCourseAccess.objects.filter(user=user)