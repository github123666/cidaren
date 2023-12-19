import time


def create_timestamp() -> int:
    return int(time.time() * 1000)
