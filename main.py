# -*- coding: utf-8 -*-
from source.gui.gui import guimain
from source.core.help import G
from source.core.win.win import Window
import sys, os

from inspect import currentframe

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

if __name__ == '__main__':
    G.ROOT_PATH = os.path.abspath('.').replace('\\', '/')
    print(G.ROOT_PATH)

    G.DEVICE = Window(title='钉钉')
    
    guimain()
