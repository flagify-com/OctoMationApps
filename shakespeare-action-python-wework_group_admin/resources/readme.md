# 企业微信群聊管理工具
## 介绍
企业微信群聊管理工具是一款基于Python的企业微信群聊管理工具，可以帮助企业管理微信群聊，包括创建群聊会话、修改群聊会话、查看群聊会话、发送消息等。

- 版本：v1.1
- 作者：[wzfukui](https://github.com/wzfukui)
- 更新时间：2024-04-23

## 功能
- 创建群聊会话
    - 名称
    - 群主
    - 人员
- 修改群聊会话
    - 名称
    - 群主
    - 增加人员
    - 移除人员
- 查看群聊会话
    - 成员列表
    - 群主
    - 群名
- 发送文本消息
- 发送图片消息（未实现）
- 发送文件消息（未实现）
- 发送语音消息（未实现）
- 发送视频消息（未实现）
- 发送链接消息（未实现）

##  配置参数
- apiserver_base_url：企业微信API服务器地址，默认为https://qyapi.weixin.qq.com/cgi-bin
- corpid：企业ID，在企业微信管理后台-我的企业界面，https://work.weixin.qq.com/wework_admin/frame#profile
- corpsecret：应用Secret，在企业微信管理后台-应用管理-自建应用的配置界面，https://work.weixin.qq.com/wework_admin/frame#apps/modApiApp/5629501796623943

> appid，应用ID，硬编码：wework_group_admin

## 安装组件

```bash
pip install python-dotenv
```

## 参考信息
- [企业内部开发>服务端API>消息推送>应用发送消息到群聊会话>概述](https://developer.work.weixin.qq.com/document/path/90244)
- [获取access_token](https://developer.work.weixin.qq.com/document/path/91039)

## Relesae Notes
- v1.1：追加Python组件python-dotenv安装说明，支持从.env文件读取配置参数