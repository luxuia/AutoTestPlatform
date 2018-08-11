import cv2 as cv
import numpy as np
import sys

UNIT_TEST_RES_PATH = '../../example/cv_test/'

"""
method = cv2.TM_SQDIFF or cv2.TM_CCORR_NORMED
"""
def matchTemplate(image, template, method = cv.TM_SQDIFF):
    assert(method in [cv.TM_SQDIFF, cv.TM_CCORR_NORMED])

    channels = cv.split(template)
    zero_channel = np.zeros_like(channels[0])
    mask = np.array(channels[3])

    transparent_mask = cv.merge([mask, mask, mask, mask])

    result = cv.matchTemplate(image, template, method, None, transparent_mask)

    cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result, None)

    print(' lowest squard difference with mask', min_val, max_val, min_loc, max_loc)

    if method == cv.TM_SQDIFF or method == cv.TM_SQDIFF_NORMED:
        return min_val, min_loc, result
    else:
        return max_val, max_loc, result

def matchTemplateMultiScale(image, template, method = cv.TM_SQDIFF, scale=3):
    #TODO

if __name__ == '__main__':
    image = cv.imread(UNIT_TEST_RES_PATH + 'game_frame.png', cv.IMREAD_UNCHANGED)
    template = cv.imread(UNIT_TEST_RES_PATH + 'template.png', cv.IMREAD_UNCHANGED)

    img_display = image.copy()

    image_window = "Source Image"
    result_window = 'Result Image'

    cv.namedWindow( image_window, cv.WINDOW_AUTOSIZE)
    cv.namedWindow( result_window, cv.WINDOW_AUTOSIZE)

    match_val, match_loc, result = matchTemplate(image, template, cv.TM_CCORR_NORMED)

    cv.rectangle(img_display, match_loc, (match_loc[0]+template.shape[0], match_loc[1]+template.shape[1]), (0, 0, 0), 2, 8, 0)
    cv.rectangle(result, match_loc, (match_loc[0]+template.shape[0], match_loc[1]+template.shape[1]), (0, 0, 0), 2, 8, 0)

    cv.imshow(image_window, img_display)
    cv.imshow(result_window, result)

    cv.waitKey(0)
