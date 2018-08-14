from .help import *
from .cv_help import *
import cv2 as cv
from .help import G

def loop_find(template, timeout=1, interval=0.5, intervalfunc=None):
    while True:
        screen = G.DEVICE.snapshot()

        if screen is None:
            print('screen is None')
        else:
            return template.match_in(screen)



class Template(object):
    def __init__(self, filename):
        self.filename = filename
        self.cfg = self._get_cfg()

    def _get_cfg(self):
        return Res.get_cfg(self.filename)


    def match_in(self, screen):
        return self._cv_match(screen)

    def _cv_match(self, screen):
        image = Res.get_image(self.filename)
        ret = None

        ret = self._find_template(image, screen)

        return ret

    def _find_template(self, image, screen):
        return matchTemplate(image, screen, cv.TM_CCORR_NORMED)
