import time
import twint

from functools import wraps


def empty_retry(tries=3, delay=3, backoff=2):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                twint.output.clean_lists()
                result = f(*args, **kwargs)
                if result:
                    return result

                print(f'Retrying.. (tries left = {mtries - 1})')
                time.sleep(mdelay)

                mtries -= 1
                mdelay *= backoff
            twint.output.clean_lists()
            return f(*args, **kwargs)
        return f_retry

    return deco_retry
