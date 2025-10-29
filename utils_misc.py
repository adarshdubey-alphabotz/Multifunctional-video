# utils_misc.py
def parse_time_str(timestr):
    mins, secs = map(int, timestr.strip().split(":"))
    return mins * 60 + secs
