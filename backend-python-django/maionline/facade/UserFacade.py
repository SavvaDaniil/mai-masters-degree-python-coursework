
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from typing import Union

from maionline.dto.UserDTO import UserLoginForm, UserProfileForm
from maionline.models import UserData
from maionline.repository.UserRepository import UserRepository
from maionline.repository.UserDataRepository import UserDataRepository
from maionline.customException.UserCustomException import UserLoginWrongException, UserNotFoundException, UsernameIsAlreadyExistsException, PasswordCurrentWrongExists
from maionline.viewmodel.UserViewModel import UserProfileViewModel

class UserFacade:

    def __init__(self):
        self.userRepository: UserRepository = UserRepository()
        self.userDataRepository: UserDataRepository = UserDataRepository()

    def update_by_user(self, request: HttpRequest, user_id: int, userProfileForm: UserProfileForm) -> None:
        """Редактирование профиля пользователем"""
        user: User = self.userRepository.find_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException
        
        if userProfileForm.cleaned_data.get("username") is not None and userProfileForm.cleaned_data.get("username") != "" and user.username != userProfileForm.cleaned_data.get("username"):
            if self.userRepository.is_exists_by_username_except_id(user_id=user.id, username=userProfileForm.cleaned_data.get("username")):
                raise UsernameIsAlreadyExistsException()
            user.username = userProfileForm.cleaned_data.get("username")

        user.first_name = userProfileForm.cleaned_data.get("firstname")
        user.last_name = userProfileForm.cleaned_data.get("lastname")
        is_need_relogin: bool = False
        if userProfileForm.cleaned_data.get("password_new") is not None and userProfileForm.cleaned_data.get("password_new") != "":
            if not authenticate(username=user.username, password=userProfileForm.cleaned_data.get("password")):
                raise PasswordCurrentWrongExists()
            user.set_password(userProfileForm.cleaned_data.get("password_new"))
            is_need_relogin = True

        user.save()

        userData: UserData = self.userDataRepository.find_by_user(user=user)
        if userData is None:
            userData = UserData()
            userData.user = user
        
        userData.patronymic = userProfileForm.cleaned_data.get("patronymic")
        userData.save()

        if is_need_relogin:
            login(request=request, user=user, backend=None)



    def get_profile_view_model(self, user_id: int) -> UserProfileViewModel:
        user: User = self.userRepository.find_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException()
        userData: Union[UserData, None] = self.userDataRepository.find_by_user(user=user)

        return UserProfileViewModel(
            username=user.username,
            firstname=user.first_name,
            lastname=user.last_name,
            patronymic=userData.patronymic if userData is not None else None
        )


    def login(self, request: HttpRequest, userLoginForm: UserLoginForm) -> None:
        """Аутентификация пользователя"""
        user: Union[User, None] = None
        try:
            user = authenticate(
                username=userLoginForm.cleaned_data.get("username"), 
                password=userLoginForm.cleaned_data.get("password")
            )
        except User.DoesNotExist as e:
            raise UserLoginWrongException()
        
        if user is None:
            raise UserLoginWrongException()
        
        login(request=request, user=user, backend=None)

    def check_default_admin_exists(self) -> None:
        
        admin_default_username: str = "admin"
        userDefault: Union[User, None] = self.userRepository.find_by_username("admin")
        if userDefault is None:
            userDefault = User()
            userDefault.is_active = True
            userDefault.is_superuser = True
            userDefault.username = admin_default_username
            userDefault.set_password("master")
            userDefault.save()
        
        