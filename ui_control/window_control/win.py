import logging
from time import sleep

import cv2
import numpy as np
import pyautogui
import win32gui

from anasis.utils.photo_utils import save_photo_path


def windows_get():
    """获取阴阳师窗口句柄和位置"""
    window = win32gui.FindWindow(None, '阴阳师-MuMu模拟器专版')

    logging.info(f"窗口句柄: {window}")
    rect = win32gui.GetWindowRect(window)
    if window == 0 or window is None:
        return None
    win32gui.MoveWindow(window, rect[0], rect[1], 844, 510, True)

    rect = win32gui.GetWindowRect(window)
    logging.info(f"窗口位置: {rect}")
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


def create_stream(rect=None):
    """创建并启动一个 VideoStream。不传 rect 则自动查找游戏窗口"""
    from ui_control.window_control.video_stream import VideoStream

    if rect is None:
        result = windows_get()
        if result is None:
            raise RuntimeError("未找到游戏窗口")
        _, rect = result
    stream = VideoStream(rect)
    stream.start()
    return stream

