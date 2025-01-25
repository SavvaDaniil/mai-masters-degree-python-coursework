from django.db.models import Model, AutoField, CharField, DateTimeField, ForeignKey, OneToOneField, CASCADE, TextField, BooleanField, IntegerField, DateField, ImageField
from django.contrib.admin import ModelAdmin
from datetime import datetime, timezone
from django.contrib.auth.models import User, AbstractUser




class CourseTestAdmin(ModelAdmin):
    list_display = ("id", "name", "points_to_pass", "is_active")
class CourseTest(Model):
    
    class Meta:
        verbose_name = "Тест курса"
        verbose_name_plural = "Тесты курсов"
    
    id: AutoField = AutoField(primary_key=True)
    name: CharField = CharField("Наименование", max_length=1024, blank=True, null=True)
    points_to_pass = IntegerField("Минимальное количество баллов для сдачи", blank=True, default=0)
    is_active = BooleanField("Доступен?", default=False)

    def __str__(self) -> str:
        return "{0}. {1}".format(self.id, self.name)
    


class CourseAdmin(ModelAdmin):
    list_display = ("id", "name", "is_active", "is_visible", "is_need_test")

class Course(Model):

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    id: AutoField = AutoField(primary_key=True)
    name: CharField = CharField("Наименование", max_length=516, blank=True, null=True)
    description: TextField = TextField("Описание", blank=True, null=True)
    is_active = BooleanField("Доступен пользователям?", default=False)
    is_visible = BooleanField("Отображается пользователям?", default=False)
    courseTest: ForeignKey = ForeignKey(to=CourseTest, blank=True, null=True, on_delete = CASCADE)
    is_need_test = BooleanField("Тест доступен?", default=False)

    date_of_add: DateTimeField = DateTimeField(null=True, blank=True, editable = False)
    date_of_update: DateTimeField = DateTimeField(null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if self.date_of_add is None:
            self.date_of_add = datetime.now(tz=timezone.utc)
        self.date_of_update = datetime.now(tz=timezone.utc)
        super(Course, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return "{0}. {1}".format(self.id, self.name)
    

class CourseLessonAdmin(ModelAdmin):
    list_display = ("id", "name", "is_active", "is_slider_active", "order_in_list")
class CourseLesson(Model):

    class Meta:
        verbose_name = "Занятие курса"
        verbose_name_plural = "Занятия курсов"
    
    id: AutoField = AutoField(primary_key=True)
    course = ForeignKey(to=Course, on_delete = CASCADE)
    name: CharField = CharField("Наименование", max_length=1024, blank=True, null=True)
    content: TextField = TextField("Содержение занятия", blank=True, null=True)
    order_in_list = IntegerField("Номер занятия", blank=True, default=0)
    is_active = BooleanField("Доступен пользователям?", default=False)
    is_slider_active = BooleanField("Доступен ли слайдер?", default=False)

    date_of_add: DateTimeField = DateTimeField(null=True, blank=True, editable = False)
    date_of_update: DateTimeField = DateTimeField(null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if self.date_of_add is None:
            self.date_of_add = datetime.now(tz=timezone.utc)
        self.date_of_update = datetime.now(tz=timezone.utc)
        super(CourseLesson, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return "{0}. {1}".format(self.id, self.name)





class CourseLessonSlideAdmin(ModelAdmin):
    list_display = ("id", "courseLesson", "order_in_list", "is_active")
class CourseLessonSlide(Model):

    class Meta:
        verbose_name = "Слайд урока курса"
        verbose_name_plural = "Слайд уроков"

    def getImagePath(instance, filename) -> str:
        return 'uploads/course_lesson_slide/{0}.jpg'.format(instance.id)
    

    id: AutoField = AutoField(primary_key=True)
    courseLesson: ForeignKey = ForeignKey(to=CourseLesson, on_delete = CASCADE)
    imageSrc = ImageField("Картинка формата .jpg", upload_to = getImagePath, null=True, blank=True)

    is_active = BooleanField("Доступен к просмотру?", default=True)
    order_in_list = IntegerField("Номер слайда", blank=True, default=0)

    date_of_add: DateTimeField = DateTimeField(null=True, blank=True, editable = False)
    date_of_update: DateTimeField = DateTimeField(null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if self.date_of_add is None:
            self.date_of_add = datetime.now(tz=timezone.utc)
        self.date_of_update = datetime.now(tz=timezone.utc)
        super(CourseLessonSlide, self).save(*args, **kwargs)

    def getImageSrc(self) -> str:
        if not self.imageSrc:
            return None
        return self.imageSrc.url





class CourseTestQuestionAdmin(ModelAdmin):
    list_display = ("id", "courseTest", "order_in_list", "is_active")
class CourseTestQuestion(Model):
    
    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы тестов"
    
    id: AutoField = AutoField(primary_key=True)
    courseTest: ForeignKey = ForeignKey(to=CourseTest, on_delete = CASCADE)
    content: TextField = TextField("Контент вопроса", blank=True, null=True)
    order_in_list = IntegerField("Номер вопроса", blank=True, default=0)
    is_active = BooleanField("Доступен?", default=False)

    def __str__(self) -> str:
        return "id{0} Вопрос №{1}".format(self.id, self.order_in_list)
    


class CourseTestQuestionAnswerAdmin(ModelAdmin):
    list_display = ("id", "courseTest", "courseTestQuestion", "order_in_list", "is_correct", "points", "is_active")
class CourseTestQuestionAnswer(Model):
    
    class Meta:
        verbose_name = "Ответ на вопрос теста"
        verbose_name_plural = "Ответы на вопросы тестов"
    
    id: AutoField = AutoField(primary_key=True)
    courseTest: ForeignKey = ForeignKey(to=CourseTest, on_delete = CASCADE)
    courseTestQuestion: ForeignKey = ForeignKey(to=CourseTestQuestion, on_delete = CASCADE)
    content: TextField = TextField("Контент ответа", blank=True, null=True)
    order_in_list = IntegerField("Номер ответа", blank=True, default=0)
    is_correct = BooleanField("Правильный?", default=False)
    points = IntegerField("Баллы за ответ", blank=True, default=0)
    is_active = BooleanField("Доступен?", default=False)


class CourseTestUserAdmin(ModelAdmin):
    list_display = ("id", "user", "courseTest", "points", "is_passed", "date_of_passed")
    readonly_fields = ("courseTest", "date_of_add", "date_of_update")
class CourseTestUser(Model):
    
    class Meta:
        verbose_name = "Прохождение теста пользователем"
        verbose_name_plural = "Прохождения тестов пользователями"

    id: AutoField = AutoField(primary_key=True)
    user: ForeignKey = ForeignKey(to=User, blank=False, null=False, on_delete=CASCADE)
    courseTest = ForeignKey(to=CourseTest, on_delete = CASCADE)
    points = IntegerField("Баллы", blank=True, default=0)
    is_finished = BooleanField("Закончен?", default=False)
    is_passed = BooleanField("Пройден?", default=False)
    date_of_passed: DateTimeField = DateTimeField(null=True, blank=True)

    date_of_add: DateTimeField = DateTimeField(null=True, blank=True, editable = False)
    date_of_update: DateTimeField = DateTimeField(null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if self.date_of_add is None:
            self.date_of_add = datetime.now(tz=timezone.utc)
        self.date_of_update = datetime.now(tz=timezone.utc)
        super(CourseTestUser, self).save(*args, **kwargs)




class CourseTestUserActionAdmin(ModelAdmin):
    list_display = ("id", "user", "courseTest", "courseTestQuestion", "answer_id_list")
    readonly_fields = ("courseTest", "courseTestQuestion", "answer_id_list", "date_of_add", "date_of_update")
class CourseTestUserAction(Model):
    
    class Meta:
        verbose_name = "Ответ пользователя на вопросы теста"
        verbose_name_plural = "Ответы пользователей на вопросы тестов"

    id: AutoField = AutoField(primary_key=True)
    user: ForeignKey = ForeignKey(to=User, blank=False, null=False, on_delete=CASCADE)
    courseTest: ForeignKey = ForeignKey(to=CourseTest, on_delete = CASCADE)
    courseTestUser: ForeignKey = ForeignKey(to=CourseTestUser, null=True, on_delete = CASCADE)
    courseTestQuestion: ForeignKey = ForeignKey(to=CourseTestQuestion, on_delete = CASCADE)
    #courseTestQuestionAnswer: ForeignKey = ForeignKey(to=CourseTestQuestionAnswer, on_delete = CASCADE)
    answer_id_list: CharField = CharField("Список id выбранных ответов", max_length=1024, blank=True, null=True)

    date_of_add: DateTimeField = DateTimeField(null=True, blank=True, editable = False)
    date_of_update: DateTimeField = DateTimeField(null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if self.date_of_add is None:
            self.date_of_add = datetime.now(tz=timezone.utc)
        self.date_of_update = datetime.now(tz=timezone.utc)
        super(CourseTestUserAction, self).save(*args, **kwargs)








class UserCourseAccessAdmin(ModelAdmin):
    list_display = ("id", "user", "course", "is_active", "is_active_with_deadline", "is_passed", "date_of_passed")
    readonly_fields = ("is_passed", "date_of_passed")
class UserCourseAccess(Model):

    class Meta:
        verbose_name = "Доступ пользователя"
        verbose_name_plural = "Доступы пользователей"
        
    id: AutoField = AutoField(primary_key=True)
    user: ForeignKey = ForeignKey(to=User, blank=False, null=False, on_delete=CASCADE)
    course: ForeignKey = ForeignKey(to=Course, on_delete = CASCADE)
    is_active = BooleanField("Доступен?", default=False)
    is_active_with_deadline = BooleanField("Ограничен по времени?", default=False)
    """Статус временного доступа"""

    deadline_date_since: DateField = DateField("Дата октрытия доступа (при дедлайне)", null=True, blank=True)
    deadline_date_until: DateField = DateField("Дата закрытия доступа (при дедлайне)", null=True, blank=True)

    is_passed = BooleanField("Сдан?", default=False)
    date_of_passed: DateTimeField = DateTimeField("Дата сдачи курса пользователем", null=True, blank=True)




class UserDataAdmin(ModelAdmin):
    list_display = ("id", "user")
    readonly_fields = ("user", "date_of_add", "date_of_update")

class UserData(Model):
    """Для дополнительных полей в профиле"""
    
    class Meta:
        verbose_name = "Данные"
        verbose_name_plural = "Данные пользователей"

    id: AutoField = AutoField(primary_key=True)

    user: OneToOneField = OneToOneField(User, blank=False, null=False, on_delete=CASCADE)
    patronymic: CharField = CharField("Отчество", max_length=516, blank=True, null=True)
    comment: TextField = TextField("Комментарий", blank=True, null=True)

    date_of_add: DateTimeField = DateTimeField(null=True, blank=True, editable = False)
    date_of_update: DateTimeField = DateTimeField(null=True, blank=True, editable = False)

    def save(self, *args, **kwargs):
        if self.date_of_add is None:
            self.date_of_add = datetime.now(tz=timezone.utc)
        self.date_of_update = datetime.now(tz=timezone.utc)
        super(UserData, self).save(*args, **kwargs)
