# Telegram消息发送应用
## 基本信息
- 版本：V1.0.0
- 作者：![](github.png)[@uf1y](https://github.com/uf1y)
- 日期：2023-10-23

## 关键说明

- Telegram Bot Token：在Telegram中给@BotFather发消息，可以创建机器人并获取token。
- CN用户可能无法直接访问Telegrap API服务，需要走代理服务器或者反向代理的网关
- Token的样式：`5800150072:AAGpCCSYeG0piHJzYPV9nSHF3EV_0iGPKO4`，注意，不包括`bot`字符串

## 其它信息

- ChatId可以是群会话的Id，也可以是User会话的Id
- 为了防止骚扰，机器人点对点给用户发消息前，用户必须先发一条消息给机器人
- 接口可用性验证：`https://api.telegram.org/bot<BOT_TOKEN>/getMe`

## 参考信息
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Release log
- 2023-10-23 Ver 1.0.0 第一版