from pywinauto.application import Application
from pywinauto.win32functions import SetForegroundWindow
from pywinauto import mouse, keyboard

from .screenshot import screenshot, find_window
import socket

class Window():
    """ Main """

    def __init__(self, handle=None, title=None):
        if title is not None:
            handle = find_window(title)

        self.app = None
        self.handle = int(handle) if handle else None

        self._app = Application()
        self._top_window = None
        self._focus_rect = (0, 0, 0, 0)
        self.mouse = mouse
        self.keyboard = keyboard

        self._init_connect(handle)

    @property
    def uuid(self):
        return self.handle

    def _init_connect(self, handle):
        if handle:
            self.connect(handle=handle)

    def connect(self, handle=None):
        if handle:
            handle = int(handle)
            self.app = self._app.connect(handle = handle)
            self._top_window = self.app.window(handle=handle).wrapper_object()
        else:
            error('no handle pass')
        self.set_foreground()

    def snapshot(self, filename = None):
        screen = screenshot(self.handle)

        if filename is not None:
            print('save to ' + filename)

    def keyevent(self, keyname):
        """
            https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
        """
        self.keyboard.SendKeys(keyname)

    def text(self, text):
        self.keyevent(text)

    def touch(self, pos, **kwargs):
        """
        https://pywinauto.readthedocs.io/en/latest/code/pywinauto.mouse.html
        """
        duration = kwargs.get("duration", 0.01)
        right_click = kwargs.get('right_click', False)
        button = 'right' if right_click else 'left'
        coords = self._action_pos(pos)

        self.mouse.press(button=button, coords=coords)
        time.sleep(duration)
        self.mouse.release(button=button, coords=coords)

    def double_click(self, pos):
        coords = self._action_pos(pos)
        self.mouse.double_click(coords = coords)

    def swipe(self, p1, p2, duration=0.8, steps=5):
        from_x, from_y = self._action_pos(p1)
        to_x, to_y = self._action_pos(p2)

        interval = float(duration)/(steps+1)
        self.mouse.press(coords=(from_x, from_y))
        time.sleep(interval)

        for i in range(1, steps):
            self.mouse.move(coords=(
                    int(from_x+(to_x-from_x)*i/steps),
                    int(from_y+(to_y-from_y)*i/steps),
                ))
            time.sleep(interval)
        for i in range(10):
            self.mouse.move(coords=(to_x, to_y))
        time.sleep(interval)
        self.mouse.release(coords=(to_x, to_y))


    def _action_pos(self, pos):
        if self.app:
            pos = self._windowpos_to_screenpos(pos)
        pos = (int(pos[0], int(pos[1])))
        return pos

    def set_foreground(self):
        SetForegroundWindow(self._top_window)

    def get_rect(self):
        """
        Get rectangle
        Returns:
            None
        """
        return self._top_window.rectangle()

    @property
    def focus_rect(self):
        return self._focus_rect

    @focus_rect.setter
    def focus_rect(self, value):
        # set focus rect to get rid of window border
        assert len(value) == 4, "focus rect must be in [left, top, right, bottom]"
        self._focus_rect = value

    def get_current_resolution(self):
        rect = self.get_rect()
        w = (rect.right + self._focus_rect[2]) - (rect.left + self._focus_rect[0])
        h = (rect.bottom + self._focus_rect[3]) - (rect.top + self._focus_rect[1])
        return w, h

    def _windowpos_to_screenpos(self, pos):
        """
        Convert given position relative to window topleft corner to screen coordinates
        Args:
            pos: coordinates (x, y)
        Returns:
            converted position coordinates
        """
        rect = self.get_rect()
        pos = (int((pos[0] + rect.left + self._focus_rect[0]) * self._dpifactor), 
            int((pos[1] + rect.top + self._focus_rect[1]) * self._dpifactor))
        return pos

    def get_ip_address(self):
        """
        Return default external ip address of the windows os.
        Returns:
             :py:obj:`str`: ip address
        """
        return socket.gethostbyname(socket.gethostname())
    

    


