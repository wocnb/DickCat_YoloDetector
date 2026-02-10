"""
检测结果平滑模块 🎀
避免检测框闪烁，为主人提供稳定的视觉体验~
"""
from collections import deque
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from .yolo_detector import DetectionResult


@dataclass
class TrackedDetection:
    """被跟踪的检测结果"""
    box: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    confidence: float
    class_id: int
    class_name: str
    frame_count: int = 0  # 跟踪帧数


class DetectionSmoother:
    """
    检测结果平滑器 (｡♥‿♥｡)
    使用移动平均和历史跟踪来减少检测框的闪烁~
    """

    def __init__(
        self,
        smooth_factor: float = 0.3,
        history_size: int = 5,
        iou_threshold: float = 0.5
    ):
        """
        初始化平滑器

        Args:
            smooth_factor: 平滑因子（0-1），越小越平滑
            history_size: 保留的历史帧数
            iou_threshold: IOU阈值，用于匹配相同目标
        """
        self.smooth_factor = smooth_factor
        self.history_size = history_size
        self.iou_threshold = iou_threshold

        # 跟踪的检测列表
        self.tracked_detections: List[TrackedDetection] = []

        # 每个跟踪目标的历史位置
        self.detection_histories: List[deque] = []

    def smooth(self, detections: List[DetectionResult]) -> List[DetectionResult]:
        """
        平滑检测结果

        Args:
            detections: 当前帧的检测结果

        Returns:
            平滑后的检测结果
        """
        if not detections:
            # 没有检测到目标，减少所有跟踪目标的生命值
            self._decay_trackings()
            return self._get_active_detections()

        # 匹配当前检测与已有跟踪
        matched_pairs, unmatched_detections, unmatched_trackings = self._match_detections(
            detections
        )

        # 更新已匹配的跟踪
        for detection_idx, tracking_idx in matched_pairs:
            self._update_tracking(
                tracking_idx,
                detections[detection_idx]
            )

        # 为未匹配的检测创建新跟踪
        for detection_idx in unmatched_detections:
            self._create_tracking(detections[detection_idx])

        # 移除过期的跟踪
        self._remove_expired_trackings(unmatched_trackings)

        # 返回平滑后的结果
        return self._get_active_detections()

    def _match_detections(
        self,
        detections: List[DetectionResult]
    ) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
        """
        匹配检测结果与已有跟踪

        Returns:
            (匹配对列表, 未匹配的检测索引, 未匹配的跟踪索引)
        """
        if not self.tracked_detections:
            return [], list(range(len(detections))), []

        matched_pairs = []
        matched_detections = set()
        matched_trackings = set()

        # 计算IOU矩阵
        iou_matrix = np.zeros((len(detections), len(self.tracked_detections)))
        for i, det in enumerate(detections):
            for j, track in enumerate(self.tracked_detections):
                iou_matrix[i, j] = self._calculate_iou(det.box, track.box)

        # 贪婪匹配
        for _ in range(min(len(detections), len(self.tracked_detections))):
            # 找到最大IOU
            max_idx = np.argmax(iou_matrix)
            det_idx, track_idx = max_idx // len(self.tracked_detections), max_idx % len(self.tracked_detections)

            if iou_matrix[det_idx, track_idx] >= self.iou_threshold:
                matched_pairs.append((det_idx, track_idx))
                matched_detections.add(det_idx)
                matched_trackings.add(track_idx)

                # 标记已匹配
                iou_matrix[det_idx, :] = -1
                iou_matrix[:, track_idx] = -1
            else:
                break

        # 未匹配的检测和跟踪
        unmatched_detections = [
            i for i in range(len(detections))
            if i not in matched_detections
        ]
        unmatched_trackings = [
            j for j in range(len(self.tracked_detections))
            if j not in matched_trackings
        ]

        return matched_pairs, unmatched_detections, unmatched_trackings

    def _update_tracking(self, tracking_idx: int, detection: DetectionResult):
        """更新已有跟踪"""
        tracking = self.tracked_detections[tracking_idx]

        # 平滑位置（指数移动平均）
        new_box = detection.box
        old_box = tracking.box

        smoothed_box = []
        for k in range(4):
            smoothed = int(old_box[k] * (1 - self.smooth_factor) + new_box[k] * self.smooth_factor)
            smoothed_box.append(smoothed)

        tracking.box = tuple(smoothed_box)
        tracking.confidence = detection.confidence
        tracking.class_name = detection.class_name
        tracking.frame_count += 1

        # 更新历史
        if tracking_idx >= len(self.detection_histories):
            self.detection_histories.append(deque(maxlen=self.history_size))
        self.detection_histories[tracking_idx].append(smoothed_box)

    def _create_tracking(self, detection: DetectionResult):
        """创建新跟踪"""
        new_tracking = TrackedDetection(
            box=detection.box,
            confidence=detection.confidence,
            class_id=detection.class_id,
            class_name=detection.class_name,
            frame_count=1
        )
        self.tracked_detections.append(new_tracking)
        self.detection_histories.append(deque([detection.box], maxlen=self.history_size))

    def _decay_trackings(self):
        """衰减所有跟踪（当没有检测到目标时）"""
        # 减少帧数但不立即删除，给予一定的容错时间
        for tracking in self.tracked_detections:
            tracking.frame_count = max(0, tracking.frame_count - 2)

    def _remove_expired_trackings(self, expired_indices: List[int]):
        """移除过期的跟踪（从后往前删除以保持索引正确）"""
        for idx in sorted(expired_indices, reverse=True):
            if self.tracked_detections[idx].frame_count <= 0:
                self.tracked_detections.pop(idx)
                if idx < len(self.detection_histories):
                    self.detection_histories.pop(idx)

    def _get_active_detections(self) -> List[DetectionResult]:
        """获取活跃的检测结果"""
        active_detections = []
        for tracking in self.tracked_detections:
            if tracking.frame_count > 0:
                active_detections.append(DetectionResult(
                    box=tracking.box,
                    confidence=tracking.confidence,
                    class_id=tracking.class_id,
                    class_name=tracking.class_name
                ))
        return active_detections

    @staticmethod
    def _calculate_iou(
        box1: Tuple[int, int, int, int],
        box2: Tuple[int, int, int, int]
    ) -> float:
        """
        计算两个框的IOU

        Args:
            box1, box2: (x1, y1, x2, y2)

        Returns:
            IOU值
        """
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2

        # 计算交集
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
            return 0.0

        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)

        # 计算并集
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area

        if union_area == 0:
            return 0.0

        return inter_area / union_area
