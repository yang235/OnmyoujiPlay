import logging
from time import sleep

from anasis.utils.photo_utils import photo_path, activate_photo_path
from game_actions.control_game import register
from ui_control.window_control.keyboard_action import board_press
from ui_control.window_control.mouse_action import mouse_click


@register("temple_activity")
def check_in(ctx):
    return True




