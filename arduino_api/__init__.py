"""
Arduino mouse and keyboard API for python.

"""

import time
import numpy
import pyautogui
from serial.serialwin32 import Serial

PORT = None

UPPER_LIMIT = 120
LOWER_LIMIT = -120
ENDING_SIGN = '`'
INT_STARTING_SIGN = '|'
STRING_STARTING_SIGN = '%'


def ard_init(port: int) -> None:
    """ Init Arduino. """
    global PORT
    PORT = f"COM{port}"


def send_string(data: str):
    """ Send string to Arduino. """
    arduino = Serial(PORT)
    arduino.write(f'{STRING_STARTING_SIGN}{data}{ENDING_SIGN}'.encode('utf-8'))


def send_ascii(char: int):
    """ Send char in ascii code. """
    arduino = Serial(PORT)
    arduino.write(f'{INT_STARTING_SIGN}{char}{ENDING_SIGN}'.encode('utf-8'))


def hold_right():
    release_buttons()
    _send('r')


def hold_left() -> None:
    release_buttons()
    _send('l')


def release_buttons():
    """Realease all keyboard and mouse buttons.
    """
    _send('x')


def click(sleep: bool = False):
    _send('c')
    if sleep:
        time.sleep(0.5)


def _send(data):
    """ Send encoded data to Arduino port."""
    arduino = Serial(PORT)
    arduino.write(f'{data}{ENDING_SIGN}'.encode('utf-8'))


def ard_mouse_to_pos(target_pos: tuple, sleep: bool = False):
    """ Move to the given pixel the screen. """
    pos = pyautogui.position()
    pos = numpy.array([pos.x, pos.y])
    vector = (
        target_pos[0] - pos[0],
        target_pos[1] - pos[1],
    )
    _send(f'{vector[0]}:{vector[1]}')
    if sleep:
        time.sleep(0.5)


def mouse_move(pos):
    """ Move by delta. """
    _send(f'{pos[0]}:{pos[1]}')
