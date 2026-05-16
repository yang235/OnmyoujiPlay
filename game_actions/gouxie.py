from datetime import datetime
from time import sleep

import cv2

from anasis.utils.compile import compare_with_template_grep as cwg
from anasis.utils.photo_utils import photo_path, save_gou_xie_path
from game_actions.control_game import register
from ui_control.window_control.mouse_action import mouse_click
from ui_control.window_control.win import capture_window


def find_xie_zuo(rect):
    screenshot = capture_window(rect)
    match_pos = cwg(screenshot, photo_path("right_up.png"), 0.4)
    if match_pos is None:
        return False
    print("已识别到进入游戏，开始匹配悬赏...")
    match_pos = cwg(screenshot, photo_path("fengyin.png"))
    if match_pos is None:
        match_pos = cwg(screenshot, photo_path("fengyin2.png"))
    if match_pos is None:
        print("匹配悬赏失败")
        return False
    mouse_click(match_pos, rect)
    sleep(2)
    screenshot = capture_window(rect)
    print("正在寻找勾协...")
    match_pos = cwg(screenshot, photo_path("error_gouxie.png"), 0.9)
    if match_pos is not None:
        return False
    match_pos = cwg(screenshot, photo_path("gouxie.png"), 0.7)
    if match_pos is not None :
        current_time = datetime.now().strftime("%m%d%H%M%S")
        cv2.imwrite(save_gou_xie_path(f"gx_{current_time}.png").encode("utf-8").decode("utf-8"), screenshot)
        print("勾协已截图: 存放在output/gouxie下")
    match_pos = cwg(screenshot, photo_path("gouxie_close.png"), 0.6)
    mouse_click(match_pos, rect)
    return True

@register("gou_xie")
def gou_xie(rect):
    """勾协主流程"""
    is_bool = find_xie_zuo(rect)
    if not is_bool:
        print("封印悬赏步骤未成功，请重试")