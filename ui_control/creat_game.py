import logging
from time import sleep

from anasis.utils.compile import compare_with_template_grep as cwg
from anasis.utils.excel_analysis import count_info, part_info, remark_info
from anasis.utils.photo_utils import photo_path
from anasis.utils.pp_ocr import choose_part, choose_count, choose_user_one_part
from game_actions import register
from game_actions.gouxie import gou_xie
from game_actions.return_game_login import user_avatar, user_center
from ui_control.window_control.mouse_action import mouse_click
from ui_control.window_control.video_stream import VideoStream
from ui_control.window_control.win import windows_get, capture_window


def start_step(count_name, parts, rect):
    # 截图窗口内容
    sleep(2)
    capture_window(rect)
    match_enter = choose_count(count_name, rect)
    if match_enter:
        # 进入游戏后重新截屏
        sleep(5)
        screenshot = capture_window(rect)
        exchange = cwg(screenshot, photo_path("exchange.png"))
        mouse_click(exchange, rect)
        sleep(1)
        capture_window(rect)
        # 选择分区
        parts, remove_part = choose_part(parts, rect)
        sleep(3)
        screenshot = capture_window(rect)
        # 分区进去游戏
        exchange = cwg(screenshot, photo_path("enter_game2.png"))
        logging.info("点击进入游戏")
        mouse_click(exchange, rect)
        # 判断是否多分区登录
        screenshot = capture_window(rect)
        more_parts = cwg(screenshot, photo_path("more_part.png"))
        if more_parts is not None:
            choose_user_one_part(remove_part,exchange,rect)
        if exchange is not None:
            sleep(10)
            # ToDO 增加广告关闭

            # TODO 勾协与神秘商人可接入
            gou_xie(rect)
            sleep(2)
            stream = VideoStream(rect)
            stream.start()
            try:
                user_avatar(stream, rect)
                sleep(3)
                user_center(stream, rect)
            finally:
                stream.stop()
        return parts, remove_part
    else:
        logging.info("未找到进入游戏按钮")

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
