"""项目启动入口"""

from game_actions import load, dispatch, list_actions


def main():
    load("ui_control.creat_game")
    print("已注册动作:", list_actions())
    dispatch("login")


if __name__ == "__main__":
    main()
