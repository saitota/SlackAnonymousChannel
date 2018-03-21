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

class PostData(object):
    def __init__(self):
        self.BOT_TOKEN = os.environ['BOT_TOKEN']
        self.OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
        self.BOT_NAME = os.environ['BOT_NAME']
        self.BOT_ICON = os.environ['BOT_ICON']
        self.DM_MESSAGE = os.environ['DM_MESSAGE']
    def headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(self.BOT_TOKEN)
        }
    def headers_oath(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(self.OAUTH_TOKEN)
        }
    def data_convopen(self,user):
        return {
            'token': self.OAUTH_TOKEN,
            'users': user
        }
    def data_dmsend(self,channel):
        return {
            'token': self.OAUTH_TOKEN,
            'channel': channel,
            'text': self.DM_MESSAGE,
            'username': self.BOT_NAME,
            'icon_emoji': self.BOT_ICON
        }
    def data_delete(self,channel,ts):
        return {
            'token': self.OAUTH_TOKEN,
            'channel': channel,
            'ts': ts
        }
    def data_message(self,channel,text,attachments,thread_ts):
        return {
            'token': self.OAUTH_TOKEN,
            'channel': channel,
            'text': text,
            'attachments':attachments,
            'thread_ts':thread_ts,
            'username': self.BOT_NAME,
            'icon_emoji': self.BOT_ICON
        }


def handler(event, context):
    #getenv
    HOOK_CHANNEL = os.environ['HOOK_CHANNEL']
    #REPLY_WORD = os.environ['REPLY_WORD']

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
        # DM Open 処理
        url_conv_open = 'https://slack.com/api/conversations.open'
        postdata = PostData()
        post_head = postdata.headers()
        post_data = postdata.data_convopen(body.get('event').get('user'))
        req = urllib.request.Request(url_conv_open, data=json.dumps(post_data).encode('utf-8'), method='POST', headers=post_head)
        res = urllib.request.urlopen(req)
        logger.info('dm list result: %s', res.msg)
        conv_channel = json.loads(res.read().decode('utf8'))
        # dm  送信処理
        url_dm_post = 'https://slack.com/api/chat.postMessage'
        post_data = postdata.data_dmsend(conv_channel.get('channel').get('id'))
        req = urllib.request.Request(url_dm_post, data=json.dumps(post_data).encode('utf-8'), method='POST', headers=post_head)
        res = urllib.request.urlopen(req)
        logger.info('dm send result: %s', res.msg)

    #投稿があったときの処理
    elif body.get('event').get('channel') == HOOK_CHANNEL and body.get('event').get('subtype','') == '':
        url_delete = 'https://slack.com/api/chat.delete'
        url_post = 'https://slack.com/api/chat.postMessage'
        postdata = PostData()
        post_head = postdata.headers()
        post_head_oath = postdata.headers_oath()
        post_delete = postdata.data_delete(HOOK_CHANNEL,body.get('event').get('event_ts'))
        post_message = postdata.data_message(
            HOOK_CHANNEL,
            body.get('event').get('text'),
            body.get('event').get('attachments'),
            body.get('event').get('thread_ts')
            )
        # DELETE処理
        req = urllib.request.Request(url_delete, data=json.dumps(post_delete).encode('utf-8'), method='POST', headers=post_head_oath)
        res = urllib.request.urlopen(req)
        logger.info('delete result: %s', res.msg)
        # POST処理
        req = urllib.request.Request(url_post, data=json.dumps(post_message).encode('utf-8'), method='POST', headers=post_head)
        res = urllib.request.urlopen(req)
        logger.info('post result: %s', res.msg)
        return {'statusCode': 200, 'body': 'ok'}

    return {'statusCode': 200, 'body': 'quit'}

