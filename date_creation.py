import time


# random date creation code
def date_between(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_string_date(start, end, prop):
    return date_between(start, end, '%d/%m/%Y', prop)
