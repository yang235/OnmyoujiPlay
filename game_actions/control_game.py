"""
游戏动作调度模块
只定义动作注册与调度机制，不包含任何具体游戏行为。
"""

from __future__ import annotations

import importlib
from typing import Any, Callable

_registry: dict[str, Callable] = {}


def register(name: str):
    """装饰器：将函数注册为可调度的游戏动作"""
    def decorator(func: Callable):
        _registry[name] = func
        return func
    return decorator


def dispatch(name: str, *args, **kwargs) -> Any:
    """按动作名调度执行。未注册时自动尝试加载 gouxie 模块。"""
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


