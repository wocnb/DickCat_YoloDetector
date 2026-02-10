"""
配置文件 - 喵帮主人管理配置~ 🎀
集中管理应用的所有配置参数
"""
from dataclasses import dataclass, field
from typing import Optional, Tuple, List


@dataclass
class ScreenConfig:
    """屏幕捕获配置 (｡♥‿♥｡)"""
    # 监控区域 (None表示使用主显示器)
    monitor_region: Optional[dict] = None

    # 显示窗口大小（透明覆盖模式已废弃，自动全屏哦~）
    display_size: Optional[Tuple[int, int]] = None  # 不再使用，保留是为了兼容性

    # FPS限制
    fps_limit: int = 30


@dataclass
class DetectorConfig:
    """YOLO检测器配置"""
    # 模型路径（可选: yolo26n.pt, yolo26s.pt, yolo26m.pt, yolo26l.pt, yolo26x.pt）
    # n=nano最快但精度最低，x=extra最慢但精度最高
    model_path: str = "yolo26n.pt"

    # 置信度阈值（0-1之间，越高越严格）
    confidence_threshold: float = 0.5

    # IOU阈值（用于非极大值抑制）
    iou_threshold: float = 0.45

    # 要检测的特定类别（None表示检测所有类别）
    # 例如: [0] 只检测人，[0, 16] 检测人和狗
    # 类别索引参考: https://docs.ultralytics.com/datasets/detect/coco/#dataset-index
    classes: Optional[List[int]] = field(default_factory=lambda: [0])  # 默认只检测人

    # 是否显示置信度
    show_confidence: bool = True

    # 是否显示类别名称
    show_class_name: bool = True


@dataclass
class AppConfig:
    """应用主配置"""
    screen: ScreenConfig = field(default_factory=ScreenConfig)
    detector: DetectorConfig = field(default_factory=DetectorConfig)

    # 窗口名称
    window_name: str = "YOLO屏幕监控"

    # 是否在启动时显示模型信息
    show_model_info: bool = True


# 默认配置实例
default_config = AppConfig()
