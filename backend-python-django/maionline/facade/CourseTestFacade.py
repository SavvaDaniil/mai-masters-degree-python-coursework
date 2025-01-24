from typing import Union, List
from django.contrib.auth.models import User
from datetime import datetime, timezone

from maionline.models import CourseTest, Course, UserCourseAccess, CourseTestQuestion, CourseTestQuestionAnswer, CourseTestUser, CourseTestUserAction
from maionline.dto.CourseTestDTO import CourseTestUserCommandDTO
from maionline.repository.UserRepository import UserRepository
from maionline.repository.CourseRepository import CourseRepository
from maionline.repository.UserCourseAccessRepository import UserCourseAccessRepository
from maionline.repository.CoureTestRepository import CoureTestRepository
from maionline.repository.CourseTestQuestionRepository import CourseTestQuestionRepository
from maionline.repository.CourseTestQuestionAnswerRepository import CourseTestQuestionAnswerRepository
from maionline.repository.CourseTestUserRepository import CourseTestUserRepository
from maionline.repository.CourseTestUserActionRepository import CourseTestUserActionRepository
from maionline.util.CourseUtil import CourseUtil
from maionline.factory.CourseTestFactory import CourseTestFactory
from maionline.viewmodel.CourseTestViewModel import CourseTestLiteViewModel, CourseTestUserStatusViewModel, CourseTestQuestionUserLiteViewModel, CourseTestQiestionUserAnswer, CourseTestUserLiteViewModel
from maionline.customException.UserCustomException import UserNotFoundException
from maionline.customException.CourseCustomException import CourseNotFoundException, CourseAccessDeniedForUserException
from maionline.customException.CourseTestCustomException import CourseTestNotSetForCourseException, CourseTestNotFoundException, CourseTestQuestionNotFoundException

