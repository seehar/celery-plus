import time
from datetime import datetime
from datetime import timedelta


def wait_time(
    hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0
) -> None:
    now = datetime.now()
    target_time = now.replace(
        hour=hour, minute=minute, second=second, microsecond=microsecond
    )
    if now > target_time:
        target_time += timedelta(days=1)

    delay = (target_time - now).total_seconds()
    if delay > 0:
        time.sleep(delay)
