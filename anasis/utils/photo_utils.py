import os
import sys


def _base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def photo_path(name):
    return os.path.join(_base_dir(), "anasis", "photo", name)

def activate_photo_path(name):
    return os.path.join(_base_dir(), "anasis", "activate_photo", name)


def save_photo_path(name):
    return os.path.join(_base_dir(), "output", name)


def save_ocr_path():
    return os.path.join(_base_dir(), "output")


def save_gou_xie_path(name):
    return os.path.join(_base_dir(), "output", "gouxie", name)