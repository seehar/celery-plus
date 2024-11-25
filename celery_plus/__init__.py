from inspect import getmembers
from inspect import isclass
from types import ModuleType
from typing import TYPE_CHECKING

from .ischeduler import IScheduler
from .utils.time_util import wait_time


if TYPE_CHECKING:
    from celery import Celery


def setup_periodic_task(sender: "Celery", scheduler_module: ModuleType):
    classes = getmembers(scheduler_module, isclass)
    for class_name, class_ in classes:
        class_(sender).register()


__all__ = ("IScheduler", "setup_periodic_task", "wait_time")
