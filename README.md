# OnmyoujiPlay — 阴阳师多小号自动化

基于 OpenCV 实时视频流 + OCR 的《阴阳师》游戏自动化工具，通过 tkinter UI 启动登录流程、执行多小号日常翻勾协任务。(仅支持mumu桌面版本，旧版本桌面修改/ui_control/window_control/win.py中的名称)

## 功能特性

- **实时视频流监控** — 通过 win32 BitBlt 高速截取游戏窗口，使用 OpenCV 模板匹配实时识别游戏界面元素
- **OCR 文字识别** — 基于 PaddleOCR 识别游戏内账号名、分区名等文字信息
- **可配置动作链** — JSON 配置文件编排日常任务链，目前包含勾协、邮箱领取、签到
- **多账号批量管理** — tkinter UI 展示账号列表、分区状态，支持批量登录
- **Excel 进度记录** — 自动标记已完成的分区
- **绿色便携打包** — 内嵌 Python 运行时 + 全部依赖，解压即用
- 夸克网盘:「OnmyoujiPlay_portable.zip」链接:https://pan.quark.cn/s/0bbcee715c67 提取码：ukjp
- 下载源码与夸克中的runtime依赖，解压至目录文件onmyoujiPlay下既可以免下载环境直接运行
## 项目结构

```
OnmyoujiPlay/
├── main.py                     # 项目入口，加载模块并启动登录流程
├── start.bat                   # 便携包启动脚本
├── game_actions/               # 动作模块（可链式调用）
│   ├── __init__.py             # 导出 register / dispatch / load / run_chain
│   ├── control_game.py         # 动作注册、链式调度核心
│   ├── game_actions.json       # 动作链配置 {"chains": {"daily": ["gou_xie", "you_xiang", "check_in"]}}
│   ├── load_parts.py           # 进入游戏：选号→选分区→进入
│   ├── gou_xie.py              # 勾协：匹配封印→寻找勾协→截图
│   ├── you_xiang.py            # 邮箱：识别邮箱→领取→确认
│   └── return_game_login.py    # 返回主界面工具函数
├── ui_control/                 # UI 与窗口控制
│   ├── ui/
│   │   └── tk.py               # tkinter UI 主界面（账号列表、视频流、日志）
│   ├── creat_game.py           # 登录流程编排（串联动作链）
│   └── window_control/
│       ├── video_stream.py     # 视频流核心（BitBlt 截图 + 模板匹配）
│       ├── win.py              # 游戏窗口查找 / 创建视频流
│       ├── mouse_action.py     # 鼠标操作封装
│       └── keyboard_action.py  # 键盘操作封装
├── anasis/                     # 分析工具与模板
│   ├── utils/
│   │   ├── pp_ocr.py           # PaddleOCR 封装（选号/选分区）
│   │   ├── photo_utils.py      # 模板图片路径 + 截图保存
│   │   ├── excel_analysis.py   # Excel 账号/分区/标记 读写
│   │   └── compile.py          # 编译工具
│   ├── photo/                  # 模板图片（*.png）
│   └── count_info.xlsx         # 账号信息表
├── output/                     # 运行输出（截图、日志）
├── dist/                       # 便携包输出目录
├── runtime/                    # 便携包内嵌 Python 运行时
└── 打包说明.txt                 # 打包流程文档
```

## 运行要求

| 组件 | 说明 |
|------|------|
| Python | 3.8 |
| OpenCV | cv2 (含模板匹配) |
| PaddleOCR | 文字识别 |
| pywin32 | win32gui / win32ui 窗口截取 |
| pywinauto | 窗口操作 |
| PIL / Pillow | 图像处理 (tkinter 显示) |
| tkinter | UI 界面 (Tcl/Tk 8.6) |

## 快速开始

### 便携包（推荐）

1. 确保整个 `OnmyoujiPlay_portable` 目录完整（含 `runtime/`）
2. 账号存储在anasis文件下 excel中 目前支持多账号和多个分区（一区多角色，需要全部列出，容错较低填写账号需要仔细）
3. 右击 `start.bat` 管理员身份启动
4. 在弹出的 UI界面中点击「启动登录」可以完成未登录的所有账号，每次启动前需要等待ocr插件加载，需要手动重置所有标记

### 源码运行

```bash
# 安装依赖（在 conda 环境中）
pip install opencv-python paddleocr pywin32 pywinauto pillow

# 启动 UI
python ui_control/ui/tk.py
```

## 动作链配置

编辑 `game_actions/game_actions.json` 即可自定义任务链：

```json
{
    "chains": {
        "daily": ["gou_xie", "you_xiang", "check_in"]
    }
}
```

- 链中每个动作需用 `@register("name")` 注册
- 动作函数签名为 `def action(ctx) -> bool`，`ctx` 包含 `rect`（窗口位置）、`stream`（视频流）等
- 返回 `False` 将中断后续动作

## UI 说明

```
┌─────────────────────┬────────────────────────────────┐
│ 账号列表             │  实时画面                       │
│  [账号A] [账号B]    │  (游戏窗口视频流, ~10fps)       │
│                     │                                │
│ 分区                ├────────────────────────────────┤
│  [未登录] 区1       │  操作日志                       │
│  [已登录] 区2       │  > 已识别到进入游戏             │
│                     │  > 正在寻找勾协...              │
│ [标记已完成]        │                                │
│ [启动登录] [停止]    │                                │
└─────────────────────┴────────────────────────────────┘
```

- **左侧**：账号选择、分区列表、操作按钮
- **右侧上方**：游戏窗口实时视频流
- **右侧下方**：操作日志（实时输出）

## 打包分发

打包流程详见 [打包说明.txt](./打包说明.txt)。

核心思路：复制 conda 环境中的 Python 运行时 + 全部依赖到 `runtime/` 目录，通过 `start.bat` 设置环境变量（PYTHONHOME / PYTHONPATH / TCL_LIBRARY 等）后直接运行源码。

## License

MIT
