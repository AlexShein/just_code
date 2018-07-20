import asyncio
import logging
import time
import urllib.request
from multiprocessing.dummy import Pool

log = logging.getLogger('perfomance_test')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

URLS = [
    'http://weather.com',
    'http://google.com',
    'http://yandex.ru',
    'http://wikipedia.org',
    'http://habrahabr.ru',
    'http://ostrovok.org',
    'http://booking.com',
    'http://www.kaggle.com',
    'http://www.habr.com',
    'http://www.gitlab.com',
    'http://www.github.com',
]


def sync():
    start = time.time()
    for i, result in enumerate([
        urllib.request.urlopen(url)
        for url in URLS
    ]):
        pass
        # log.info(f'{i}, {result.url}, {result.read().decode("utf-8").count("<")}')
    log.info(f'###Sync execution took {time.time()-start:.2f}')


def sync_threading():
    start = time.time()
    with Pool() as pool:
        results = pool.map(lambda url: urllib.request.urlopen(url), URLS)
    for i, result in enumerate(results):
        pass
        # log.info(f'{i}, {result.url}, {result.read().decode("utf-8").count("<")}')
    log.info(f'###Sync execution with threading took {time.time()-start:.2f}')


async def main():
    start = time.time()
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None,
            urllib.request.urlopen,
            url
        )
        for url in URLS
    ]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        # log.info(f'{i}, {result.url}, {result.read().decode("utf-8").count("<")}')
    log.info(f'###Async execution took {time.time()-start:.2f}')

sync()
sync_threading()

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
ioloop.close()

# Gives output like
# 2018-07-20 10:33:54,303 - perfomance_test - INFO - ###Sync execution took 9.75
# 2018-07-20 10:33:56,267 - perfomance_test - INFO - ###Sync execution with threading took 1.96
# 2018-07-20 10:33:56,291 - asyncio - DEBUG - Using selector: KqueueSelector
# 2018-07-20 10:33:57,695 - perfomance_test - INFO - ###Async execution took 1.40
