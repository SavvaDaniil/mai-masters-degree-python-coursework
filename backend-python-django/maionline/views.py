from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from maionline.dto.UserDTO import UserLoginForm, UserProfileForm
from maionline.dto.CourseTestDTO import CourseTestUserCommandDTO
from typing import Union, List
from maionline.facade.UserFacade import UserFacade
from maionline.facade.CourseFacade import CourseFacade
from maionline.facade.CourseLessonFacade import CourseLessonFacade
from maionline.facade.CourseTestFacade import CourseTestFacade
from maionline.abstracts.NotCriticalAbstractException import NotCriticalAbstractException
from maionline.viewmodel.UserViewModel import UserProfileViewModel
from maionline.viewmodel.CourseViewModel import CoursePreviewViewModel, CourseInfoViewModel
from maionline.viewmodel.CourseLessonViewModel import CourseLessonInfoViewModel
from maionline.viewmodel.CourseTestViewModel import CourseTestLiteViewModel, CourseTestUserStatusViewModel
from maionline.viewmodel.BaseResponse import BaseResponse
import logging
from logging import Logger
log: Logger = logging.getLogger(__name__)

userFacade: UserFacade = UserFacade()
courseFacade: CourseFacade = CourseFacade()
courseLessonFacade: CourseLessonFacade = CourseLessonFacade()
courseTestFacade: CourseTestFacade = CourseTestFacade()

@csrf_exempt
def api_course_test_user_command(request: HttpRequest) -> JsonResponse:
    """Инициализация старта теста, либо продолжение"""

    #ToDo: может все-таки командой? start, next, prev

    if not request.user.is_authenticated:
        return JsonResponse(status=401)
    
    error: Union[str, None] = None
    courseTestUserCommandDTO: CourseTestUserCommandDTO = CourseTestUserCommandDTO(request.POST)
    if courseTestUserCommandDTO.is_valid():
        try:
            courseTestUserStatusViewModel: CourseTestUserStatusViewModel = courseTestFacade.command_course_test_by_user(user_id=request.user.id, courseTestUserCommandDTO=courseTestUserCommandDTO)
            baseResponse: BaseResponse = BaseResponse(courseTestUserStatusViewModel=courseTestUserStatusViewModel)
            return JsonResponse(
                data=baseResponse.__dict__,
                status=200
            )
        except NotCriticalAbstractException as e:
            error = str(e)
        except Exception as e:
            log.error(e)
            error = "Неизвестная ошибка на сервере"
    else:
        error = "Не все обязательные поля заполнены"

    baseResponse: BaseResponse = BaseResponse(error=error)
    return JsonResponse(
        data=baseResponse.__dict__,
        status=400
    )


def course_test(request: HttpRequest, course_id: int = 0) -> HttpResponse:
    """Страница теста курса"""

    if not request.user.is_authenticated:
        return redirect("/login")

    if course_id <= 0:
        return redirect("/courses")
    link_back: str = f"/course/{course_id}"
    
    courseTestLiteViewModel: CourseTestLiteViewModel = courseTestFacade.get_lite_by_course_id(user_id=request.user.id, course_id=course_id)
    return render(
        request, 
        "course_test.html", 
        context={
            "title": courseTestLiteViewModel.name,
            "courseTestLiteViewModel" : courseTestLiteViewModel,
            "link_back": link_back
        }
    )



def course_lesson(request: HttpRequest, course_id: int = 0, course_lesson_id: int = 0) -> HttpResponse:
    """Страница занятия курса"""

    if not request.user.is_authenticated:
        return redirect("/login")
    
    if course_id <= 0:
        return redirect("/courses")
    
    link_back: str = f"/course/{course_id}"
    if course_lesson_id <= 0:
        return redirect(link_back)

    
    courseLessonInfoViewModel: CourseLessonInfoViewModel = courseLessonFacade.get_info_for_user(
        user_id=request.user.id,
        course_id=course_id,
        course_lesson_id=course_lesson_id
    )
    return render(
        request, 
        "course_lesson.html", 
        context={
            "title": courseLessonInfoViewModel.name,
            "courseLessonInfoViewModel" : courseLessonInfoViewModel,
            "link_back": link_back
        }
    )


