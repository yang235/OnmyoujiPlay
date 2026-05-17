import logging
import threading
import time

import cv2
import numpy as np
import win32con
import win32gui
import win32ui

from anasis.utils.compile import compare_with_template_grep as cwg


def _grab_screen(rect):
    """使用 win32 BitBlt 从桌面截取指定区域，返回 BGR numpy 数组"""
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(img_dc, width, height)
    old_bmp = mem_dc.SelectObject(bmp)
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    bmpstr = bmp.GetBitmapBits(True)
    img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((height, width, 4))

    mem_dc.SelectObject(old_bmp)
    win32gui.DeleteObject(bmp.GetHandle())
    mem_dc.DeleteDC()
    img_dc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, desktop_dc)

    return img[:, :, :3]


class VideoStream:
    """后台线程持续捕获窗口画面，主线程阻塞等待模板匹配"""

    def __init__(self, rect, fps=20):
        self.rect = rect
        self.fps = fps
        self._latest_frame = None
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def start(self):
        """启动后台捕获线程"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        logging.info(f"VideoStream 已启动 rect={self.rect} fps={self.fps}")

    def stop(self):
        """停止捕获线程"""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2)
        logging.info("VideoStream 已停止")

    def read(self):
        """返回最新帧的副本，无帧时返回 None"""
        with self._lock:
            if self._latest_frame is None:
                return None
            return self._latest_frame.copy()

    def wait_for_template(self, template_path, threshold=0.7, timeout=10):
        """
        阻塞等待模板匹配成功。
        成功返回 (center_x, center_y)，超时返回 None。
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            frame = self.read()
            if frame is None:
                time.sleep(0.01)
                continue
            match_pos = cwg(frame, template_path, threshold)
            if match_pos is not None:
                logging.info(f"实时匹配成功: {template_path} pos={match_pos}")
                return match_pos
            time.sleep(0.03)
        logging.info(f"实时匹配超时: {template_path} (timeout={timeout}s)")
        return None

    def _capture_loop(self):
        interval = 1.0 / self.fps
        while self._running:
            frame_start = time.time()
            try:
                frame = _grab_screen(self.rect)
                with self._lock:
                    self._latest_frame = frame
            except Exception as e:
                logging.debug(f"抓屏异常: {e}")
            elapsed = time.time() - frame_start
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
