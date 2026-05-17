import logging
from time import sleep

from anasis.utils.photo_utils import photo_path
from game_actions.control_game import register
from ui_control.window_control.keyboard_action import board_press
from ui_control.window_control.mouse_action import mouse_click


@register("check_in")
def check_in(ctx):
    rect = ctx["rect"]
    stream = ctx["stream"]
    match_pos = stream.wait_for_template(photo_path("right_up.png"), 0.4, timeout=5)
    if match_pos is None:
        logging.info("校验进入游戏未成功,请重试")
        return False
    match_pos = stream.wait_for_template(photo_path("deng_lu.png"), 0.8, timeout=3)
    if match_pos is None:
        logging.info("签到任务已完成")
        return True
    mouse_click(match_pos, rect)
    match_pos = stream.wait_for_template(photo_path("qd_wan.png"), 0.8, timeout=5)
    mouse_click(match_pos, rect)
    match_pos = stream.wait_for_template(photo_path("qd_no_task.png"), 0.8, timeout=1)
    if match_pos is not None:
        match_pos = stream.wait_for_template(photo_path("return.png"), 0.8, timeout=5)
        mouse_click(match_pos, rect)
        return True
    match_pos = stream.wait_for_template(photo_path("qian_dao_close_esc.png"), 0.8, timeout=5)
    sleep(4)
    board_press("esc")
    match_pos = stream.wait_for_template(photo_path("qd_success.png"), 0.8, timeout=5)
    match_pos = stream.wait_for_template(photo_path("qd_moyu_close.png"), 0.8, timeout=5)
    mouse_click(match_pos, rect)
    match_pos = stream.wait_for_template(photo_path("return.png"), 0.8, timeout=5)
    mouse_click(match_pos, rect)
    return True