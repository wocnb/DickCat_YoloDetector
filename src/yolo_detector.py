"""
YOLO目标检测模块
负责使用YOLO模型进行目标检测
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from .logger import default_logger


@dataclass
class DetectionResult:
    """检测结果数据类"""
    box: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    confidence: float
    class_id: int
    class_name: str


class YOLODetector:
    """
    YOLO检测器类
    职责：加载YOLO模型并执行目标检测
    """

    # 默认的类别颜色
    DEFAULT_COLORS = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 165, 0),
        (255, 192, 203), (0, 128, 0)
    ]

    def __init__(
        self,
        model_path: str = "yolo26n.pt",
        confidence_threshold: float = 0.5,
        iou_threshold: float = 0.45,
        classes: Optional[List[str]] = None
    ):
        """
        初始化YOLO检测器

        Args:
            model_path: 模型文件路径，默认使用yolo26n（Nano版本，速度快）
            confidence_threshold: 置信度阈值
            iou_threshold: IOU阈值，用于非极大值抑制
            classes: 要检测的类别列表，None表示检测所有类别
        """
        default_logger.info(f"正在加载YOLO模型: {model_path}")
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.classes = classes

        # 记录模型信息
        class_info = "所有类别" if classes is None else f"类别: {classes}"
        default_logger.info(f"YOLO检测器初始化完成")
        default_logger.info(f"  - 置信度阈值: {confidence_threshold}")
        default_logger.info(f"  - IOU阈值: {iou_threshold}")
        default_logger.info(f"  - 检测范围: {class_info}")

    def detect(self, frame: np.ndarray) -> List[DetectionResult]:
        """
        对图像帧执行目标检测

        Args:
            frame: 输入图像 (BGR格式)

        Returns:
            DetectionResult对象列表
        """
        results = self.model(
            frame,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            classes=self.classes,
            verbose=False
        )

        detections = []
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)

            for box, conf, cls_id in zip(boxes, confidences, class_ids):
                class_name = self.model.names.get(cls_id, f"class_{cls_id}")
                detections.append(DetectionResult(
                    box=tuple(map(int, box)),
                    confidence=float(conf),
                    class_id=int(cls_id),
                    class_name=class_name
                ))

            # 记录检测摘要（debug级别，避免刷屏）
            if detections:
                detection_summary = {}
                for d in detections:
                    detection_summary[d.class_name] = detection_summary.get(d.class_name, 0) + 1
                default_logger.debug(f"检测到 {len(detections)} 个物体: {detection_summary}")

        return detections

    def draw_detections(
        self,
        frame: np.ndarray,
        detections: List[DetectionResult],
        show_confidence: bool = True,
        show_class_name: bool = True
    ) -> np.ndarray:
        """
        在图像上绘制检测结果

        Args:
            frame: 输入图像
            detections: 检测结果列表
            show_confidence: 是否显示置信度
            show_class_name: 是否显示类别名称

        Returns:
            绘制后的图像
        """
        frame_copy = frame.copy()

        for detection in detections:
            x1, y1, x2, y2 = detection.box
            color = self._get_color(detection.class_id)

            # 绘制边界框
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)

            # 准备标签文本
            label_parts = []
            if show_class_name:
                label_parts.append(detection.class_name)
            if show_confidence:
                label_parts.append(f"{detection.confidence:.2f}")

            label = " ".join(label_parts)

            # 绘制标签背景和文本
            if label:
                (label_width, label_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
                )
                y1_label = max(y1, label_height + 10)

                cv2.rectangle(
                    frame_copy,
                    (x1, y1_label - label_height - baseline - 5),
                    (x1 + label_width, y1_label),
                    color,
                    -1
                )
                cv2.putText(
                    frame_copy,
                    label,
                    (x1, y1_label - baseline),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1
                )

        return frame_copy

    def _get_color(self, class_id: int) -> Tuple[int, int, int]:
        """
        根据类别ID获取颜色

        Args:
            class_id: 类别ID

        Returns:
            (B, G, R)颜色元组
        """
        idx = class_id % len(self.DEFAULT_COLORS)
        return self.DEFAULT_COLORS[idx]

    def get_model_info(self) -> Dict:
        """
        获取模型信息

        Returns:
            包含模型信息的字典
        """
        return {
            "classes": self.model.names,
            "confidence_threshold": self.confidence_threshold,
            "iou_threshold": self.iou_threshold
        }
