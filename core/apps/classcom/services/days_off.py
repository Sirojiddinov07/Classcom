from core.apps.classcom import models
from typing import Union, List, Optional
from django.db.models import Q
from .date import DateService
import pandas as pd
from datetime import datetime


class DaysOffService:
    def __init__(self) -> None:
        ...

    def get_daysoff_from_user(
        self,
        user_id: int,
        science: Optional[List[Union[int, models.Science]]] = None,
        classes: Optional[List[Union[int, models.Classes]]] = None,
        date_lte: Optional[str] = None,
        date_gte: Optional[str] = None,
        weekdays: Optional[List[int]] = [],
    ) -> Union[int]:
        """User dam olish kunlarini filter qilib beradi.

        Args:
            user_id (int): _description_
            science (Optional[List[Union[int, models.Science]]], optional): _description_. Defaults to None.
            classes (Optional[List[Union[int, models.Classes]]], optional): _description_. Defaults to None.
            date_lte (Optional[str], optional): _description_. Defaults to None.
            date_gte (Optional[str], optional): _description_. Defaults to None.

        Returns:
            _type_: DaysOff model
        """
        query = Q(user_id=user_id) | Q(user__isnull=True)
        date_gte = DateService().format_date(date_gte)
        date_lte = DateService().format_date(date_lte)

        if science:
            query &= Q(science__in=science)
        if classes:
            query &= Q(_class__in=classes)
        if date_gte:
            query &= Q(to_date__gte=date_gte)
        if date_lte:
            query &= Q(from_date__lte=date_lte)
        else:
            query &= Q(from_date__lte=datetime.now())

        obj = models.DaysOff.objects.filter(query)
        response = pd.DatetimeIndex([])
        for date in obj:
            response = response.union(
                DateService().weekday_counter(
                    date.from_date.strftime("%d.%m.%Y"),
                    date.to_date.strftime("%d.%m.%Y"),
                    weekdays,
                )
            )
        return response.unique().size
