from typing import List, Type, Union

from core.apps.classcom import services
from core.http.models import User


class ScheduleService:
    def __init__(self) -> None: ...

    def get_weekdays(self, user: Union[Type[User]]) -> List[int]:
        """Get weekdays for a user.

        Args:
            user (Union[Type[User]]): _description_

        Returns:
            _type_: _description_
        """
        schedule = user.schedules.all()
        weekdays = []
        for s in schedule:
            weekdays.append(services.DateService().weekday_index(s.weekday))
        return weekdays
