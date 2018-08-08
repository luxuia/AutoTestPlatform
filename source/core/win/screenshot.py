# -*- coding: utf-8 -*-

import win32gui
import win32api
import win32ui
import win32con
#import ctypes

import numpy as np
import cv2

SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

def find_window(title):
    def _EnumWindowCallback( hwnd, windows):
        temp = []
        temp.append(hex(hwnd))
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if right > 0 and bottom > 0 and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            temp.append(win32gui.GetClassName(hwnd))
            temp.append(win32gui.GetWindowText(hwnd))
            temp.append( (left, top, right, bottom) )
            windows[hwnd] = temp

    windows = {}
    win32gui.EnumWindows(_EnumWindowCallback, windows)
    print('total window with %d classes', (len(windows)))

    for item in windows:
        app = windows[item]
        print(app)
        if app[2] == title:
            return item

def screenshot(hwnd=None, title=None):
    if hwnd is None and title is not None:
        hwnd = find_window(title)
    #rect = app[3]

    dc = win32gui.CreateDC('DISPLAY', None, None)

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    width = right - left
    height = bottom - top

    #user32 = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
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

    bmpInt = np.array(bmpInt, dtype=np.uint8).reshape(height, width, 4)

    return bmpInt, width, height
   
if __name__ == '__main__':
    #multiprocessing.Process(target = run)
    img, width, height = screenshot(title='钉钉')

    cv2.imshow('image', img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()