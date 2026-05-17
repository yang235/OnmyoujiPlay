import logging
from time import sleep

import cv2

from anasis.utils.excel_analysis import count_info, part_info, remark_info
from anasis.utils.photo_utils import photo_path, save_photo_path
from anasis.utils.pp_ocr import choose_part, choose_count, choose_user_one_part
from game_actions import register
from game_actions.gouxie import gou_xie
from game_actions.return_game_login import user_avatar, user_center
from ui_control.window_control.mouse_action import mouse_click
from ui_control.window_control.video_stream import VideoStream
from ui_control.window_control.win import windows_get


def start_step(count_name, parts, rect):
    stream = VideoStream(rect)
    stream.start()
    sleep(2)
    try:
        # OCR: 保存帧供 choose_count 识别
        frame = stream.read()
        if frame is not None:
            cv2.imwrite(save_photo_path("yys.png"), frame)
        match_enter = choose_count(count_name, rect)
        if match_enter:
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
            # 判断是否多分区登录
            more_parts = stream.wait_for_template(photo_path("more_part.png"))
            if more_parts is not None:
                choose_user_one_part(remove_part, enter_match, rect)
            if enter_match is not None:
                sleep(10)
                # ToDO 增加广告关闭

                # TODO 勾协与神秘商人可接入
                gou_xie(rect)
                sleep(2)
                user_avatar(stream, rect)
                sleep(3)
                user_center(stream, rect)
            return parts, remove_part
        else:
            logging.info("未找到进入游戏按钮")
    finally:
        stream.stop()

@register("login")
def login():
    count_names = count_info()
    parts = part_info(count_names)
    result = windows_get()
    if result is None:
        logging.info("未找到游戏窗口,请启动游戏")
        exit()
    _, rect = result
    logging.info("请勿移动窗口")
    for count_name in count_names:
        logging.info(count_name)
        parts = part_info(count_name)
        while parts is not None and len(parts) > 0:
            parts,_ = start_step(count_name, parts, rect)
            remark_info(count_name, parts)
