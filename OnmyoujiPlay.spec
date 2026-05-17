# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui_control\\ui\\tk.py'],
    pathex=[],
    binaries=[],
    datas=[('anasis/photo', 'anasis/photo'), ('anasis/count_info.xlsx', 'anasis'), ('game_actions/game_actions.json', 'game_actions')],
    hiddenimports=['game_actions.gouxie', 'game_actions.load_parts', 'game_actions.return_game_login', 'game_actions.control_game', 'ui_control.creat_game', 'anasis.utils.compile', 'anasis.utils.pp_ocr', 'anasis.utils.photo_utils', 'anasis.utils.excel_analysis', 'paddleocr', 'paddle', 'cv2', 'PIL', 'PIL.ImageTk', 'win32gui', 'win32ui', 'win32con', 'pywinauto', 'pyautogui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OnmyoujiPlay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OnmyoujiPlay',
)
