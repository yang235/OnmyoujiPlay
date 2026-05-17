"""
游戏动作调度模块
只定义动作注册与调度机制，不包含任何具体游戏行为。
"""

from __future__ import annotations

import importlib
import json
import logging
import os
from typing import Any, Callable

_registry: dict[str, Callable] = {}

_chain_config: dict = {}
_config_loaded = False


def register(name: str):
    """装饰器：将函数注册为可调度的游戏动作"""
    def decorator(func: Callable):
        _registry[name] = func
        return func
    return decorator


def dispatch(name: str, *args, **kwargs) -> Any:
    """按动作名调度执行"""
    action = _registry.get(name)
    if action is None:
        raise KeyError(f"未注册的动作: {name}")
    return action(*args, **kwargs)


def list_actions() -> list[str]:
    """列出所有已注册的动作名"""
    return list(_registry.keys())


def load(module_name: str):
    """动态加载动作模块，触发 @register 装饰器执行注册"""
    importlib.import_module(module_name)


def load_chain_config():
    """加载动作链配置"""
    global _chain_config, _config_loaded
    if _config_loaded:
        return
    config_path = os.path.join(os.path.dirname(__file__), "game_actions.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            _chain_config = json.load(f)
        _config_loaded = True
        logging.info(f"已加载动作链配置: {list(_chain_config.get('chains', {}).keys())}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.warning(f"加载动作链配置失败: {e}")
        _chain_config = {}
        _config_loaded = True


def run_chain(name: str, ctx: dict) -> bool:
    """
    执行动作链。从配置中读取动作列表，按序执行。
    任一动作返回 False 则中断链，返回 False。
    全部成功返回 True。
    """
    load_chain_config()
    action_names = _chain_config.get("chains", {}).get(name, [])
    if not action_names:
        logging.warning(f"动作链 '{name}' 未配置或为空")
        return True
    logging.info(f"执行动作链 '{name}': {action_names}")
    for action_name in action_names:
        action = _registry.get(action_name)
        if action is None:
            logging.error(f"未注册的动作: {action_name}")
            return False
        logging.info(f"  -> {action_name}")
        result = action(ctx)
        if not result:
            logging.info(f"动作 {action_name} 返回失败，链中断")
            return False
    logging.info(f"动作链 '{name}' 执行完成")
    return True


