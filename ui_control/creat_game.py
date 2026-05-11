import os
import subprocess
from time import sleep


import numpy as np
import pyautogui
import win32gui


def run_play():
    exe_path = r"D:\阴阳师\Launch.exe"
    subprocess.Popen(exe_path)


def windows_get():
    """获取阴阳师窗口句柄和位置"""
    window = win32gui.FindWindow(None, '阴阳师-MuMu模拟器专版')

    print(f"窗口句柄: {window}")

    if window == 0 or window is None:
        return None

    rect = win32gui.GetWindowRect(window)
    print(f"窗口位置: {rect}")

    return window, rect


def capture_window(rect):
    """截取窗口区域"""
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save('full.png')
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def compare_with_template(screenshot, template_path, threshold=0.8):
    """将截图与模板图片进行模板匹配"""
    template = cv2.imread(template_path)
    if template is None:
        print(f"无法读取模板图片: {template_path}")
        return None

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"模板匹配相似度: {max_val:.4f}")

    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        print(f"匹配成功! 截图内坐标: ({center_x}, {center_y})")
        return center_x, center_y
    else:
        print(f"未匹配到模板（最高相似度 {max_val:.4f} < 阈值 {threshold}）")
        return None


def mouse_click():
    current_x, current_y = pyautogui.position()
    print(f"鼠标位置: x={current_x}, y={current_y}")


if __name__ == '__main__':
    result = windows_get()
    if result is None:
        print("未找到游戏窗口，尝试启动游戏...")
        run_play()
        sleep(10)
        result = windows_get()
        if result is None:
            print("启动失败，退出")
            exit()

    window, rect = result

    # 截图窗口内容
    screenshot = capture_window(rect)
    print(f"截图尺寸: {screenshot.shape}")

    # 与 anasis/photo/game_login.png 做对比
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'anasis', 'photo', 'game_login.png'
    )
    match_pos = compare_with_template(screenshot, template_path)

    if match_pos:
        print(f"已识别到登录界面，按钮位置: {match_pos}")

    mouse_click()