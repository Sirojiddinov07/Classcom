"""
Service for working with dates
"""

import pandas as pd
from typing import List, Union
from datetime import datetime


class DateService:
    def __init__(self) -> None:
        ...

    def weekday_counter(
        self, start_date, end_date, weekdays: Union[List[int]] = []
    ) -> int:
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
            case "Monday":
                return 0
            case "Tuesday":
                return 1
            case "Wednesday":
                return 2
            case "Thursday":
                return 3
            case "Friday":
                return 4
            case "Saturday":
                return 5
            case "Sunday":
                return 6
            case _:
                return -1

    def format_date(self, date: str) -> str:
        if not date:
            return None
        return datetime.strptime(date, "%d.%m.%Y")
