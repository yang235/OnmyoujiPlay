import logging
from time import sleep

import pyautogui
from pywinauto import mouse

def move_mouse(x1, y1, x2, y2):
    steps = 10
    step_x = (x2 - x1) / steps
    step_y = (y2 - y1) / steps
    for i in range(steps + 1):
        current_x = x1 + step_x * i
        current_y = y1 + step_y * i
        pyautogui.moveTo(current_x, current_y)


def mouse_click(mouse, rect):  #mouse =  mouse_x mouse_y
    current_x, current_y = pyautogui.position()
    # 示例调用
    logging.info(f"鼠标位置: x={current_x}, y={current_y}")
    move_mouse(current_x, current_y, mouse[0] + rect[0], mouse[1] + rect[1])

    pyautogui.click()

    current_x, current_y = pyautogui.position()
    # 示例调用
    logging.info(f"鼠标位置: x={current_x}, y={current_y}")

def mouse_scroll(base, rect):
    current_x, current_y = pyautogui.position()
    move_mouse(current_x, current_y, base[0] + rect[0], base[1] + rect[1])
    current_x, current_y = pyautogui.position()
    sleep(2)
    mouse.scroll(coords=(current_x, current_y), wheel_dist=-2)