"""
YOLO屏幕监控应用 - 主入口
使用YOLO模型实时监控和识别电脑屏幕内容
"""
import sys
from src.screen_monitor_app import ScreenMonitorApp
from src.yolo_detector import YOLODetector
from src.screen_capture import ScreenCapture
from src.config import AppConfig, default_config
from src.logger import default_logger, setup_logger


def create_app_from_config(config: AppConfig = default_config) -> ScreenMonitorApp:
    """
    根据配置创建应用实例

    Args:
        config: 应用配置对象

    Returns:
        ScreenMonitorApp实例
    """
    default_logger.info("开始创建应用实例...")

    # 创建检测器
    detector = YOLODetector(
        model_path=config.detector.model_path,
        confidence_threshold=config.detector.confidence_threshold,
        iou_threshold=config.detector.iou_threshold,
        classes=config.detector.classes
    )

    # 创建屏幕捕获器
    capture = ScreenCapture(monitor=config.screen.monitor_region)

    # 创建应用（透明覆盖模式，直接在屏幕上绘制哦~）
    app = ScreenMonitorApp(
        detector=detector,
        capture=capture,
        fps_limit=config.screen.fps_limit,
        enable_mouse_control=config.mouse.enabled,
        mouse_target_percent=config.mouse.target_percent
    )

    default_logger.info("应用实例创建完成")
    return app


def main():
    """主函数"""
    # 设置日志
    logger = setup_logger(
        name="YOLOMonitor",
        level=None,  # 使用默认INFO级别
        log_to_file=True
    )

    logger.info("=" * 60)
    logger.info("🚀 YOLO屏幕监控应用启动")
    logger.info("=" * 60)

    try:
        # 方式1: 使用默认配置
        app = create_app_from_config()
        app.run()

        # 方式2: 使用自定义配置
        # config = AppConfig()
        # config.detector.model_path = "yolo26s.pt"  # 使用更大的模型
        # config.detector.confidence_threshold = 0.7  # 提高置信度阈值
        # config.detector.classes = [0]  # 只检测人
        # config.screen.display_size = (1920, 1080)  # 更高的显示分辨率
        #
        # app = create_app_from_config(config)
        # app.run()

    except Exception as e:
        logger.error(f"程序异常退出: {e}", exc_info=True)
        sys.exit(1)

    logger.info("程序正常退出")


if __name__ == "__main__":
    main()
