from inspect import getmembers
from inspect import isclass
from types import ModuleType

from celery import Celery

from .ischeduler import IScheduler


def setup_periodic_task(sender: Celery, scheduler_module: ModuleType):
    classes = getmembers(scheduler_module, isclass)
    for class_name, class_ in classes:
        class_().scheduler_register(sender)


__all__ = ("IScheduler", "setup_periodic_task")
