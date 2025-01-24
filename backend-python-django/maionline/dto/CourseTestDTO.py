
from django.forms import Form, CharField, IntegerField


class CourseTestUserCommandDTO(Form):
    """Форма для аутентификации пользователя"""
    course_test_id: IntegerField = IntegerField(required=True)
    command: CharField = CharField(max_length=512, required=True)

    course_test_question_id: IntegerField = IntegerField(required=False)
    course_test_question_number: IntegerField = IntegerField(required=False)
    answer_ids_list: CharField = CharField(max_length=1024, required=False)