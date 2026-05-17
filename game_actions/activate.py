import logging
from time import sleep

import cv2

from anasis.utils.photo_utils import photo_path, save_photo_path
from anasis.utils.pp_ocr import choose_part, choose_count, choose_user_one_part
from game_actions.control_game import register
from ui_control.window_control.mouse_action import mouse_click


@register("activate")
def activate(ctx):
    """游戏激活：选角→进入游戏→选分区→进入"""
    rect = ctx["rect"]
    stream = ctx["stream"]
    count_name = ctx["count_name"]
    parts = ctx["parts"]

    # OCR: 保存帧供 choose_count 识别
    frame = stream.read()
    if frame is not None:
        cv2.imwrite(save_photo_path("yys.png"), frame)
    match_enter = choose_count(count_name, rect)
    if not match_enter:
        logging.info("未找到进入游戏按钮")
        return False

    sleep(5)
    match_pos = stream.wait_for_template(photo_path("exchange.png"))
    if match_pos is not None:
        mouse_click(match_pos, rect)
    sleep(1)

    # OCR: 保存帧供 choose_part 识别
    frame = stream.read()
    if frame is not None:
        cv2.imwrite(save_photo_path("yys.png"), frame)
    parts, remove_part = choose_part(parts, rect)
    sleep(3)

    enter_match = stream.wait_for_template(photo_path("enter_game2.png"))
    logging.info("点击进入游戏")
    if enter_match is not None:
        mouse_click(enter_match, rect)

    sleep(3)
    more_parts = stream.wait_for_template(photo_path("more_part.png"), 0.8, timeout=3)
    if more_parts is not None:
        frame = stream.read()
        if frame is not None:
            cv2.imwrite(save_photo_path("yys.png"), frame)
        choose_user_one_part(remove_part, enter_match, rect)

    if enter_match is not None:
        sleep(10)
    ctx["parts"] = parts
    ctx["remove_part"] = remove_part
    return True
