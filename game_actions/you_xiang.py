import logging
from time import sleep

from anasis.utils.photo_utils import photo_path
from game_actions.control_game import register
from ui_control.window_control.keyboard_action import board_press
from ui_control.window_control.mouse_action import mouse_click


@register("you_xiang")
def you_xiang(ctx):
    rect = ctx["rect"]
    stream = ctx["stream"]
    match_pos = stream.wait_for_template(photo_path("right_up.png"), 0.4, timeout=5)
    if match_pos is None:
        logging.info("校验进入游戏未成功,请重试")
        return False
    match_pos = stream.wait_for_template(photo_path("you_xiang.png"), 0.8, timeout=5)
    if match_pos is None:
        logging.info("寻找邮箱未成功,请重试")
        return False
    mouse_click(match_pos, rect)
    match_pos = stream.wait_for_template(photo_path("yx_net_error.png"), 0.8, timeout=2)
    if match_pos is not None:
        logging.info("网络卡顿请等待")
        sleep(10)
    match_pos = stream.wait_for_template(photo_path("yx_lingqu.png"), 0.8, timeout=5)
    if match_pos is None:
        logging.info("当前邮箱不需要领取")
        return True
    mouse_click(match_pos, rect)
    match_pos = stream.wait_for_template(photo_path("yx_queren.png"), 0.8, timeout=5)
    if match_pos is None:
        logging.info("未找到确认奖励,请重试")
        return False
    mouse_click(match_pos, rect)
    match_pos = stream.wait_for_template(photo_path("yx_huode_esc.png"), 0.8, timeout=5)
    if match_pos is None:
        logging.info("获得奖励失败,请重试")
        return False
    board_press("esc")
    board_press("esc")
    return True
