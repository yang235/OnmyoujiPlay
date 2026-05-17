import logging
from time import sleep

from anasis.utils.photo_utils import photo_path
from ui_control.window_control.mouse_action import mouse_click


def return_home(stream, rect):
    point = stream.wait_for_template(photo_path("return.png"), timeout=5)
    if point is not None:
        mouse_click(point, rect)
    sleep(3)

def user_avatar(stream, rect):
    logging.info("尝试点击头像进行返回")
    point = stream.wait_for_template(photo_path("user_avatar.png"), timeout=5)
    if point is not None:
        mouse_click(point, rect)

def user_center(stream, rect):
    logging.info("尝试点击用户中心进行返回")
    point = stream.wait_for_template(photo_path("user_center.png"), timeout=5)
    if point is not None:
        mouse_click(point, rect)
