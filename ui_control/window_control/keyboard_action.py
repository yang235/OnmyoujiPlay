from time import sleep

import keyboard


def board_press(action):
    # action is str
    sleep(1)
    keyboard.press_and_release(action)