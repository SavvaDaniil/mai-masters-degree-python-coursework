from typing import List, Union
from datetime import datetime

from maionline.models import Course, UserCourseAccess


class CourseUtil():

    def get_user_status_for_course(self, course: Course, userCourseAccess: UserCourseAccess, for_date: Union[datetime, None]) -> str:
        """Получение статуса доступа пользователя к курсу, можно и на дату. Если даты не будет, а доступ по дате, проставится текущая"""
        
        user_status: str = "closed"

        if userCourseAccess.course is None or userCourseAccess.course.id != course.id:
            return user_status

        if userCourseAccess.is_active:
            if userCourseAccess.is_active_with_deadline and userCourseAccess.deadline_date_since is not None and userCourseAccess.deadline_date_until is not None:
                if for_date is None:
                    for_date = datetime.now().date()
                if userCourseAccess.deadline_date_since <= for_date and for_date < userCourseAccess.deadline_date_until:
                    user_status = "opened"
            else:
                user_status = "opened"
        
        elif userCourseAccess.is_passed:
            user_status = "done"

        return user_status