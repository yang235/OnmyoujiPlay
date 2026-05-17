import logging
from datetime import datetime
from time import sleep

import cv2

from anasis.utils.photo_utils import photo_path, save_gou_xie_path
from game_actions.control_game import register
from ui_control.window_control.mouse_action import mouse_click


@register("gou_xie")
def gou_xie(ctx):
    """勾协主流程"""
    rect = ctx["rect"]
    stream = ctx["stream"]

    match_pos = stream.wait_for_template(photo_path("right_up.png"), 0.4, timeout=5)
    if match_pos is None:
        logging.info("封印悬赏步骤未成功，请重试")
        return False
    logging.info("已识别到进入游戏，开始匹配悬赏...")
    match_pos = stream.wait_for_template(photo_path("fengyin.png"), timeout=5)
    if match_pos is None:
        match_pos = stream.wait_for_template(photo_path("fengyin2.png"), timeout=3)
    if match_pos is None:
        logging.info("匹配悬赏失败")
        return False
    mouse_click(match_pos, rect)
    sleep(2)
    logging.info("正在寻找勾协...")
    match_pos = stream.wait_for_template(photo_path("error_gouxie.png"), 0.9, timeout=3)
    if match_pos is not None:
        logging.info("协作未加载完成")
        return False
    match_pos = stream.wait_for_template(photo_path("gouxie.png"), 0.7, timeout=3)
    if match_pos is not None:
        frame = stream.read()
        if frame is not None:
            current_time = datetime.now().strftime("%m%d%H%M%S")
            cv2.imwrite(save_gou_xie_path(f"gx_{current_time}.png").encode("utf-8").decode("utf-8"), frame)
            logging.info("勾协已截图: 存放在output/gouxie下")
    match_pos = stream.wait_for_template(photo_path("gouxie_close.png"), 0.6, timeout=3)
    if match_pos is not None:
        mouse_click(match_pos, rect)
        logging.info("已经回到庭院")
    return True
