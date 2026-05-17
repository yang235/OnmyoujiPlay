"""项目启动入口"""

import logging

from game_actions import load, dispatch, list_actions


def main():
    load("game_actions.load_parts")
    load("game_actions.gou_xie")
    load("game_actions.you_xiang")
    load("game_actions.check_in")
    load("ui_control.creat_game")
    logging.info("已注册动作:", list_actions())
    dispatch("login")


if __name__ == "__main__":
    main()
