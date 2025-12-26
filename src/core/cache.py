import time
from threading import Lock
from collections import defaultdict
from src.core.posts import get_thread_info

THREAD_CACHE = {}
CACHE_TTL = 600

CACHE_LOCK = Lock()
KEY_LOCKS = defaultdict(Lock)

def get_thread_info_cached(board, thread_no):
    key = f"{board}:{thread_no}"
    now = time.monotonic()

    with CACHE_LOCK:
        cached = THREAD_CACHE.get(key)
        if cached and now - cached["time"] < CACHE_TTL:
            return cached["data"]

    with KEY_LOCKS[key]:
        with CACHE_LOCK:
            cached = THREAD_CACHE.get(key)
            if cached and now - cached["time"] < CACHE_TTL:
                return cached["data"]

        data = get_thread_info(board, thread_no)

        with CACHE_LOCK:
            THREAD_CACHE[key] = {
                "time": time.monotonic(),
                "data": data
            }

        return data