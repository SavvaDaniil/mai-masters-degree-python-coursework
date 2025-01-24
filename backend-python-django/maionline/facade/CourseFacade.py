
from typing import List, Union
from django.contrib.auth.models import User
from datetime import datetime, timezone

from maionline.models import Course, UserCourseAccess, CourseLesson
from maionline.repository.UserRepository import UserRepository
from maionline.repository.CourseRepository import CourseRepository
from maionline.repository.UserCourseAccessRepository import UserCourseAccessRepository
from maionline.repository.CourseLessonRepository import CourseLessonRepository
from maionline.factory.CourseFactory import CourseFactory
from maionline.factory.CourseLessonFactory import CourseLessonFactory
from maionline.util.CourseUtil import CourseUtil
from maionline.viewmodel.CourseViewModel import CoursePreviewViewModel, CourseInfoViewModel
from maionline.customException.UserCustomException import UserNotFoundException
from maionline.customException.CourseCustomException import CourseNotFoundException
from maionline.viewmodel.CourseLessonViewModel import CourseLessonPreviewViewModel

class CourseFacade():

    def __init__(self):
        self.courseRepository: CourseRepository = CourseRepository()
        self.userRepository: UserRepository = UserRepository()
        self.courseFactory: CourseFactory = CourseFactory()
        self.userCourseAccessRepository: UserCourseAccessRepository = UserCourseAccessRepository()
        self.courseLessonRepository: CourseLessonRepository = CourseLessonRepository()
        self.courseLessonFactory: CourseLessonFactory = CourseLessonFactory()
        self.courseUtil: CourseUtil = CourseUtil()

    def get_info_for_user(self, user_id: int, course_id: int) -> CourseInfoViewModel:

        user: User = self.userRepository.find_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        course: Course = self.courseRepository.find_by_id(course_id=course_id)
        if course is None:
            raise CourseNotFoundException()
        
        course_user_status: str = "closed"
        userCourseAccess: Union[UserCourseAccess, None] = self.userCourseAccessRepository.find_by_user_with_course(user=user, course=course)
        if userCourseAccess is not None:
            course_user_status = self.courseUtil.get_user_status_for_course(
                course=course,
                userCourseAccess=userCourseAccess,
                for_date=datetime.now(tz=timezone.utc).date()
            )

        if course_user_status == "closed":
            #ToDo: Выдать ошибку
            pass

        courseLessonPreviewViewModels: List[CourseLessonPreviewViewModel] = []
        courseLessons: List[CourseLesson] = self.courseLessonRepository.list_active_by_course(course=course)
        for courseLesson in courseLessons:
            courseLessonPreviewViewModels.append(
                self.courseLessonFactory.create_preview(courseLesson=courseLesson)
            )
        
        
        return self.courseFactory.create_info_model(
            course=course,
            user_status=course_user_status,
            courseLessonPreviewViewModels=courseLessonPreviewViewModels
        )


    def list_preview_for_user(self, user_id: int) -> List[CoursePreviewViewModel]:
        """Список доступных пользователю курсов в виде наименования со статусами доступов"""

        user: User = self.userRepository.find_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()

        coursePreviewViewModels: List[CoursePreviewViewModel] = []
        course_list_active: List[Course] = self.courseRepository.list_active()

        userCourseAccesses: List[UserCourseAccess] = self.userCourseAccessRepository.list_by_user(user=user)

        user_status: Union[str, None] = None
        for course_active in course_list_active:

            if not course_active.is_active:
                continue

            if not course_active.is_visible:
                continue

            dateNow: datetime = datetime.now(tz=timezone.utc).date()
            user_status = "closed"

            for userCourseAccess in userCourseAccesses:
                user_status = self.courseUtil.get_user_status_for_course(
                    course=course_active, 
                    userCourseAccess=userCourseAccess,
                    for_date=dateNow
                )

            coursePreviewViewModels.append(
                self.courseFactory.create_preview_model(
                    course=course_active, 
                    user_status=user_status
                )
            )

        return coursePreviewViewModels
        
                