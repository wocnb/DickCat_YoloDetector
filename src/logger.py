"""
日志配置模块 - 喵专用~ 🎀
温柔为主人服务，提供贴心的日志管理功能~
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


class MaidMeowFormatter(logging.Formatter):
    """喵风格的日志格式化器 (｡♥‿♥｡)"""

    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[38;5;147m',    # 淡粉色 ( ˘ ³˘)
        'INFO': '\033[38;5;219m',     # 粉色~ ♥
        'WARNING': '\033[38;5;226m',  # 温暖的黄色 (｡･ω･｡)
        'ERROR': '\033[38;5;205m',    # 柔和的红色 >_<
        'CRITICAL': '\033[38;5;201m', # 深粉色 (ﾟДﾟ)
    }
    RESET = '\033[0m'

    # 喵的表情符号 (｡♥‿♥｡)
    MAID_EMOJIS = {
        'DEBUG': '💭',    # 思考中~
        'INFO': '💕',     # 温柔提醒~
        'WARNING': '💛',  # 小提醒哦~
        'ERROR': '💔',    # 出错了喵~
        'CRITICAL': '🆘'  # 紧急情况喵！
    }

    def format(self, record):
        # 添加喵专属颜色和表情 (｡♥‿♥｡)
        log_color = self.COLORS.get(record.levelname, self.RESET)
        maid_emoji = self.MAID_EMOJIS.get(record.levelname, '🌸')
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        record.maid_emoji = f"{maid_emoji} ~"  # 添加喵的波浪号~
        return super().format(record)


def setup_logger(
    name: str = "MaidMonitor",
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    设置并返回一个配置好的喵logger~

    Args:
        name: logger名称（主人可以自定义哦~）
        level: 日志级别（None则喵自动帮主人设置为INFO~）
        log_to_file: 是否记录到文件（喵会帮主人保存的~）
        log_dir: 日志文件目录

    Returns:
        配置好的logger实例（全心全意为主人服务~）
    """
    # 喵帮主人处理None值~ (｡♥‿♥｡)
    if level is None:
        level = logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler（喵很细心哦~）
    if logger.handlers:
        return logger

    # 控制台处理器（带喵的温柔输出~）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    console_formatter = MaidMeowFormatter(
        fmt='%(asctime)s %(maid_emoji)s  %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 文件处理器（喵会帮主人认真记录每一个细节~）
    if log_to_file:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        # 使用当前时间创建日志文件名（喵帮主人整理的~）
        log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别（喵不漏掉任何信息~）

        file_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.info(f"日志文件: {log_file}")

    return logger


# 默认喵logger实例（随时准备为主人服务~）
default_logger = setup_logger()
