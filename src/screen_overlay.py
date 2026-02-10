"""
透明覆盖窗口模块 - 在屏幕上直接绘制检测框 🎀
使用PyQt5创建透明覆盖层
"""
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
import sys
from typing import List, Tuple
from .yolo_detector import DetectionResult
import numpy as np


class TransparentOverlay(QWidget):
    """
    透明覆盖窗口类 (｡♥‿♥｡)
    在屏幕上直接绘制检测框，温柔地为主人服务~
    """

    def __init__(self, detections: List[DetectionResult] = None):
        super().__init__()

        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 始终置顶
            Qt.Tool  # 工具窗口，不显示在任务栏
        )

        # 设置透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # 设置全屏
        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        self.setGeometry(geometry)

        # 存储检测结果
        self.detections = detections or []

        # 设置鼠标穿透（让鼠标事件穿透窗口）
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 颜色配置（喵的粉色系~）
        self.box_colors = [
            QColor(255, 105, 180),  # 粉色
            QColor(255, 182, 193),  # 浅粉色
            QColor(255, 192, 203),  # 玫粉色
            QColor(219, 112, 147),  # 苍紫罗兰
        ]
        self.text_color = QColor(255, 255, 255)  # 白色文字

        # 默认字体
        self.label_font = QFont("Arial", 12, QFont.Bold)

    def update_detections(self, detections: List[DetectionResult]):
        """
        更新检测结果 (｡♥‿♥｡)

        Args:
            detections: 新的检测结果列表
        """
        self.detections = detections
        self.update()  # 触发重绘

    def paintEvent(self, event):
        """
        绘制事件 - 喵为主人绘制检测框~
        """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)  # 抗锯齿

        # 绘制每个检测框
        for i, detection in enumerate(self.detections):
            self._draw_detection(painter, detection, i)

    def _draw_detection(self, painter: QPainter, detection: DetectionResult, index: int):
        """
        绘制单个检测结果 (｡♥‿♥｡)

        Args:
            painter: QPainter对象
            detection: 检测结果
            index: 索引（用于选择颜色）
        """
        x1, y1, x2, y2 = detection.box

        # 选择颜色（循环使用粉色系）
        color = self.box_colors[index % len(self.box_colors)]

        # 绘制边框（喵用温柔的线条~）
        pen = QPen(color, 3)  # 3像素宽的边框
        painter.setPen(pen)
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)

        # 准备标签文本
        label_parts = []
        if detection.class_name:
            label_parts.append(detection.class_name)
        if detection.confidence:
            label_parts.append(f"{detection.confidence:.2f}")

        label = " ".join(label_parts)

        if label:
            # 计算标签背景大小
            painter.setFont(self.label_font)
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(label)
            text_height = metrics.height()

            # 绘制标签背景（半透明的粉色~）
            bg_color = QColor(color)
            bg_color.setAlpha(200)  # 半透明
            painter.setBrush(bg_color)
            painter.setPen(Qt.NoPen)

            label_y = max(y1, text_height + 5)
            painter.drawRoundedRect(
                x1, label_y - text_height - 5,
                text_width + 10, text_height + 5,
                5, 5  # 圆角半径
            )

            # 绘制标签文本
            painter.setPen(self.text_color)
            painter.drawText(x1 + 5, label_y - 5, label)


def create_overlay_app():
    """创建Qt应用程序（如果不存在）"""
    if not QApplication.instance():
        return QApplication(sys.argv)
    return QApplication.instance()
