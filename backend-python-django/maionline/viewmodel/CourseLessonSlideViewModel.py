from typing import Union
from dataclasses import dataclass

@dataclass
class CourseLessonSlideLiteViewModel:
    id: int
    url: Union[str, None] = None
    order_in_list: int = 0