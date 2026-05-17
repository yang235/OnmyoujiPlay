import logging

import cv2


def compare_with_template_grep(screenshot, template_path, threshold=0.7):
    """将截图与模板图片进行模板匹配"""
    # 直接以灰度图像读取
    template = cv2.imread(template_path ,cv2.IMREAD_GRAYSCALE)

    if template is None:
        logging.info(f"无法读取模板图片: {template_path}")
        return None

    # 将截图转为灰度图
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    logging.info(f"模板匹配相似度: {max_val:.4f}")

    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        logging.info(f"匹配成功! 截图内坐标: ({center_x}, {center_y})")
        return center_x, center_y
    else:
        logging.info(f"未匹配到模板（最高相似度 {max_val:.4f} < 阈值 {threshold}）")
        return None