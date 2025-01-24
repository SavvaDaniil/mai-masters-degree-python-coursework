from django.contrib import admin

# Register your models here.


from maionline.models import UserData, UserDataAdmin, Course, CourseAdmin, CourseLesson, CourseLessonAdmin, UserCourseAccess, UserCourseAccessAdmin, CourseLessonSlide, CourseLessonSlideAdmin, CourseTest, CourseTestAdmin, CourseTestQuestion, CourseTestQuestionAdmin, CourseTestQuestionAnswer, CourseTestQuestionAnswerAdmin, CourseTestUser, CourseTestUserAdmin, CourseTestUserAction, CourseTestUserActionAdmin


admin.site.register(UserData, UserDataAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseLesson, CourseLessonAdmin)
admin.site.register(UserCourseAccess, UserCourseAccessAdmin)
admin.site.register(CourseLessonSlide, CourseLessonSlideAdmin)
admin.site.register(CourseTest, CourseTestAdmin)
admin.site.register(CourseTestQuestion, CourseTestQuestionAdmin)
admin.site.register(CourseTestQuestionAnswer, CourseTestQuestionAnswerAdmin)
admin.site.register(CourseTestUser, CourseTestUserAdmin)
admin.site.register(CourseTestUserAction, CourseTestUserActionAdmin)