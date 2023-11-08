
# 通用HTTP Client

## 一、APP介绍


描述：本应用是一个通用的HTTP Client，支持GET、POST、PUT、DELETE等HTTP请求，允许用自定义HTTP HEAD、BODY、PROXY、TIMETOUT等参数。


| 内容 | 详细描述 |
| ---- | ------ |
| app版本      | 1.0.5 |
| 发布时间     | 2023-11-08 15:13:00 |
| 应用连接方式  | 标准HTTP请求 |
| 支持版本     | HTTP/1.1 |
| 作者        |  [@wzfukui](https://github.com/wzfukui) |

## 二、app使用注意事项

1）APP已测试通过型号&版本

| 型号   | 软件版本  |
| ----- | ------- |
| / | / |

2）作者提示

> 默认超时60秒
> 文本编码为：UTF-8
> Query和表单格式的Body，需要用户自行完成URL编码


3）更新说明
> 首次发布

4) URL格式说明
- [rfc1738](https://datatracker.ietf.org/doc/html/rfc1738)
- [Wikipedia:URL](https://en.wikipedia.org/wiki/URL)


## 三、动作说明

### 1）http_request
动作描述：HTTP请求
对应接口：

**入参说明**

| 参数  | 类型 | 数据样例 | 必须 | 默认值 | 说明   |
| ---- | ----- | ---- | ---- | ---- | ---- |
| SERVER |  string  | https://user:pass@example.com:8080 | 是 |  |  URL服务器  |
| PATH |  string  | /user/info | 是 | / |  URL路径 |
| QUERY |  string  | user=Chris&comment=I%20love%20OctoMation| 否 | 空 |  URL请求参数(不带?，需自行做好URL Encode) |
| CONTENT_TYPE |  string  | application/json| 否 | application/json |  HTTP请求头中的Content-Type |
| USER_AGENT |  string  | Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 | 否 | 空 |  HTTP请求头中的Content-Type |
| COOKIES |  string  | vk=70acfa88; cbc-sid=2043816; ua=0b690880; uba_countrycode=HK;| 否 | 空 |  HTTP请求头中的Cookie字符串 |
| COOKIE_FILE |  string  | /tmp/cookie.1312112.pkl | 否 | 空 |  存储Cookie的文件，优先级低于COOKIES |
| HEADER |  string  | KEY:VALUE| 否 | 空 |  自定义HTTP头 |
| BODY |  string  | 一段文本 | 否 | 空 |  HTTP请求体（Form模式需要自行URL Encode） |
| METHOD |  string  | GET| 否 | GET |  HTTP请求方法 |
| PROXY |  string  | http://127.0.0.1:3128| 否 | 空 |  代理服务器 |
| ALLOW_REDIRECTS |  string  |True| 否 | True |  是否允许重定向 |
| VERIFY_SSL |  string  |True| 否 | True |  是否校验SSL证书 |
| TIMEOUT |  string  |120| 否 | 60 |  HTTP请求超时（秒） |


```json
{
    "SERVER": {
        "data_type": "string",
        "description": "URL服务器，如：https://user:pass@example.com:8080",
        "default_value": "",
        "options": "",
        "required": true,
        "order": 0
    },
    "PATH": {
        "data_type": "string",
        "description": "URL路径，如：/user/info，默认为：/",
        "default_value": "/",
        "options": "",
        "required": true,
        "order": 1
    },
    "QUERY": {
        "data_type": "string",
        "description": "URL请求参数(不带?，需自行做好URL Encode，如：user=Chris&comment=I%20love%20OctoMation）",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 2
    },
    "CONTENT_TYPE": {
        "data_type": "string",
        "description": "HTTP请求头中的Content-Type，默认为空",
        "default_value": "",
        "options": [
            {
                "application/json": "application/json",
                "text/html": "text/plain",
                "text/plain": "text/plain",
                "application/x-www-form-urlencoded": "application/x-www-form-urlencoded"
            }
        ],
        "required": false,
        "order": 3
    },
    "USER_AGENT": {
        "data_type": "string",
        "description": "HTTP请求头中的User Agent，默认为：OctoMation-HTTP-Client v1.0.0",
        "default_value": "OctoMation-HTTP-Client v1.0.0",
        "options": [
            {
                "OctoMation-HTTP-Client v1.0.0": "OctoMation-HTTP-Client v1.0.0",
                "Firefox+Win": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                "Chrome+macOS": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Huawei P30 Pro": "Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
                "iPhone 13 Pro Max": "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
                "Edge+Win10": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
            }
        ],
        "required": false,
        "order": 4
    },
    "HEADER": {
        "data_type": "string",
        "description": "自定义HTTP头，KEY:VALUE，按行填写。",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 5
    },
    "BODY": {
        "data_type": "string",
        "description": "HTTP请求体（Form模式需要自行URL Encode）",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 6
    },
    "METHOD": {
        "data_type": "string",
        "description": "HTTP请求方法，默认：GET",
        "default_value": "GET",
        "options": [
            {
                "HEAD": "HEAD",
                "GET": "GET",
                "POST": "POST",
                "DELETE": "DELETE",
                "OPTIONS": "OPTIONS",
                "PUT": "PUT"
            }
        ],
        "required": true,
        "order": 7
    },
    "PROXY": {
        "data_type": "string",
        "description": "代理服务器，如：http://127.0.0.1:3128",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 8
    },
    "ALLOW_REDIRECTS": {
        "data_type": "boolean",
        "description": "是否允许重定向，默认：True",
        "default_value": true,
        "options": [
            {
                "是": true,
                "否": false
            }
        ],
        "required": false,
        "order": 9
    },
    "VERIFY_SSL": {
        "data_type": "boolean",
        "description": "是否校验SSL证书，默认：True",
        "default_value": true,
        "options": [
            {
                "是": true,
                "否": false
            }
        ],
        "required": false,
        "order": 10
    },
    "TIMEOUT": {
        "data_type": "integer",
        "description": "HTTP请求超时（秒）",
        "default_value": 60,
        "options": "",
        "required": false,
        "order": 11
    },
    "COOKIES": {
        "data_type": "string",
        "description": "适用于HTTP请求头的Cookie字符串，作为入参优先级大于：COOKIE_FILE，默认：空",
        "default_value": "",
        "options":"",
        "required": false,
        "order": 12
    },
    "COOKIE_FILE": {
        "data_type": "string",
        "description": "存储Cookie的文件路径，默认：空，不存储",
        "default_value": "",
        "options": [
            {
                "随机生成一个Cookie文件": "__RANDOM__COOKIE__FILE__",
                "不使用Cookie文件": ""
            }
        ],
        "required": false,
        "order": 13
    }
}
```

**出参说明**    

| 参数  | 类型   | 数据样例  | 说明 |
| ---- | ----- | ------- | ---- |  
| action_result.code |  integer  | `200` |  APP执行返回状态码，默认：200  |
| action_result.msg |  string  | `请求发送成功，请确认返回结果:)` |  APP执行返回的消息  |
| action_result.data.http_response_code |  integer  | `200` |  HTTP返回的状态码  |
| action_result.data.http_response_text |  string  | `<html>...</html>`，`{"errcode":0,"errmsg":"ok"}` |  HTTP返回的文本结果  |
| action_result.data.http_response_headers |  json  | `{"Server": "nginx/1.12.2", "Content-Type": "text/html"}` |  JSON格式的HTTP Header  |
| action_result.data.cookies |  string  | `BAIDUID=5A19B:FG=1; BIDUPSID=5A19BE8392; PSTM=1699268694` |  Cookie字符串  |
| action_result.data.cookie_file |  string  | `/tmp/cookie_12121212.pkl` |  存放cookie的文件路径  |


使用过程截图：

HTTP Client请求示例

> 稍后补上，github不让上传这个图片。

HTTP Client请求钉钉webhook

<img width="743" alt="om-http_client_request_dingtalk-webhook" src="https://github.com/wzfukui/OctoMationApps/assets/146505187/a9beff9e-ce8b-4c31-b273-480dba80343f">


## 三、资源配置说明

###  1）基本信息配置

| 配置项     | 样例                  | 说明                                           |
| ---------- | --------------------- | ---------------------------------------------- |
| 资源名     |     | /       |
| 描述       |  | /              |
| 产品供应商 |  WZZN | 产品生产厂商（可选）        |
| 产品名称   |  通用通用HTTP客户端  | 产品名称 （可选）    |
| 执行引擎   | 任意引擎  | 在多引擎环境下可以指派执行引擎，默认“任意引擎” |
        
### 2）资源配置参数

| 参数 | 类型 | 样例 | 必须 | 默认值 | 说明 |
| ---- | ---- | ---- | ---- | ------ | ---- |
|      |      |      |      |        |      |


# Release log

- 2023-11-08 15:13:00 v1.0.5 修复HTTP Header赋值value时强制小写的bug
- 2023-11-07 23:03:00 v1.0.4 增加HTTP Header JSON的输出
- 2023-11-07 14:08:00 v1.0.3 入参在cookie_file基础上增加cookie string的支持
- 2023-11-06 20:09:10 v1.0.2 增加Cookie支持
- 2023-11-03 14:13:27 v1.0.1 删除空白文件
- 2023-11-01 02:27:06 v1.0.0 初始 
