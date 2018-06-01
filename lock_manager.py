import logging

from redis.exceptions import LockError
from redis.lock import Lock

from app.client.redis import redis_client

log = logging.getLogger(__name__)


class LockManager():

    def __init__(self, lock_name, lock_timeout=10):
        self.lock_name = lock_name
        self.lock_timeout = lock_timeout
        self.is_lock_free = False

    def __enter__(self):
        self.lock = Lock(
            redis_client,
            self.lock_name,
            blocking_timeout=1,
            timeout=self.lock_timeout,
        )
        try:
            self.is_lock_free = self.lock.acquire(blocking=False)
        except LockError:
            log.error(
                'lock acquire error',
                extra={'data': {'lock_name': self.lock_name}},
                exc_info=True,
            )
        return self

    def __exit__(self, type, value, traceback):
        if self.is_lock_free:
            try:
                self.lock.release()
            except LockError:
                log.error(
                    'lock release error',
                    extra={'data': {'lock_name': self.lock_name}},
                    exc_info=True,
                )

