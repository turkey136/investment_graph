# -*- coding: utf-8 -*-
import collections

def check_vary_code(last_day_close_value, close_value):
    if last_day_close_value != None:
        if close_value == last_day_close_value:
            return 0
        elif close_value > last_day_close_value:
            return 1
        else:
            return -1
    else:
        return None

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el