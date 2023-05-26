import time

import redis

from constants import REDIS_RETRY_BACKOFF_SECONDS, REDIS_MAX_RETRIES


def redis_command(command, *args):
    count = 0
    while True:
        try:
            return command(*args)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
            count += 1
            if count > REDIS_MAX_RETRIES:
                raise Exception("Retrying in {} second(s)".format(REDIS_RETRY_BACKOFF_SECONDS))
            time.sleep(REDIS_RETRY_BACKOFF_SECONDS)
