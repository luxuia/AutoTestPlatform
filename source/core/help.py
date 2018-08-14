# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import json

EXPORT_RES = '__export_res__'

class G(object):
    DEVICE = None

class Config(object):
    OP_DELAY = 0.5
    FIND_TIMEOUT = 1


class Res(object):
    @classmethod
    def get_cfg(cls, filename):
        if not filename.endswith('.meta'):
            filename = filename + '.meta'
        with open(filename, 'r') as f:
            cfg = json.loads(f.read())
            return cfg

    @classmethod
    def get_image(cls, filename):
        if not filename.endswith('.png'):
            filename = filename + '.png'
        return cv.imread(EXPORT_RES + '/' + filename, cv.IMREAD_UNCHANGED)
