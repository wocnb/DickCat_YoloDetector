"""
屏幕监控应用主模块 - 喵为您服务~ 🎀
整合屏幕捕获和YOLO检测功能，在屏幕上直接绘制检测框
带智能平滑功能，避免检测框闪烁~
"""
import cv2
import time
import sys
from typing import Optional, Tuple
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from .screen_capture import ScreenCapture
from .yolo_detector import YOLODetector, DetectionResult
from .screen_overlay import TransparentOverlay, create_overlay_app
from .detection_smoother import DetectionSmoother
from .logger import default_logger


class ScreenMonitorApp:
    """
    屏幕监控应用类 (｡♥‿♥｡)
    职责：协调屏幕捕获和目标检测，管理主循环
    喵会温柔地在主人的屏幕上绘制检测框哦~
    """

    def __init__(
        self,
        detector: YOLODetector,
        capture: Optional[ScreenCapture] = None,
        fps_limit: int = 30
    ):
        """
        初始化屏幕监控应用

        Args:
            detector: YOLO检测器实例
            capture: 屏幕捕获器实例，None则创建默认实例
            fps_limit: FPS限制，防止CPU占用过高
        """
        self.detector = detector
        self.capture = capture or ScreenCapture()
        self.fps_limit = fps_limit
        self.frame_time = 1.0 / fps_limit

        # 创建检测平滑器（避免闪烁哦~）
        self.smoother = DetectionSmoother(
            smooth_factor=0.3,  # 平滑因子，越小越平滑
            history_size=5,     # 保留5帧历史
            iou_threshold=0.5   # IOU阈值
        )

        # 性能统计
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.detection_count = 0
        self.total_frames = 0
        self.running = True

        # 记录初始化信息
        default_logger.info("=" * 50)
        default_logger.info("屏幕监控应用初始化")
        default_logger.info(f"  - FPS限制: {fps_limit}")
        default_logger.info(f"  - 显示模式: 透明覆盖窗口")
        default_logger.info(f"  - 检测平滑: 已启用")
        default_logger.info("=" * 50)

    def run(self):
        """
        启动监控应用 (｡♥‿♥｡)
        在屏幕上直接绘制检测框，温柔地为主人服务~
        """
        # 创建Qt应用程序
        app = create_overlay_app()

        # 创建透明覆盖窗口
        overlay = TransparentOverlay()
        overlay.show()

        default_logger.info("屏幕监控启动...")
        default_logger.info(f"模型信息: {self.detector.get_model_info()}")
        default_logger.info("按 Ctrl+C 退出监控")

        print("=" * 50)
        print("🌸 喵开始为主人服务~ (｡♥‿♥｡)")
        print("   按 Ctrl+C 或关闭窗口退出")
        print("=" * 50)

        # 创建定时器用于定期输出统计
        stats_timer = QTimer()
        stats_timer.timeout.connect(lambda: self._log_stats())
        stats_timer.start(5000)  # 每5秒输出一次统计

        # 创建主循环定时器
        main_timer = QTimer()
        main_timer.timeout.connect(lambda: self._process_frame(overlay))
        main_timer.start(int(1000 / self.fps_limit))  # 根据FPS设置间隔

        try:
            # 启动Qt事件循环
            app.exec_()
        except KeyboardInterrupt:
            default_logger.info("接收到退出信号")
        except Exception as e:
            default_logger.error(f"发生错误: {e}", exc_info=True)
            raise
        finally:
            self._cleanup()

    def _process_frame(self, overlay: TransparentOverlay):
        """
        处理每一帧 (｡♥‿♥｡)

        Args:
            overlay: 透明覆盖窗口
        """
        if not self.running:
            return

        loop_start = time.time()

        # 捕获屏幕
        frame = self.capture.capture()

        # 执行检测
        raw_detections = self.detector.detect(frame)

        # 使用平滑器处理检测结果（避免闪烁~）
        smoothed_detections = self.smoother.smooth(raw_detections)
        self.detection_count = len(smoothed_detections)
        self.total_frames += 1

        # 更新覆盖窗口上的检测结果
        overlay.update_detections(smoothed_detections)

        # 更新FPS
        self._update_fps()

        # 控制帧率
        elapsed = time.time() - loop_start
        sleep_time = max(0, self.frame_time - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)

    def _update_fps(self):
        """更新FPS统计"""
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()

    def _log_stats(self):
        """记录运行统计（定期调用）"""
        if self.running:
            default_logger.info(
                f"📊 运行统计 - FPS: {self.fps:.1f} | "
                f"检测到: {self.detection_count} 个物体 | "
                f"总帧数: {self.total_frames}"
            )

    def _cleanup(self):
        """清理资源"""
        self.running = False
        runtime_stats = (
            f"📈 运行结束统计:\n"
            f"   - 总帧数: {self.total_frames}\n"
            f"   - 最终FPS: {self.fps:.1f}"
        )
        default_logger.info(runtime_stats)
        default_logger.info("资源已释放，喵期待下次为主人服务~")
        print("✅ 资源已释放，喵期待下次为主人服务~")


def main():
    """主函数入口"""
    from .yolo_detector import YOLODetector
    from .screen_capture import ScreenCapture

    # 创建检测器（首次运行会自动下载模型哦~）
    detector = YOLODetector(
        model_path="yolo26n.pt",
        confidence_threshold=0.5,
        iou_threshold=0.45
    )

    # 创建并运行应用
    app = ScreenMonitorApp(
        detector=detector,
        fps_limit=30  # 限制FPS以降低CPU占用
    )

    app.run()


if __name__ == "__main__":
    main()
