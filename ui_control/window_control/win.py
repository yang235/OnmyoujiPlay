from time import sleep

import cv2
import numpy as np
import pyautogui
import win32gui

from anasis.utils.photo_utils import save_photo_path


def windows_get():
    """获取阴阳师窗口句柄和位置"""
    window = win32gui.FindWindow(None, '阴阳师-MuMu模拟器专版')

    print(f"窗口句柄: {window}")
    rect = win32gui.GetWindowRect(window)
    if window == 0 or window is None:
        return None
    win32gui.MoveWindow(window, rect[0], rect[1], 844, 510, True)

    rect = win32gui.GetWindowRect(window)
    print(f"窗口位置: {rect}")
    return window, rect



def capture_window(rect):
    """截取窗口区域"""
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    sleep(2)
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(save_photo_path("yys.png"))

    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)