import cProfile
from datetime import datetime

def func_profile(func):
    def decorator(*args, **kwargs):
        fpath = '/Users/datnguyen/workspace/projects/PW_emarch/profile_{}.prof'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
        profile = cProfile.Profile()
        result = profile.runcall(func, *args, **kwargs)
        profile.dump_stats(fpath)
        return result

    return decorator

