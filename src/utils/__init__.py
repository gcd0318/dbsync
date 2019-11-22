import time

def timestamp(t=None, fmt='%Y%m%d_%H%M%S'):
    if t is None:
        t = time.localtime()
    return time.strftime(fmt, t)