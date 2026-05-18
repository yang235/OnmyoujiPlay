import logging
from time import sleep

from anasis.utils.photo_utils import photo_path, activate_photo_path
from game_actions.control_game import register
from ui_control.window_control.keyboard_action import board_press
from ui_control.window_control.mouse_action import mouse_click


@register("temple_activity")
def check_in(ctx):
    rect = ctx["rect"]
    stream = ctx["stream"]
    match_pos = stream.wait_for_template(photo_path("right_up.png"), 0.4, timeout=5)
    if match_pos is None:
        logging.info("校验进入游戏未成功,请重试")
        return False
    match_pos = stream.wait_for_template(activate_photo_path("qd.png"), 0.8, timeout=3)
    mouse_click(match_pos,rect)
    match_pos = stream.wait_for_template(activate_photo_path("qd_close.png"), 0.8, timeout=5)
    if match_pos is None:
        match_pos = stream.wait_for_template(photo_path("return.png"), 0.8, timeout=3)
        mouse_click(match_pos, rect)
        return True
    mouse_click(match_pos,rect)
    sleep(2)
    board_press("esc")
    match_pos = stream.wait_for_template(photo_path("return.png"), 0.8, timeout=3)
    mouse_click(match_pos, rect)
    return True




