import logging
import aiohttp
import asyncio

logger = logging.getLogger(__name__)
UNIQ_ID = "ued4vct1knrwhoxb"


async def fetch_streamer_data(session, nickname, uniq=UNIQ_ID):
    url = f"https://zh.stripchat.com/api/front/v2/models/username/{nickname}/cam?timezoneOffset=-480&triggerRequest=loadCam&primaryTag=girls&uniq={uniq}"
    proxy = "http://127.0.0.1:7890"

    try:
        async with session.get(url, proxy=proxy) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        raise ValueError(f"请求出错: {e}")


async def monitor_streamer_data(nickname):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                data = await fetch_streamer_data(session, nickname)
                yield data
            except ValueError as e:
                logger.error(f"{e}")
                yield None
            except Exception as e:
                logger.error(f"monitor_streamer_data other error: {e}")
                yield None
            await asyncio.sleep(10)

