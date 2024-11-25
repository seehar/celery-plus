from inspect import getmembers
from inspect import isclass
from types import ModuleType
from typing import TYPE_CHECKING

from .ischeduler import IScheduler
from .utils.time_util import wait_time


if TYPE_CHECKING:
    from celery import Celery


def celery_plus_setup(sender: "Celery", scheduler_module: ModuleType):
    classes = getmembers(scheduler_module, isclass)
    for class_name, class_ in classes:
        class_().register(sender)


__all__ = ("IScheduler", "celery_plus_setup", "wait_time")
