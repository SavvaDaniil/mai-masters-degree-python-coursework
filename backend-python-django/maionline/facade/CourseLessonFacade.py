
from typing import List, Union
from django.contrib.auth.models import User
from datetime import datetime

from maionline.models import CourseLesson, Course, UserCourseAccess
from maionline.repository.UserRepository import UserRepository
from maionline.repository.CourseRepository import CourseRepository
from maionline.repository.CourseLessonRepository import CourseLessonRepository
from maionline.repository.UserCourseAccessRepository import UserCourseAccessRepository
from maionline.util.CourseUtil import CourseUtil
from maionline.factory.CourseLessonFactory import CourseLessonFactory
from maionline.facade.CourseLessonSlideFacade import CourseLessonSlideFacade
from maionline.viewmodel.CourseLessonViewModel import CourseLessonInfoViewModel, CourseLessonPreviewViewModel
from maionline.viewmodel.CourseLessonSlideViewModel import CourseLessonSlideLiteViewModel
from maionline.customException.UserCustomException import UserNotFoundException
from maionline.customException.CourseCustomException import CourseNotFoundException, CourseAccessDeniedForUserException
from maionline.customException.CourseLessonCustomException import CourseLessonNotFoundException, CourseLessonNotConnectedToCourseException

class CourseLessonFacade():

    def __init__(self):
        self.userRepository: UserRepository = UserRepository()
        self.courseRepository: CourseRepository = CourseRepository()
        self.courseLessonRepository: CourseLessonRepository = CourseLessonRepository()
        self.userCourseAccessRepository: UserCourseAccessRepository = UserCourseAccessRepository()
        self.courseUtil: CourseUtil = CourseUtil()
        self.courseLessonFactory: CourseLessonFactory = CourseLessonFactory()
        self.courseLessonSlideFacade: CourseLessonSlideFacade = CourseLessonSlideFacade()

    def get_info_for_user(self, user_id: int, course_id: int, course_lesson_id: int) -> CourseLessonInfoViewModel:

        user: User = self.userRepository.find_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        course: Course = self.courseRepository.find_by_id(course_id=course_id)
        if course is None:
            raise CourseNotFoundException()
        
        courseLesson: CourseLesson = self.courseLessonRepository.find_by_id(course_lesson_id=course_lesson_id)
        if courseLesson is None:
            raise CourseLessonNotFoundException()
        
        if courseLesson.course is None or courseLesson.course.id != course.id:
            #Todo отдельная страница
            raise CourseLessonNotConnectedToCourseException()
        
        userCourseAccess: Union[UserCourseAccess, None] = self.userCourseAccessRepository.find_by_user_with_course(user=user, course=course)
        if userCourseAccess is None:
            #Todo отдельная страница
            raise CourseAccessDeniedForUserException()
        
        if self.courseUtil.get_user_status_for_course(course=course, userCourseAccess=userCourseAccess, for_date=datetime.now().date()) == "closed":
            #Todo отдельная страница
            raise CourseAccessDeniedForUserException()
        
        courseLessonPreviewViewModels: List[CourseLessonPreviewViewModel] = []
        courseLessonOthers: List[CourseLesson] = self.courseLessonRepository.list_active_by_course(course=course)
        for courseLessonOther in courseLessonOthers:
            courseLessonPreviewViewModels.append(
                self.courseLessonFactory.create_preview(courseLesson=courseLessonOther)
            )
        #courseLessonSlideLiteViewModels: List[CourseLessonSlideLiteViewModel] = self.courseLessonSlideFacade.list_info_by_course_lesson(courseLesson=courseLesson)
        slides: List[str] = self.courseLessonSlideFacade.list_slides_by_course_lesson(courseLesson=courseLesson)
        
        return self.courseLessonFactory.create_info(
            courseLesson=courseLesson, 
            courseLessonPreviewViewModels=courseLessonPreviewViewModels,
            slides=slides
        )



        

