from typing import List, Union
from maionline.models import CourseTest

class CoureTestRepository():

    def find_by_id(self, id: int) -> Union[CourseTest, None]:
        try:
            return CourseTest.objects.get(id=id)
        except CourseTest.DoesNotExist:
            return None