class CourseTestFacade():

    def __init__(self):
        self.courseRepository: CourseRepository = CourseRepository()
        self.userRepository: UserRepository = UserRepository()
        self.userCourseAccessRepository: UserCourseAccessRepository = UserCourseAccessRepository()
        self.coureTestRepository: CoureTestRepository = CoureTestRepository()
        self.courseTestQuestionRepository: CourseTestQuestionRepository = CourseTestQuestionRepository()
        self.courseTestQuestionAnswerRepository: CourseTestQuestionAnswerRepository = CourseTestQuestionAnswerRepository()
        self.courseTestUserRepository: CourseTestUserRepository = CourseTestUserRepository()
        self.courseTestUserActionRepository: CourseTestUserActionRepository = CourseTestUserActionRepository()
        self.courseTestFactory: CourseTestFactory = CourseTestFactory()
        self.courseUtil: CourseUtil = CourseUtil()

    def command_course_test_by_user(self, user_id: int, courseTestUserCommandDTO: CourseTestUserCommandDTO) -> CourseTestUserStatusViewModel:
        """Команды от пользователя во время выполнения теста курса"""

        user: User = self.userRepository.find_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()
        
        courseTest: Union[CourseTest, None] = self.coureTestRepository.find_by_id(id=courseTestUserCommandDTO.cleaned_data.get("course_test_id"))
        if courseTest is None:
            raise CourseTestNotFoundException()
        
        #получаем или создаем новый статус прохождения теста пользователем
        #ToDo: может проставить статус 0 не начинали, 1 начал, 2 закончил??? Зачем?
        courseTestUser: Union[CourseTestUser, None] = self.courseTestUserRepository.find_by_user_with_course_test(user=user, courseTest=courseTest)
        if courseTestUser is None:
            courseTestUser = CourseTestUser()
            courseTestUser.user = user
            courseTestUser.courseTest = courseTest
            courseTestUser.points = 0
            courseTestUser.save()

        #получаем список вопросов тест
        courseTestQuestions: List[CourseTestQuestion] = self.courseTestQuestionRepository.list_by_course_test(courseTest=courseTest)

        if courseTestQuestions is None or len(courseTestQuestions) == 0:
            pass

        #получаем список ответов на вопросы
        courseTestQuestionAnswers: List[CourseTestQuestionAnswer] = self.courseTestQuestionAnswerRepository.list_by_course_test(courseTest=courseTest)
        #получаем все ответы пользователя, если они были
        courseTestUserActions: List[CourseTestUserAction] = self.courseTestUserActionRepository.list_by_user_with_course_test(user=user, courseTest=courseTest)

        
        course_test_question_number: int = courseTestUserCommandDTO.cleaned_data.get("course_test_question_number")
        if course_test_question_number is None:
            course_test_question_number = 1
        course_test_question_id: int = courseTestUserCommandDTO.cleaned_data.get("course_test_question_id")

        if courseTestUserCommandDTO.cleaned_data.get("command") == "prev":
            if course_test_question_number <= 1:
                return None
            else:
                course_test_question_number -= 1

        if courseTestUserCommandDTO.cleaned_data.get("command") == "question":

            answers_ids_str: Union[str, None] = None
            if courseTestUserCommandDTO.cleaned_data.get("answer_ids_list") is not None and courseTestUserCommandDTO.cleaned_data.get("answer_ids_list") != "":
                answer_id_strs: List[str] = str(courseTestUserCommandDTO.cleaned_data.get("answer_ids_list")).split(",")
                answers_ids: List[int] = list(map(int, answer_id_strs))
                answers_ids_str: str = ",".join(str(x) for x in answers_ids)

            courseTestQuestion: CourseTestQuestion = self.courseTestQuestionRepository.find_by_id(id=course_test_question_id)
            if courseTestQuestion is None:
                raise CourseTestQuestionNotFoundException()
            
            courseTestUserAction: Union[CourseTestUserAction, None] = self.courseTestUserActionRepository.find_by_user_with_course_test_with_course_test_question(
                user=user,
                courseTest=courseTest,
                courseTestQuestion=courseTestQuestion
            )
            if courseTestUserAction is None:
                courseTestUserAction = CourseTestUserAction()
                courseTestUserAction.user = user
                courseTestUserAction.courseTest = courseTest
                courseTestUserAction.courseTestUser = courseTestUser
                courseTestUserAction.courseTestQuestion = courseTestQuestion
                courseTestUserAction.save()

            if courseTestUserAction.answer_id_list != answers_ids_str:
                courseTestUserAction.answer_id_list = answers_ids_str
                courseTestUserAction.save()

            if course_test_question_number >= len(courseTestQuestions):
                #окончание тестирование и выдача результата

                result_points: int = 0
                points_for_answer: int = 0
                is_wrong_answer: bool = False
                answer_ids_list: List[str] = []
                #прогружаем снова все ответы пользователя
                courseTestUserActions: List[CourseTestUserAction] = self.courseTestUserActionRepository.list_by_user_with_course_test(user=user, courseTest=courseTest)

                for courseTestQuestion in courseTestQuestions:
                    for courseTestUserAction in courseTestUserActions:
                        if courseTestUserAction.courseTestQuestion is None or courseTestUserAction.courseTestQuestion.id != courseTestQuestion.id:
                            continue
                        if courseTestUserAction.answer_id_list is None or courseTestUserAction.answer_id_list == "":
                            continue
                        
                        is_wrong_answer = False
                        points_for_answer = 0
                        answer_ids_list = str(courseTestUserAction.answer_id_list).split(",")
                        for answer_id in answer_ids_list:
                            for courseTestQuestionAnswer in courseTestQuestionAnswers:
                                if str(courseTestQuestionAnswer.id) != answer_id or is_wrong_answer or courseTestQuestionAnswer.courseTestQuestion is None or courseTestQuestionAnswer.courseTestQuestion.id != courseTestQuestion.id:
                                    continue
                                
                                if courseTestQuestionAnswer.is_correct:
                                    points_for_answer += courseTestQuestionAnswer.points
                                else:
                                    is_wrong_answer = True
                                    continue
                        
                        if not is_wrong_answer:
                            result_points += points_for_answer
                

                courseTestUser.points = result_points
                courseTestUser.is_finished = True
                if courseTest.points_to_pass <= result_points:
                    courseTestUser.is_passed = True
                    courseTestUser.date_of_passed = datetime.now(tz=timezone.utc)
                courseTestUser.save()
                        
                courseTestUserLiteViewModel: CourseTestUserLiteViewModel = CourseTestUserLiteViewModel(
                    id=courseTestUser.id,
                    user_id=courseTestUser.user.id,
                    course_test_id=courseTest.id,
                    points_to_pass=courseTest.points_to_pass,
                    points=courseTestUser.points,
                    is_finished=courseTestUser.is_finished,
                    is_passed=courseTestUser.is_passed
                )

                return CourseTestUserStatusViewModel(
                    course_test_id=courseTest.id,
                    course_test_question_numbers=len(courseTestQuestions),
                    course_test_question_current_number=course_test_question_number,
                    courseTestUserLiteViewModel=courseTestUserLiteViewModel
                )
            else:
                course_test_question_number += 1




        if courseTestUserCommandDTO.cleaned_data.get("command") == "start":
            #Удаляем все прошлые ответы
            for courseTestUserAction in courseTestUserActions:
                courseTestUserAction.delete()
            courseTestUserActions = []

            #очищаем статус прохождения
            courseTestUser.points = 0
            courseTestUser.is_passed = False
            courseTestUser.date_of_passed = None
            courseTestUser.save()
        

        #Выдача следующего вопроса
        courseTestQiestionUserAnswersForQuestion: List[CourseTestQiestionUserAnswer] = []
        is_checked: bool = False
        #course_test_question_answer_number: int = 0
        answer_ids: List[int] = []
        for courseTestQuestionAnswer in courseTestQuestionAnswers:
            if courseTestQuestionAnswer.courseTestQuestion is None or courseTestQuestionAnswer.courseTestQuestion.id != courseTestQuestions[course_test_question_number-1].id:
                continue

            #проверяем ответ на вопрос
            answer_ids = []
            is_checked = False
            for courseTestUserAction in courseTestUserActions:
                if courseTestUserAction.courseTestQuestion is None \
                    or courseTestUserAction.courseTestQuestion.id != courseTestQuestions[course_test_question_number-1].id:
                    continue

                is_checked = False
                if courseTestUserAction.answer_id_list is not None and courseTestUserAction.answer_id_list != "":
                    answer_ids = str(courseTestUserAction.answer_id_list).split(",")
                    is_checked = (str(courseTestQuestionAnswer.id) in answer_ids)

            courseTestQiestionUserAnswersForQuestion.append(
                CourseTestQiestionUserAnswer(
                    id=courseTestQuestionAnswer.id,
                    content=courseTestQuestionAnswer.content,
                    number=course_test_question_number,
                    is_checked=is_checked
                )
            )

        courseTestQuestionUserLiteViewModel: CourseTestQuestionUserLiteViewModel = CourseTestQuestionUserLiteViewModel(
            id=courseTestQuestions[course_test_question_number-1].id,
            content=courseTestQuestions[course_test_question_number-1].content,
            answers=courseTestQiestionUserAnswersForQuestion
        )

        return CourseTestUserStatusViewModel(
            course_test_id=courseTest.id,
            course_test_question_numbers=len(courseTestQuestions),
            course_test_question_current_number=course_test_question_number,
            is_first=True,
            is_last=(len(courseTestQuestions) >= course_test_question_number),
            question=courseTestQuestionUserLiteViewModel
        )


    def get_lite_by_course_id(self, user_id: int, course_id: int) -> CourseTestLiteViewModel:

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
            raise CourseAccessDeniedForUserException()

        if course.courseTest is None:
            raise CourseTestNotSetForCourseException()
        
        courseTestUserLiteViewModel: Union[CourseTestUserLiteViewModel, None] = None
        courseTestUser: Union[CourseTestUser, None] = self.courseTestUserRepository.find_by_user_with_course_test(user=user, courseTest=course.courseTest)
        if courseTestUser is not None:
            if courseTestUser.is_finished:
                courseTestUserLiteViewModel = CourseTestUserLiteViewModel(
                    id=courseTestUser.id,
                    user_id=courseTestUser.user.id,
                    course_test_id=course.courseTest.id,
                    points_to_pass=course.courseTest.points_to_pass,
                    points=courseTestUser.points,
                    is_finished=courseTestUser.is_finished,
                    is_passed=courseTestUser.is_passed
                )

        return self.courseTestFactory.create_lite(courseTest=course.courseTest, course=course, courseTestUserLiteViewModel=courseTestUserLiteViewModel)