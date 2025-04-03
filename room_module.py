import logging
import asyncio

from monitor import monitor_streamer_data
from parser import parse_monitor_data, extract_messages
from ws_client import auto_reconnect

logger = logging.getLogger(__name__)


class Room:
    def __init__(self, nickname):
        self.nickname = nickname
        self.status = None
        self.ws_task: asyncio.Task | None = None
        self.total = 0

    async def run_websocket(self, sid):
        try:
            async for output in auto_reconnect(sid):
                for data in extract_messages(output):
                    self.total += data
                    logger.info(f'已获取小费总和: {self.total}')
        except asyncio.CancelledError:
            logger.error("run_websocket 任务被主动终止")

    async def run(self):
        try:
            async for data in monitor_streamer_data(self.nickname):
                try:
                    res = parse_monitor_data(data)
                    status, sid = res['status'], res['sid']
                    if self.ws_task is None or self.ws_task.done():
                        self.ws_task = asyncio.create_task(self.run_websocket(sid))
                    if self.status != status:
                        self.status = status
                        logger.info(f"{self.nickname} 状态更新为: {status}")
                except Exception as e:
                    logger.error(f"Error while processing message: {e}")
        except asyncio.CancelledError:
            logger.error("run 任务被主动终止")

