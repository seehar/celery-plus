import asyncio
import datetime
import logging
import time
import uuid
from abc import ABCMeta
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union


if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    from celery import Celery
    from celery.canvas import Signature
    from celery.schedules import crontab


class IScheduler(metaclass=ABCMeta):
    @abstractmethod
    def register(self, sender: "Celery") -> None:
        """
        Register the scheduler to the celery app
        :param sender: celery application
        :return:
        """

    @staticmethod
    def execute_task_every_second(
        task_func: Callable, second: int, args: Optional[List[Any]] = None
    ) -> None:
        """
        分钟内秒级任务调度
        :param task_func: 要执行的函数
        :param second:
        :param args:
        :return:
        """
        task_start_time = datetime.datetime.now()
        while True:
            now = datetime.datetime.now()
            if now.minute != task_start_time.minute:
                break

            task_func.apply_async(args=args)  # noqa
            time.sleep(second)

    @staticmethod
    def add_periodic_task(
        sender: "Celery",
        schedule: Union[int, "crontab"],
        sig: "Signature",
        args: Tuple[Any] = (),
        kwargs: Tuple[Any] = (),
        name: Optional[str] = None,
        **opts
    ) -> None:
        if not name:
            name = str(sig.task) + uuid.uuid4().hex
        sender.add_periodic_task(schedule, sig, args, kwargs, name, **opts)

    @property
    def asyncio_loop(self) -> "AbstractEventLoop":
        try:
            loop = asyncio.get_event_loop()
        except Exception as e:
            logging.exception(e)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
        return loop
