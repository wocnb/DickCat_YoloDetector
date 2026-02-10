"""
鼠标控制模块 - 喵帮主人控制鼠标~ 🎀
自动移动鼠标到检测框的指定位置
"""
import pyautogui
from typing import Tuple, Optional, List
from .yolo_detector import DetectionResult
from .logger import default_logger


class MouseController:
    """
    鼠标控制器 (｡♥‿♥｡)
    自动将鼠标移动到检测框的上部指定百分比位置~
    """

    def __init__(
        self,
        target_percent: float = 0.2,
        smoothness: float = 0.3,
        move_speed: int = 20
    ):
        """
        初始化鼠标控制器

        Args:
            target_percent: 目标位置在检测框上部的百分比（0-1）
                          0.2 = 上部20%的中心
                          0.5 = 上半部分的中心
            smoothness: 移动平滑度（0-1），越小越平滑
            move_speed: 每次移动的像素数
        """
        self.target_percent = target_percent
        self.smoothness = smoothness
        self.move_speed = move_speed

        # 当前鼠标位置（用于平滑移动）
        self.current_x, self.current_y = pyautogui.position()

        # 目标位置
        self.target_x = self.current_x
        self.target_y = self.current_y

        # 是否有新的目标
        self.has_target = False

        # 禁用pyautogui的安全检查（允许快速移动）
        pyautogui.FAILSAFE = False

        default_logger.info(f"鼠标控制器初始化完成")
        default_logger.info(f"  - 目标位置: 上部 {target_percent * 100:.0f}%")
        default_logger.info(f"  - 平滑度: {smoothness}")
        default_logger.info(f"  - 移动速度: {move_speed} px/次")

    def update_target(self, detections: List[DetectionResult]):
        """
        更新鼠标目标位置

        Args:
            detections: 检测结果列表
        """
        if not detections:
            # 没有检测到目标，保持当前位置
            self.has_target = False
            return

        # 选择最大的检测框（通常是最重要的目标）
        target_detection = max(
            detections,
            key=lambda d: (d.box[2] - d.box[0]) * (d.box[3] - d.box[1])
        )

        # 计算目标位置
        x1, y1, x2, y2 = target_detection.box

        # 计算检测框的中心X坐标
        center_x = (x1 + x2) // 2

        # 计算检测框上部指定百分比的中心Y坐标
        box_height = y2 - y1
        target_region_height = box_height * self.target_percent
        target_y = int(y1 + target_region_height / 2)

        # 更新目标位置
        self.target_x = center_x
        self.target_y = target_y
        self.has_target = True

    def move(self):
        """
        执行鼠标移动（瞬间移动到目标位置）
        """
        if not self.has_target:
            return

        # 瞬间移动到目标位置
        pyautogui.moveTo(self.target_x, self.target_y, duration=0)
        self.current_x = self.target_x
        self.current_y = self.target_y

    def set_target_percent(self, percent: float):
        """
        设置目标位置百分比

        Args:
            percent: 百分比（0-1）
        """
        self.target_percent = max(0.0, min(1.0, percent))
        default_logger.info(f"鼠标目标位置已更新: 上部 {self.target_percent * 100:.0f}%")

    def enable(self):
        """启用鼠标控制"""
        self.has_target = True
        default_logger.info("鼠标控制已启用")

    def disable(self):
        """禁用鼠标控制"""
        self.has_target = False
        default_logger.info("鼠标控制已禁停")

    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        """
        获取屏幕尺寸

        Returns:
            (width, height)
        """
        return pyautogui.size()
