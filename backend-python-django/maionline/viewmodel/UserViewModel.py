
from dataclasses import dataclass
from typing import Union

@dataclass
class UserProfileViewModel:
    username: str
    firstname: Union[str, None] = None
    lastname: Union[str, None] = None
    patronymic: Union[str, None] = None
