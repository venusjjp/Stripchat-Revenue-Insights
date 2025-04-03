
import asyncio
import os
import time
from datetime import datetime
import logging

from room_module import Room

if not os.path.exists("log"):
    os.mkdir("log")

# 初始化根 Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # 全局最低级别（DEBUG 及以上都处理）

time_str = datetime.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M%S")
file_handler = logging.FileHandler(rf".\log\tip_{time_str}.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)  # 文件记录的最低级别

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台输出的最低级别

# 定义日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加 Handler 到 Logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logging.getLogger("websockets").setLevel(logging.WARNING)  # 关闭 websockets 的 DEBUG 日志

# 测试日志输出
# logger.debug("Debug 信息（写入文件，不显示在控制台）")
# logger.info("Info 信息（写入文件并显示）")
# logger.warning("Warning 信息（写入文件并显示）")


def main(nickname):
    room = Room(nickname)
    asyncio.run(room.run())

