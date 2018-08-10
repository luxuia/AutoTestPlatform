import cv2
import numpy as np
import sys

def matchTemplate(image, template_path, method):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    channels = cv2.split(template)
    zero_channel = np.zeros_like(channels[0])
    mask = np.array(channels[3])

    mask[channels[3] == 0] = 1
    mask[channels[3] == 100] = 0

    transparent_mask = cv2.merge([zero_channel, zero_channel, zero_channel, mask])

    result = cv.matchTemplate(image, template, method, transparent_mask)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(' lowest squard difference with mask', min_val, max_val, min_loc, max_loc)

    return min_val, max_val, min_loc, max_loc

if __name__ == '__main__':
    image = cv2.imread('../../')