def course(request: HttpRequest, course_id: int = 0) -> HttpResponse:
    """Страница курса"""

    if not request.user.is_authenticated:
        return redirect("/login")
    
    if course_id <= 0:
        return redirect("/courses")
    
    #Todo: try

    courseInfoViewModel: CourseInfoViewModel = courseFacade.get_info_for_user(user_id=request.user.id, course_id=course_id)

    return render(
        request, 
        "course.html", 
        context={
            "title": courseInfoViewModel.name,
            "courseInfoViewModel" : courseInfoViewModel,
            "link_back": "/courses"
        }
    )


def courses(request: HttpRequest) -> HttpResponse:
    """Главная, курсы"""
    if not request.user.is_authenticated:
        return redirect("/login")
    
    coursePreviewViewModels: List[CoursePreviewViewModel] = courseFacade.list_preview_for_user(user_id=request.user.id)

    return render(
        request, 
        "courses.html", 
        context={
            "title": "Курсы",
            "coursePreviewViewModels" : coursePreviewViewModels
        }
    )


def index(request: HttpRequest) -> HttpResponse:
    """Главная, профиль"""
    if not request.user.is_authenticated:
        return redirect("/login")

    warning: Union[str, None] = None
    userProfileViewModel: Union[UserProfileViewModel, None] = None
    try:
        if request.method == "POST":
            userProfileForm: UserProfileForm = UserProfileForm(request.POST)
            if userProfileForm.is_valid():
                try:
                    userFacade.update_by_user(request=request, user_id=request.user.id, userProfileForm=userProfileForm)
                except NotCriticalAbstractException as e:
                    warning = str(e)
                except Exception as e:
                    log.error(e)
                    warning = "Неизвестная ошибка на сервере"
            else:
                warning = "не все обязательные поля заполнены"

        userProfileViewModel = userFacade.get_profile_view_model(user_id=request.user.id)

    except NotCriticalAbstractException as e:
        warning = str(e)
    except Exception as e:
        log.error(e)
        
    return render(
        request, 
        "index.html", 
        context={
            "title": "Профиль",
            "userProfileViewModel" : userProfileViewModel,
            "warning" : warning
        }
    )

def api_user_profile_update(request: HttpRequest) -> JsonResponse:
    """Обновление профиля пользователем"""

    if request.method != "POST":
        return JsonResponse(status=500)
    
    error: Union[str, None] = None
    userProfileForm: UserProfileForm = UserProfileForm(request.POST)
    if userProfileForm.is_valid():
        try:
            userFacade.update_by_user(request=request, user_id=request.user.id, userProfileForm=userProfileForm)
        except NotCriticalAbstractException as e:
            error = str(e)
        except Exception as e:
            log.error(e)
            error = "Неизвестная ошибка на сервере"
    else:
        error = "Не все обязательные поля заполнены"

    baseResponse: BaseResponse = BaseResponse(error=error)
    return JsonResponse(
        data=baseResponse.__dict__,
        status=200
    )

def login(request: HttpRequest) -> HttpResponse:
    """Страница аутентификации"""

    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        userLoginForm: UserLoginForm = UserLoginForm(request.POST)
        if userLoginForm.is_valid():
            try:
                userFacade.login(request=request, userLoginForm=userLoginForm)
                return redirect("/")
            except NotCriticalAbstractException as e:
                return render(request=request, template_name="login.html", context= {
                    "title" : "Аутентификация",
                    "warning" : "Неправильно введены логин или пароль"
                })
            except Exception as e:
                log.error(e)
                return render(request=request, template_name="login.html", context= {
                    "title" : "Аутентификация",
                    "warning" : "Неизвестная ошибка на сервере"
                })
        else:
            return render(request=request, template_name="login.html", context= {
                "title" : "Аутентификация",
                "warning" : "Не все поля заполнены"
            })


    return render(request=request, template_name="login.html", context= {
        "title" : "Аутентификация"
    })

def logout_view(request: HttpRequest) -> None:
    if request.user.is_authenticated:
        logout(request=request)
    return redirect("/login")


@csrf_exempt
def api_user_admin_default_check(request: HttpRequest) -> JsonResponse:
    """Проверка существования пользователя с username 'admin' по умолчанию"""

    try:
        userFacade.check_default_admin_exists()
    except Exception as e:
        baseResponse: BaseResponse = BaseResponse(error=str(e))
        return JsonResponse(
            data=baseResponse.__dict__,
            status=400
        )
        
    baseResponse: BaseResponse = BaseResponse()
    return JsonResponse(
        data=baseResponse.__dict__,
        status=200
    )
