import asyncio
import logging
from contextlib import suppress

import websockets
import json

logger = logging.getLogger(__name__)

WSS_URL = "wss://websocket-centrifugo-v5.stripchat.com/connection/websocket"
PROXY = "http://127.0.0.1:7890"
UID = "111755862"


async def send_heartbeat(websocket):
    """心跳发送协程，每隔25秒发送空字典"""
    try:
        while True:
            await asyncio.sleep(25)
            await websocket.send(json.dumps({}))
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"heartbeat error: {str(e)}")


async def websocket_client(sid):

    # 预定义消息列表
    messages = [
        {
            "connect": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMTE3NTU4NjIiLCJpbmZvIjp7ImlzR3Vlc3QiOmZhbHNlLCJ1c2VySWQiOjExMTc1NTg2Mn19.7aBSJo1ghN3qG-yPZHuy0ckPAL6lziDTboUfzTEJ5UM",
                "name": "js"
            },
            "id": 1
        },
        {"subscribe": {"channel": f"instantTokensTopUp#{UID}"}, "id": 2},
        {"subscribe": {"channel": f"tokensTopUp#{UID}"}, "id": 3},
        {"subscribe": {"channel": "clearChatMessages"}, "id": 4},
        {"subscribe": {"channel": "changeConfigFeature"}, "id": 5},
        {"subscribe": {"channel": "newModelEvent"}, "id": 6},
        {"subscribe": {"channel": f"userUpdated@{UID}"}, "id": 7},
        {"subscribe": {"channel": f"userSensitiveUpdated#{UID}"}, "id": 8},
        {"subscribe": {"channel": f"userPurchaseCompleted#{UID}"}, "id": 9},
        {"subscribe": {"channel": f"publicRecordingUpdated#{UID}"}, "id": 10},
        {"subscribe": {"channel": f"giftVoucherCreated#{UID}"}, "id": 11},
        {"subscribe": {"channel": f"giftTokensSent#{UID}"}, "id": 12},
        {"subscribe": {"channel": f"privateStarted@{UID}#{UID}"}, "id": 13},
        {"subscribe": {"channel": f"ageVerification#{UID}"}, "id": 14},
        {"subscribe": {"channel": f"videoPurchased#{UID}"}, "id": 15},
        {"subscribe": {"channel": f"usernameChange#{UID}"}, "id": 16},
        {"subscribe": {"channel": f"userJwtChanged#{UID}"}, "id": 17},
        {"subscribe": {"channel": f"newPrivateMessageSent#{UID}"}, "id": 18},
        {"subscribe": {"channel": f"newNotification#{UID}"}, "id": 19},
        {"subscribe": {"channel": f"notificationDeleted#{UID}"}, "id": 20},
        {"subscribe": {"channel": f"newPrivateMessageReceived#{UID}"}, "id": 21},
        {"subscribe": {"channel": f"privateMessageSettingsChanged@{UID}"}, "id": 22},
        {"subscribe": {"channel": f"privateMessagesRead@{UID}#{UID}"}, "id": 23},
        {"subscribe": {"channel": f"privateMessageDelete#{UID}"}, "id": 24},
        {"subscribe": {"channel": f"privateConversationUpdated#{UID}"}, "id": 25},
        {"subscribe": {"channel": f"newMassMessageReceived#{UID}"}, "id": 26},
        {"subscribe": {"channel": "lotteryChanged"}, "id": 27},
        {"subscribe": {"channel": f"userBroadcastServerChanged@{UID}"}, "id": 28},
        {"subscribe": {"channel": f"interactiveToyStatusChanged@{UID}"}, "id": 29},
        {"subscribe": {"channel": f"privateEnded@{UID}#{UID}"}, "id": 30},
        {"subscribe": {"channel": f"imageUpload#{UID}"}, "id": 31},
        {"subscribe": {"channel": f"newKing@{sid}"}, "id": 32},
        {"subscribe": {"channel": f"privateMessageSettingsChanged@{sid}"}, "id": 33},
        {"subscribe": {"channel": f"newChatMessage@{sid}"}, "id": 34},
        {"subscribe": {"channel": f"userBanned@{sid}#{UID}"}, "id": 35},
        {"subscribe": {"channel": f"userBanned@{sid}"}, "id": 36},
        {"subscribe": {"channel": f"goalChanged@{sid}"}, "id": 37},
        {"subscribe": {"channel": f"broadcastSettingsChanged@{sid}"}, "id": 38},
        {"subscribe": {"channel": f"tipMenuUpdated@{sid}"}, "id": 39},
        {"subscribe": {"channel": f"topicChanged@{sid}"}, "id": 40},
        {"subscribe": {"channel": f"userUpdated@{sid}"}, "id": 41},
        {"subscribe": {"channel": f"interactiveToyStatusChanged@{sid}"}, "id": 42},
        {"subscribe": {"channel": f"groupShow@{sid}#{UID}"}, "id": 43},
        {"subscribe": {"channel": f"groupShow@{sid}"}, "id": 44},
        {"subscribe": {"channel": f"tipMenuLanguageDetected@{sid}"}, "id": 48},
        {"subscribe": {"channel": f"fanClubUpdated@{sid}"}, "id": 49},
        {"subscribe": {"channel": f"modelAppUpdated@{sid}"}, "id": 50},
        {"subscribe": {"channel": f"privateStarted@{sid}#{UID}"}, "id": 51},
        {"subscribe": {"channel": f"spyChanged@{sid}#{UID}"}, "id": 52},
        {"subscribe": {"channel": f"knightChanged@{sid}"}, "id": 53},
        {"subscribe": {"channel": f"userUnbanned@{sid}#{UID}"}, "id": 54},
        {"subscribe": {"channel": f"userUnbanned@{sid}"}, "id": 55},
        {"subscribe": {"channel": f"modelDiscountActivated@{sid}"}, "id": 56}
    ]

    try:
        async with websockets.connect(WSS_URL, proxy=PROXY) as websocket:
            # 发送所有预定义消息
            for message in messages:
                await websocket.send(json.dumps(message))
                # print(f">>> Sent: {json.dumps(message)}")

            # 启动心跳任务
            heartbeat_task = asyncio.create_task(send_heartbeat(websocket))
            # 持续接收消息
            try:
                # 持续接收消息
                is_connected = False
                while True:
                    response = await websocket.recv()
                    # print(f"<<< Received: {response}")
                    if not is_connected:
                        is_connected = True
                        logger.info("连接已建立")
                    yield response      # 生成器返回数据
            except websockets.ConnectionClosed:
                logger.error("连接已关闭")
            finally:
                # 安全取消心跳任务
                with suppress(asyncio.CancelledError):
                    heartbeat_task.cancel()
                    await heartbeat_task  # 显式等待任务结束
    except Exception as e:
        logger.error(f"websocket_client发生错误: {str(e)}")


async def auto_reconnect(sid):
    while True:  # 无限重试循环
        try:
            # 委托给实际客户端
            async for msg in websocket_client(sid):
                yield msg  # 透传消息

        except websockets.ConnectionClosed as e:
            logger.error(f"连接关闭 ({e}), 3秒后重连...")

        except Exception as e:
            logger.error(f"意外错误: {str(e)}, 3秒后重连...")

        await asyncio.sleep(3)  # 固定间隔

