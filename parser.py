import logging
import json


logger = logging.getLogger(__name__)


def extract_messages(json_string):
    try:
        lis = json_string.split('\n')
        for msg in lis:
            try:
                res = parse_single_message(msg)
                if res is not None:
                    yield res
            except Exception as e:
                logger.error(f"parse_single_message other error: {e}\n {msg}")
    except Exception as e:
        logger.error(f"extract_messages other error: {e}\n{json_string}")
    # 生成器自然终止，不返回 None


def parse_single_message(msg):
    # 初始回应消息，可能多个消息同时回，无法json解析
    if "id" in msg and ("subscribe" in msg or "connect" in msg):
        logger.debug(f"### Initial response: {msg}")
        return

    try:
        data = json.loads(msg)
    except json.JSONDecodeError as e:
        logger.error(f"### Invalid JSON format: {msg}")
        return

    # 空消息或非push消息, 忽略
    if len(data) == 0:
        logger.debug(f"### heartbeat: {msg}")
        return
    elif 'push' not in data:
        logger.warning(f'### non-push: {msg}')
        return

    channel = data['push']['channel']
    if 'newChatMessage' in channel:
        message = data['push']['pub']['data']['message']
        message_type = message.get('type', 'unknown')  # 使用get避免KeyError
        created_at = message.get('createdAt', None)
        if message_type == 'text':
            user_id = message['userData']['id']
            username = message['userData']['username']
            info = message['details']['body']
            logger.info(f'{username} said: {info}')
            logger.debug(f'### comment msg: {msg}')
        elif message_type == 'tip':
            user_id = message['userData']['id']
            username = message['userData']['username']
            info = message['details']['amount']
            logger.info(f'{username} tipped: {info}')
            logger.debug(f'### tip msg: {msg}')
            return info
        elif message_type == 'lovense':
            logger.info('lovense triggered ...')
            # 以下对匿名情况无效，无clientUserInfo
            # user_id = message['details']['lovenseDetails']['clientUserInfo']['id']
            # username = message['details']['lovenseDetails']['clientUserInfo']['username']
            # info = message['details']['lovenseDetails']['detail']
            # logger.info(f'{username} lovense: {info}')
            logger.debug(f'### lovense msg: {msg}')
        else:
            logger.debug(f"### Unknown newChatMessage type: {msg}")
    elif 'userUpdated' in channel:
        try:
            status = data['push']['pub']['data']['user']['status']
            statusChangedAt = data['push']['pub']['data']['user']['statusChangedAt']
            logger.info(f'userUpdated status to: {status}')
            logger.debug(f'### userUpdated: {msg}')
        except KeyError as e:
            logger.error(f"userUpdated KeyError: {msg}")
    elif 'broadcastSettingsChanged' in channel:
        logger.debug(f'### broadcastSettingsChanged: {msg}')
    else:
        logger.debug(f'### Unknown channel: {msg}')


def parse_monitor_data(data):
    status = data['user']['user']['status']
    sid = data['user']['user']['id']
    return {
        'status': status,
        'sid': sid
    }


