import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image

# --------------------------
# 1. 读取图片并识别账号信息
# --------------------------
def get_account_info(image_path):
    # 读取图片
    img = cv2.imread(image_path)
    print(img.shape)
    if img is None:
        print("无法读取图片")
        return None

    # 截取账号输入框区域（根据图中位置估算坐标，可根据实际情况调整）
    # 这里的坐标是大致范围，你可以根据实际截图微调
    account_roi = img[260:350, 100:300]  # y1:y2, x1:x2

    # 转灰度并做简单预处理
    gray = cv2.cvtColor(account_roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # 使用OCR识别文本
    text = pytesseract.image_to_string(binary, lang='eng', config='--psm 7')
    text = text.strip()  # 去除多余空格和换行
    print(f"识别到的账号信息：{text}")
    return text

# --------------------------
# 2. 定位并点击“进入游戏”按钮
# --------------------------
def click_enter_game_button(template_path, screenshot_path=None):
    # 截取当前屏幕（如果不提供截图路径，就截取全屏）
    if screenshot_path is None:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    else:
        screenshot = cv2.imread(screenshot_path)

    # 读取按钮模板（可以提前截取“进入游戏”按钮的小图保存为template.png）
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    # 模板匹配
    gray_screen = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    # 找到匹配的位置并点击
    for pt in zip(*loc[::-1]):
        # 计算按钮中心坐标
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        print(f"找到按钮，点击位置：({center_x}, {center_y})")
        pyautogui.click(center_x, center_y)
        break

# --------------------------
# 主函数
# --------------------------
if __name__ == "__main__":
    # 替换为你的图片路径
    image_path = "photo/game_login.png"  # 你的截图
    template_path = "photo/enter_game.png"  # 提前截取的“进入游戏”按钮小图

    # 步骤1：识别账号信息
    account = get_account_info(image_path)

    # 步骤2：点击进入游戏按钮
    # 这里用截图模拟，实际运行时可以去掉screenshot_path参数直接用当前屏幕
    # click_enter_game_button(template_path, screenshot_path=image_path)