# -*- coding: utf-8 -*-
from source.gui.gui import guimain
from source.core.help import G
from source.core.win.win import Window
import sys



if __name__ == '__main__':

    G.DEVICE = Window(title='钉钉') 

    guimain()
