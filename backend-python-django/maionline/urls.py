from django.urls import path
from sympy import im
from maionline import views
from django.conf.urls.static import static
from django.conf import settings

from django.views.static import serve 
from django.urls import re_path as url


urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("logout", views.logout_view),
    path("courses", views.courses),
    path("course/<int:course_id>", views.course),
    path("course/<int:course_id>/lesson/<int:course_lesson_id>", views.course_lesson),
    path("course/<int:course_id>/test", views.course_test),

    path("api/user/profile", views.api_user_profile_update),
    path("api/course/test/user/command", views.api_course_test_user_command),
    path("api/user/admin/default/check", views.api_user_admin_default_check),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)