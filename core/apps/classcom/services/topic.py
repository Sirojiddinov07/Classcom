from typing import Type, Union

import pandas as pd
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _

from common.env import env
from core.apps.classcom import models

from .date import DateService
from .days_off import DaysOffService
from .schedule import ScheduleService


class TopicService:
    def __init__(self) -> None: ...

    def get_topic_by_date(
        self,
        date: Union[str],
        science_id: Union[int],
        class_id: Union[int],
        user: Union[Type[models.User]] = None,
    ) -> models.Topic:
        """Get topic by date.

        Args:
            date (str): _description_

        Returns:
            _type_: Topic model
        """
        weekdays = ScheduleService().get_weekdays(user)
        topics_count = DateService().weekday_counter(
            env.str("START_DATE"), date, weekdays
        )
        days_off = DaysOffService().get_daysoff_from_user(
            user.id, weekdays=weekdays
        )

        topics = models.Topic.objects.filter(
            science_id=science_id,
            _class_id=class_id,
        )
        topic = topics.filter(
            sequence_number=(topics_count.size - days_off) - 1
        ).first()
        
        if topic is None:
            raise ValueError(_("No topic found for this date"))
        if topics_count.size == 0:
            raise ValueError(_("You have no topics"))

        return topic

    def all_topics(
        self, science_id: int, class_id: int
    ) -> QuerySet[models.Topic]:
        """Get all topics for a class.

        Args:
            science_id (int): _description_
            class_id (int): _description_

        Returns:
            _type_: Topic model
        """

        return models.Topic.objects.filter(
            science_id=science_id, class_id=class_id
        ).order_by("sequence_number")

    def import_plan(self, file: Union[str]):
        """Excel import topics list id,name,quarter

        Args:
            file (Union[str]): Excel file path
        """
        data = pd.read_excel(file)
        for item in data.iloc:
            try:
                topic = models.Topic(
                    sequence_number=item["id"],
                    name=item["name"],
                    quarter_id=item["quarter"],
                    science_id=item["science"],
                    _class_id=item["class"],
                )
                topic.save()
            except Exception as e:
                print(e)
