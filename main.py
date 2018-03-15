# -*- coding: utf-8 -*-

import win32gui
import win32api

import multiprocessing, time

from config.work import config

TITLE_BAR_W = -100
TITLE_BAR_H = 22

def EnumWindows():
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
        if app[2] == config['app']:
            return item, app

def run():
    hwnd, app = EnumWindows()
    print('start run')
    dc = win32gui.CreateDC('DISPLAY', None, None)
    rect = app[3]
    while True:
        x, y = win32api.GetCursorPos()
        time.sleep(0.01)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)

        width = right - left
        heigh = top - bottom

        win32gui.DrawText(dc, '测试', -1, (left+TITLE_BAR_W,top+TITLE_BAR_H,1980,1080), 0)

        for work in config['work']:
            region = work['region']

            x1 = left + region[0]['x_px'] + width*region[0]['x'] + TITLE_BAR_W
            x2 = left + region[1]['x_px'] + width*region[1]['x'] + TITLE_BAR_W
            y1 = top + region[0]['y_px'] + heigh*region[0]['y'] + TITLE_BAR_H
            y2 = top + region[1]['y_px'] + heigh*region[1]['y'] + TITLE_BAR_H
#            win32gui.MoveToEx(dc, x1, y1)
#            win32gui.LineTo(dc, x2, y1)
#            win32gui.Polyline(dc, [(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

   
if __name__ == '__main__':
    print('start')
    p = multiprocessing.Process(target=run);

    p.start();
    p.join();
    print('end')