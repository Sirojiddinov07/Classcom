"""
Service for working with dates
"""

from datetime import datetime
from typing import List, Union

import pandas as pd

from core.apps.classcom.choices import Weekday


class DateService:
    def __init__(self) -> None:
        ...

    def weekday_counter(
        self, start_date, end_date, weekdays: Union[List[int]] = []
    ) -> object:
        """Weekdays counter

        Args:
            start_date (date): start date example: 23.09-2005
            end_date (date): end date example: 23.10.2005
            weekdays (list): list of weekdays to count (0=Monday, 6=Sunday)
        Returns:
            int: count of weekdays
        """
        date = pd.date_range(
            start=self.format_date(start_date), end=self.format_date(end_date)
        )
        return date[date.weekday.isin(weekdays)]

    def weekday_index(self, name: Union[str]) -> int:
        """Get weekday index by name.

        Args:
            name (Union[str]): Weekday name

        Returns:
            int: Weekday index.
        """
        match name:
            case "Monday" | Weekday.monday:
                return 0
            case "Tuesday" | Weekday.tuesday:
                return 1
            case "Wednesday" | Weekday.wednesday:
                return 2
            case "Thursday" | Weekday.thursday:
                return 3
            case "Friday" | Weekday.friday:
                return 4
            case "Saturday" | Weekday.saturday:
                return 5
            case "Sunday" | Weekday.sunday:
                return 6
            case _:
                return -1

    def format_date(self, date: str) -> str:
        if not date:
            return None
        return datetime.strptime(date, "%d.%m.%Y")
