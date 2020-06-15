import foohid
from config import MOUSE_SPEED

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap


MOUSE_UP_KEY = 'mouse_up_key'
MOUSE_DOWN_KEY = 'mouse_down_key'
MOUSE_LEFT_KEY = 'mouse_left_key'
MOUSE_RIGHT_KEY = 'mouse_right_key'
MOUSE_CLICK_KEY = 'mouse_left_click'
MOUSE_KEYS = [MOUSE_UP_KEY, MOUSE_DOWN_KEY, MOUSE_LEFT_KEY, MOUSE_RIGHT_KEY, MOUSE_CLICK_KEY]


class VirtualMouse:
    _CALLBACK = None

    @staticmethod
    def left_click():
        def mouse_event(type, posx, posy):
            event = CGEventCreateMouseEvent(None, type, (posx, posy), kCGMouseButtonLeft)
            CGEventPost(kCGHIDEventTap, event)

        def mouse_click(posx, posy):
            mouse_event(kCGEventLeftMouseDown, posx, posy)
            mouse_event(kCGEventLeftMouseUp, posx, posy)

        mouse_click(500, 500)

    @staticmethod
    def _move_down():
        foohid.move_mouse(0, 1 * MOUSE_SPEED)

    @staticmethod
    def _move_up():
        foohid.move_mouse(0, -1 * MOUSE_SPEED)

    @staticmethod
    def _move_left():
        foohid.move_mouse(-1 * MOUSE_SPEED, 0)

    @staticmethod
    def _move_right():
        foohid.move_mouse(1 * MOUSE_SPEED, 0)

    @classmethod
    def hold_down(cls):
        cls._CALLBACK = VirtualMouse._move_down

    @classmethod
    def hold_up(cls):
        cls._CALLBACK = VirtualMouse._move_up

    @classmethod
    def hold_left(cls):
        cls._CALLBACK = VirtualMouse._move_left

    @classmethod
    def hold_right(cls):
        cls._CALLBACK = VirtualMouse._move_right

    @classmethod
    def clear(cls):
        cls._CALLBACK = None

    @classmethod
    def run_callback(cls):
        if cls._CALLBACK:
            cls._CALLBACK()
