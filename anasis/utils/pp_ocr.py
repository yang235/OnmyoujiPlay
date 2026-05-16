import json
from time import sleep
from typing import List

from paddleocr import PaddleOCR
from sympy.external.gmpy import remove

from anasis.utils.photo_utils import save_photo_path, save_ocr_path
from ui_control.window_control.mouse_action import mouse_click, mouse_scroll
from ui_control.window_control.win import capture_window

pipeline = PaddleOCR(
    use_doc_orientation_classify=False, # 通过 use_doc_orientation_classify 参数指定不使用文档方向分类模型
    use_doc_unwarping=False, # 通过 use_doc_unwarping 参数指定不使用文本图像矫正模型
    use_textline_orientation=False,
    device="gpu",)

def center(box):
    if box is not None:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

def parse_ocr_result(result_json_path: str) -> List[dict]:
    with open(result_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    dt_polys = data.get("dt_polys", [])
    rec_texts = data.get("rec_texts", [])
    rec_scores = data.get("rec_scores", [])

    results = []
    for i in range(len(dt_polys)):
        results.append({
            "center": center(dt_polys[i]),
            "text": rec_texts[i] if i < len(rec_texts) else "",
            "score": rec_scores[i] if i < len(rec_scores) else 0.0,
        })
    return results


def screen():
    output = pipeline.predict(input=save_photo_path("yys.png"))
    output[0].save_to_img(save_ocr_path())
    output[0].save_to_json(save_ocr_path())
    result_list = parse_ocr_result(save_photo_path("yys_res.json"))
    items = []
    for item in result_list:
        if (float(item.get("score")) > 0.8):
            dict_item = {
                "text": item.get("text"),
                "score": round(item.get("score"), 3),
                "center": item.get("center"),
            }
            items.append(dict_item)
    return items

# 选择分区
def choose_part(parts, rect):
    is_find = False
    remove_part = ""
    while not is_find:
        items = screen()
        base = ()
        fot = ()
        for item in items:
            if item["text"] == "选择区域":
                base = item["center"]
            if item["text"] == "抢先体验":
                fot = item["center"]
            if item["text"] in parts:
                mouse_click(item["center"], rect)
                print(item["text"])
                remove_part = item["text"]
                parts.remove(item["text"])
                is_find = True
                break
        if not is_find:
            end = (base[0], fot[1])
            mouse_scroll(end, rect)
            capture_window(rect)
    return parts ,remove_part

def find_count(count_name, rect, enter_count):
    capture_window(rect)
    items = screen()
    for item in items:
        if item["text"] == count_name:
            print(item["text"], item["center"])
            mouse_click(item["center"], rect)
            sleep(2)
            print("已识别到登录界面，开始匹配进入游戏按钮...")
            mouse_click(enter_count, rect)
            return True
    return False

def choose_count(count_name, rect):
    items = screen()
    is_count = False
    enter_count = ()
    base_count = ()
    for item in items:
        if item["text"] == count_name:
            is_count = True
        if item["text"] == "进入游戏":
            enter_count = item["center"]
            print(item["text"], enter_count)
        if item["text"] == "网易游戏":
            base_count = item["center"]
            print(item["text"], base_count)
    end_count = (enter_count[0], (enter_count[1] + base_count[1])/2)
    if is_count:
        print("已识别到登录界面，开始匹配进入游戏按钮...")
        mouse_click(enter_count, rect)
        return True
    else:
        mouse_click(end_count, rect)
        return find_count(count_name, rect, enter_count)


def choose_user_one_part(part, enter_count,rect):
    items = screen()
    for item in items:
        if item["text"] == part:
            mouse_click(item["center"], rect)
            sleep(2)
            mouse_click(enter_count, rect)