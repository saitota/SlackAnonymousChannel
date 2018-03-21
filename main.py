import json
import logging
import urllib.request
import os

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def event_to_dict(event):
    if 'body' in event:
        body = json.loads(event.get('body'))
        return body
    elif 'token' in event:
        body = event
        return body
    else:
        logger.error('unexpected event format')
        exit


class ChallangeJson(object):
    def data(self, key):
        return {
            'isBase64Encoded': 'true',
            'statusCode': 200,
            'headers': {},
            'body': key
        }


def handler(event, context):
    #getenv
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    HOOK_CHANNEL = os.environ['HOOK_CHANNEL']
    #REPLY_WORD = os.environ['REPLY_WORD']
    BOT_NAME = os.environ['BOT_NAME']
    BOT_ICON = os.environ['BOT_ICON']
    DM_MESSAGE = os.environ['DM_MESSAGE']

    #受信したjsonをLogsに出力
    logging.info(json.dumps(event))

    # Output the received event to the log
    logging.info(json.dumps(event))
    body = event_to_dict(event)

    # return if it was challange-event
    if 'challenge' in body:
        challenge_key = body.get('challenge')
        logging.info('return challenge key %s:', challenge_key)
        return ChallangeJson().data(challenge_key)

    # API headers
    # join だったら DM
    if body.get('event').get('channel') == HOOK_CHANNEL and body.get('event').get('subtype','') == 'channel_join':
        headers_dm = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(BOT_TOKEN)
        }
        # DM Open 処理
        url_conv_open = 'https://slack.com/api/conversations.open'
        data_dm_open = {
            'token': OAUTH_TOKEN,
            'users': body.get('event').get('user')
        }
        req = urllib.request.Request(url_conv_open, data=json.dumps(data_dm_open).encode('utf-8'), method='POST', headers=headers_dm)
        res = urllib.request.urlopen(req)
        logger.info('dm list result: %s', res.msg)
        conv_channel = json.loads(res.read().decode('utf8'))
        # dm  送信処理
        url_dm_post = 'https://slack.com/api/chat.postMessage'
        data_dm = {
            'token': OAUTH_TOKEN,
            'channel': conv_channel.get('channel').get('id'),
            'text': DM_MESSAGE,
            'username': BOT_NAME,
            'icon_emoji': BOT_ICON
        }
        req = urllib.request.Request(url_dm_post, data=json.dumps(data_dm).encode('utf-8'), method='POST', headers=headers_dm)
        res = urllib.request.urlopen(req)
        logger.info('dm send result: %s', res.msg)

    #投稿があったときの処理
    elif body.get('event').get('channel') == HOOK_CHANNEL and body.get('event').get('username') != BOT_NAME and body.get('event').get('subtype','') == '':
        logger.info('hit!: %s', HOOK_CHANNEL)
        headers_delete = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(OAUTH_TOKEN)
        }
        headers_post = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(BOT_TOKEN)
        }
        url_delete = 'https://slack.com/api/chat.delete'
        url_post = 'https://slack.com/api/chat.postMessage'
        data_delete = {
            'token': OAUTH_TOKEN,
            'channel': HOOK_CHANNEL,
            'ts': body.get('event').get('event_ts')
        }
        data_post = {
            'token': OAUTH_TOKEN,
            'channel': HOOK_CHANNEL,
            'text': body.get('event').get('text'),
            'username': BOT_NAME,
            'icon_emoji': BOT_ICON
        }
        # DELETE処理
        req = urllib.request.Request(url_delete, data=json.dumps(data_delete).encode('utf-8'), method='POST', headers=headers_delete)
        res = urllib.request.urlopen(req)
        logger.info('delete result: %s', res.msg)
        # POST処理
        req = urllib.request.Request(url_post, data=json.dumps(data_post).encode('utf-8'), method='POST', headers=headers_post)
        res = urllib.request.urlopen(req)
        logger.info('post result: %s', res.msg)
        return {'statusCode': 200, 'body': 'ok'}

    return {'statusCode': 200, 'body': 'quit'}

