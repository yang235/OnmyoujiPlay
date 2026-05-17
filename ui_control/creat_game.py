import logging
from time import sleep

from anasis.utils.excel_analysis import count_info, part_info, remark_info
from anasis.utils.photo_utils import save_photo_path
from game_actions import register
from game_actions.control_game import dispatch, run_chain
from game_actions.return_game_login import user_avatar, user_center
from ui_control.window_control.video_stream import VideoStream
from ui_control.window_control.win import windows_get


def start_step(count_name, parts, rect):
    stream = VideoStream(rect)
    stream.start()
    sleep(2)
    try:
        ctx = {"rect": rect, "stream": stream, "count_name": count_name, "parts": parts}
        ok = dispatch("load_parts", ctx)
        if ok:
            sleep(5)
            run_chain("daily", ctx)
            sleep(2)
            user_avatar(stream, rect)
            sleep(3)
            user_center(stream, rect)
        return ctx.get("parts", parts), ctx.get("remove_part", "")
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
