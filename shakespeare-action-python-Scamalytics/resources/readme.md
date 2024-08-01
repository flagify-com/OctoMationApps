
# APP文档帮助文档

## 一、APP介绍

<!--产品描述（从官网下载），给对接的产品顺便打个广告-->

[Scamalytics](https://scamalytics.com/) 为企业提供安全产品，帮助它们检测和防止欺诈。产品在两个不同的层面上工作：

- 检测到你的在线服务的高风险连接，以每个 IP 地址的 IP 欺诈评分的形式呈现。你可以使用我们的 IP 地址查询和 API 来检查这些评分。

- 基于共享黑名单和机器学习，检测到跨多个数据点的高风险用户。这个产品非常适合拥有多个用户数据点的公司，例如约会服务和社交网络，特别有效地对抗约会骗子和浪漫欺诈。

你可以使用Scamalytics在线的IP检查工具查看IP质量产品的实际效果。这个工具会给你一个代表该IP欺诈风险的IP评分，以及其他附加信息，例如该IP是否运行代理服务器。

| 内容 | 详细描述 |
| ------------ | -------------- |
| app版本      | 2.0.2 |
| 发布时间     | 2022-05-27 |
| 更新时间     | 2024-07-31 |
| 应用连接方式 | HTTP请求 |
| 支持版本     | 截至20220527可用 |
| 作者         | 海燕（主）、WZ-Alice、wzfuki |

## 二、app使用注意事项

1）APP已测试通过型号&版本

| 型号      | 软件版本       |
| ------------ | -------------- |
| 无 | 截至20240731可用，官方接口可用 |

2）补充说明
> 网址：https://scamalytics.com/ip  
> 等级说明： very high/high/medium/low

3）注意：

**如果没有配置资源参数，程序将使用Web爬虫方式去官方网站查询IP信息，并根据网页内容进行解析。**

## 三、动作说明

###
### 1）get_ip_fraud_risk_info（老版本：search_ip）
动作描述：查询IP欺诈风险信息

**入参说明**

| 参数         | 类型   | 数据样例                 | 必须 | 默认值 | 说明                                              |
| ------------ | -------- | ------------------------ | ---- | ------ | ------------------------------------------------- |
| ip |  string  |  | True |  |  查询的IP地址  |

**出参说明**

| 参数                          | 类型   | 数据样例                       | 默认值 | 说明         |
| ----------------------------- | ------ | ------------------------------ | ------ | ------------ |
| action_result.data.ip | string  | 104.21.76.129    |     | 查询IP  |
| action_result.data.score | integer  |   10  |     | 风险评分  |
| action_result.data.risk | string  |   low  |     | 风险级别， 威胁等级：very high/high/medium/low  |
| action_result.data.anonymizing_vpn | boolean  |  True   |     | 是否VPN  |
| action_result.data.tor | boolean  |  False  |     | 是否tor  |
| action_result.data.server | boolean  |  False   |     | 是否服务器地址  |
| action_result.data.public_proxy | boolean  |   False  |     | 是否公共代理服务器  |
| action_result.data.web_proxy | boolean  |  False   |     | 是否WEB代理服务器  |
| action_result.data.ip_country_code | string  |  CA   |     | 国家编码  |
| action_result.data.ip_country_name | string  | Canada    |     | 国家名称  |
| action_result.data.ip_state_name | string  |  Ontario   |     | 省/州  |
| action_result.data.ip_city | string  |  Toronto   |     | 城市  |
| action_result.data.ip_district | string  |   Toronto  |     | 市区  |
| action_result.data.isp_name | string  |   Cloudflare, Inc.  |     | ISP信息  |
| action_result.data.isp_fraud_score | integer  |   5  |     | ISP欺诈分值  |
| action_result.data.organization_name | string  |  Cloudflare, Inc.   |     | 组织信息  |
| action_result.data.as_number | string  | 13335    |     | AS编号  |
| action_result.data.url | string  |  https://scamalytics.com/ip/104.21.76.129"   |     | 在线查询URL  |

输出示例：

```json
{
    "code": 200,
    "msg": "",
    "data": {
        "method": "api",
        "err_code": 0,
        "err_msg": "",
        "ip": "104.21.76.129",
        "hostname": "",
        "score": 0,
        "risk": "low",
        "anonymizing_vpn": false,
        "tor": false,
        "server": true,
        "public_proxy": false,
        "web_proxy": false,
        "search_engine_robot": false,
        "ip_country_code": "CA",
        "ip_state_name": "Ontario",
        "ip_city": "Toronto",
        "ip_district": "Toronto",
        "ip_postcode": "M5A",
        "ip_geolocation": "-79.3832,43.6532",
        "ip_geolocation_longtitude": -79.3832,
        "ip_geolocation_latitude": 43.6532,
        "proxy_type": "DCH",
        "connection_type": "",
        "as_number": "13335",
        "isp_name": "Cloudflare, Inc.",
        "isp_fraud_score": "",
        "organization_name": "Cloudflare, Inc.",
        "url": "https://scamalytics.com/ip/104.21.76.129",
        "exec": "",
        "credits": {
            "credits_used": 0,
            "credits_remaining": 0,
            "last_sync_timestamp_utc": "",
            "seconds_elapsed_since_last_sync": 0,
            "note": ""
        },
        "ip_country_name": "Canada"
    }
}
```

## 三、资源配置说明

###  1）基本信息配置

| 配置项     | 样例                  | 说明                                           |
| ---------- | --------------------- | ---------------------------------------------- |
| 资源名     | Scamalytics              | 资源名称具备可辨识度，比如设备所在的位置       |
| 描述       | Scamalytics | 资源描述 | 描述尽可能清晰                                 |
| 产品供应商 | Scamalytics            | 产品生产厂商（可选）                           |
| 产品名称   | IP Fraud Risk        | 产品名称 （可选）                              |
| 执行引擎   | 任意引擎              | 在多引擎环境下可以指派执行引擎，默认“任意引擎” |


### 2）资源配置参数

如果没有配置资源参数，程序将使用Web爬虫方式去官方网站查询IP信息，并根据网页内容进行解析。

| 参数 | 类型 | 样例 | 必须 | 默认值 | 说明                         |
| ---- | ---- | ---- | ---- | ------ | ---------------------------- |
| api_user | string | flagify | 否 | / | 调用API的用户名 |
| api_key | pasword | ********** | 否 | / | 调用API的KEY |

## 参考资料：

- [Scamalytics官方API文档](https://scamalytics.com/docs/scamalytics_IP_Fraud_Score_API_2.2.pdf)

## 发布记录
- 2022-05-27：发布APP版本1.0.2
- 2024-07-31：发布APP版本2.0.2
  - 重新Web查询构成
  - 增加API查询方式