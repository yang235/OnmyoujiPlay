from time import sleep

from anasis.utils.compile import compare_with_template_grep as cwg
from anasis.utils.photo_utils import photo_path
from ui_control.window_control.mouse_action import mouse_click


def return_home(screenshot, rect):
    point = cwg(screenshot, photo_path("return.png"))
    mouse_click(point, rect)
    sleep(3)

def user_avatar(screenshot, rect):
    print("尝试点击头像进行返回")
    point = cwg(screenshot, photo_path("user_avatar.png"))
    mouse_click(point, rect)

def user_center(screenshot, rect):
    print("尝试点击用户中心进行返回")
    point = cwg(screenshot, photo_path("user_center.png"))
    mouse_click(point, rect)