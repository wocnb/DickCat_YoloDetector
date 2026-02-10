"""
屏幕捕获模块
负责捕获电脑屏幕画面
"""
import numpy as np
import cv2
import mss
from typing import Optional, Tuple
import threading
from .logger import default_logger


class ScreenCapture:
    """
    屏幕捕获类
    职责：负责从屏幕捕获画面并转换为可用格式
    """

    def __init__(self, monitor: Optional[dict] = None):
        """
        初始化屏幕捕获器

        Args:
            monitor: 监控区域配置，None则使用主显示器
                    格式: {"top": 0, "left": 0, "width": 1920, "height": 1080}
        """
        self.sct = mss.mss()
        self.monitor = monitor or self.sct.monitors[1]  # 1是主显示器，0是所有显示器
        self._lock = threading.Lock()
        self._frame = None

        width, height = self.get_monitor_size()
        default_logger.info(f"屏幕捕获初始化: 区域大小 {width}x{height}")
        default_logger.debug(f"监控区域: {self.monitor}")

    def capture(self) -> np.ndarray:
        """
        捕获当前屏幕画面

        Returns:
            numpy数组格式的屏幕画面 (BGR格式)
        """
        with self._lock:
            screenshot = self.sct.grab(self.monitor)
            # mss返回的是BGRA格式，需要转换为BGR
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame

    def get_monitor_size(self) -> Tuple[int, int]:
        """
        获取当前监控区域的尺寸

        Returns:
            (width, height) 元组
        """
        return self.monitor["width"], self.monitor["height"]

    def set_monitor_region(self, top: int, left: int, width: int, height: int):
        """
        设置屏幕捕获区域

        Args:
            top: 距离顶部像素
            left: 距离左侧像素
            width: 宽度
            height: 高度
        """
        self.monitor = {"top": top, "left": left, "width": width, "height": height}
        default_logger.info(f"监控区域已更新: {width}x{height} at ({left},{top})")
