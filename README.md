# 😎 Slack Anonymous Channel
It provides Anonymous chat channel at Slack.

***DEMO:***

![demo](https://user-images.githubusercontent.com/1152469/37695513-52bd3158-2d13-11e8-8626-dea07e1dd439.gif)

***DEMO-ja:***

![demo_ja](https://user-images.githubusercontent.com/1152469/37695515-5526551e-2d13-11e8-835d-bcd41861aa60.gif)


## Description
- The post will delete immediately and it will be re-posted by BOT.
- You can chat here like anonymously.
- Message/Share/Reply will be anonymized. Join/Leave/Upload will ignore.
- Sometimes posts are cache and displayed in `Slack client` or `notification`  before deleting.
- Send caution message on DM to member who joined channel to tell policy of channel.

## Requirement
- AWS Account
- Serverless Framework
- [serverless-plugin-aws-alerts](https://serverless.com/blog/serverless-ops-metrics/) (optional)
- Slack Account

## Installation
1. Create Slack BOT from [Here](https://api.slack.com/slack-apps)
    - Bot User
        - Display Name
        - Default Username
    - Permissions
        - OAuth & Permissions
            - Scopes
                - admin
                - channels:read
                - channels:write
                - channels:history
                - users:read
2. Get two tokens
    - Permissions
        - OAuth & Permissions
            - OAuth Access Token
            - Bot User OAuth Access Token

3. Make some channel like `#anonymous` and get channel id lke `C1234ABCD` from [here](https://api.slack.com/methods/channels.list/test)

4. Clone this repo.
```
$ git clone https://github.com/saitota/SlackAnonymousChannel.git
```

5. Modify environment_dev.yml 's two TOKENs to your token.
``` environment_dev.yml
OAUTH_TOKEN: 'xoxp-000000000000-000000000000-000000000000-0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x'
BOT_TOKEN: 'xoxb-000000000000-0x0x0x0x0x0x0x'
HOOK_CHANNEL: 'Cxxxxxxxx'
```

5. Deploy with Serverless Framework (you must aws-cli initialize before)
```
$ sls deploy
...
api keys:
  None
endpoints:
  POST - https://0x0x0x0x0x.execute-api.ap-northeast-1.amazonaws.com/dev/
functions:
  fnc: SlackAnonymousChannel-dev-fnc
```
6. Set Slack BOT endpoint and event subscribe settings 
    - Event Subscriptions
        - Request URL: `set your endopint url(you can see in your deploy log)`
    - Subscribe to Workspace Events
        - message.channels

7. Done! try to say `poop` at Slack.

# 🤔 Anything Else
I wrote article about this BOT.

[saitotak - Qiita](https://qiita.com/saitotak/)

# 🐑 Author
[saitotak](https://qiita.com/saitotak)

# ✍ License
[MIT](./LICENSE)
