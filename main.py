# -*- coding: utf-8 -*-

from config.work import config
import ctypes
import cv2
import multiprocessing
import numpy as np
import time
import win32api
import win32con
import win32gui
import win32ui

TITLE_BAR_W = 2
TITLE_BAR_H = 22


def enum_windows():
    def _enum_window_callback(hwnd, windows):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if right > 0 and bottom > 0 and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            window_text = win32gui.GetWindowText(hwnd)
            window = {
                'ClassName': class_name,
                'WindowText': window_text,
                'Coordinates': (left, top, right, bottom),
                'HWND': hwnd
            }
            windows[class_name] = window

    windows = {}
    win32gui.enum_windows(_enum_window_callback, windows)
    print('total window with {} classes'.format(len(windows)))

    window = windows.get(config['app']):
    if window:
        return window['HWND'], window
    return None


def get_image():
    hwnd, app = EnumWindows()
    print('start run')
    rect = app['Coordinates']

    dc = win32gui.CreateDC('DISPLAY', None, None)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    width = right - left
    height = bottom - top

    user32 = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
    hwindc = win32gui.GetWindowDC(hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)  #用dc来获取全屏的截图

    memdc = srcdc.CreateCompatibleDC()

    bmp = win32ui.CreateBitmap()

    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)

    memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)
    #
    #user32.PrintWindow(hwnd, memdc.GetSafeHdc(), 0)
    bmpinfo = bmp.GetInfo()
    bmpInt = bmp.GetBitmapBits(False)

    return bmpInt, width, height


def do_work(image, work):
    print(work)


if __name__ == '__main__':
    #multiprocessing.Process(target = run)
    img, width, height = get_image()
    img = np.array(img, dtype=np.uint8).reshape(height, width, 4)

    for work in config['work']:
        do_work(img, work)

    cv2.imshow('image', img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
