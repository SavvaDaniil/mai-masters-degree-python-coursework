
from typing import List, Union
from maionline.models import Course

class CourseRepository():

    def find_by_id(self, course_id: int) -> Union[Course, None]:
        try:
            return Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return None

    def list_active(self) -> List[Course]:
        return Course.objects.filter(is_active=True).order_by("name").all()