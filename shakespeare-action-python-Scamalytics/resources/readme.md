
# APP文档帮助文档

## 一、APP介绍

<!--产品描述（从官网下载），给对接的产品顺便打个广告-->

Scamalytics is an essential real-time smart assistant for Lovestruck. It empowers our moderation team, reduces their workload and helps ensure the highest levels of quality and curation that our members demand.

| 内容 | 详细描述 |
| ------------ | -------------- |
| app版本      | 1.0.2 |
| 发布时间     | 2022-05-27 |
| 应用连接方式 | HTTP请求 |
| 支持版本     | 截至20220527可用 |
| 作者         | 海燕（主）、WZ-Alice |

## 二、app使用注意事项

1）APP已测试通过型号&版本

| 型号      | 软件版本       |
| ------------ | -------------- |
| 无 | 截至20220527可用 |

2）补充说明
> 网址：https://scamalytics.com/ip  
> 等级说明： 威胁等级：low: 低,  medium：中， highes: 高


## 三、动作说明

###
### 1）search_ip
动作描述：查询IP

**入参说明**

| 参数         | 类型   | 数据样例                 | 必须 | 默认值 | 说明                                              |
| ------------ | -------- | ------------------------ | ---- | ------ | ------------------------------------------------- |
| ip |  string  |  | True |  |  查询的IP地址  |

**出参说明**

| 参数                          | 类型   | 数据样例                       | 默认值 | 说明         |
| ----------------------------- | ------ | ------------------------------ | ------ | ------------ |
| action_result.data.score | integer  |     |     | 风险评分  |
| action_result.data.risk | string  |     |     | 风险级别， 威胁等级：low: 低,  medium：中， highes: 高  |
| action_result.data.anonymizing_vpn | boolean  |     |     | 是否VPN  |
| action_result.data.tor | boolean  |     |     | 是否tor  |
| action_result.data.server | boolean  |     |     | 是否服务器地址  |
| action_result.data.public_proxy | boolean  |     |     | 是否公共代理服务器  |
| action_result.data.web_proxy | boolean  |     |     | 是否WEB代理服务器  |
| action_result.data.search_engine_robot | boolean  |     |     | 是否搜索引擎爬虫  |


## 三、资源配置说明

###  1）基本信息配置

| 配置项     | 样例                  | 说明                                           |
| ---------- | --------------------- | ---------------------------------------------- |
| 资源名     | IDC_FW01              | 资源名称具备可辨识度，比如设备所在的位置       |
| 描述       | IDC数据中心出口防火墙 | 描述尽可能清晰                                 |
| 产品供应商 | Palo Alto             | 产品生产厂商（可选）                           |
| 产品名称   | 下一代防火墙          | 产品名称 （可选）                              |
| 执行引擎   | 任意引擎              | 在多引擎环境下可以指派执行引擎，默认“任意引擎” |


### 2）资源配置参数

| 参数 | 类型 | 样例 | 必须 | 默认值 | 说明                         |
| ---- | ---- | ---- | ---- | ------ | ---------------------------- |

