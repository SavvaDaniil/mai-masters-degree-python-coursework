from dataclasses import dataclass, asdict
import json
from typing import Union

from maionline.viewmodel.CourseTestViewModel import CourseTestUserStatusViewModel

@dataclass
class BaseResponse():
    error: Union[str, None] = None
    courseTestUserStatusViewModel: Union[CourseTestUserStatusViewModel, None] = None


    @property
    def __dict__(self):
        """
        get a python dictionary
        """
        return asdict(self)
        
    @property
    def json(self):
        """
        get the json formated string
        """
        return json.dumps(self.__dict__)