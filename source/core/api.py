# -*- coding: utf-8 -*-

from .help import *
from .cv import *

def isnumber(v):
    return type(v) in [type(1), type(1.1)]

def sleep(secs = 1.0):
    time.sleep(secs)

def wait(v, timeout):
    #TODO
    pos = loop_find(v, timeout)


def click(v, times=1):
    if isinstance(v, Template):
        pos = loop_find(v, timeout=Config.FIND_TIMEOUT)
    else:
        pos = v

    for _ in range(times):
        G.DEVICE.touch(pos)

        sleep(0.1)

    sleep(Config.OP_DELAY)

touch = click

def double_click(v):
    if isinstance(v, Template):
        pos = loop_find(v, timeout=ST.FIND_TIMEOUT)
    else:
        pos = v
    for _ in range(times):
        G.DEVICE.double_click(pos)

        sleep(0.1)

    sleep(Config.OP_DELAY)

def text(text, enter=True):
    G.DEVICE.text(text)
