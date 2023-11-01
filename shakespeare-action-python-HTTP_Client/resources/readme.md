
# 通用HTTP Client

## 一、APP介绍


描述：本应用是一个通用的HTTP Client，支持GET、POST、PUT、DELETE等HTTP请求，允许用自定义HTTP HEAD、BODY、PROXY、TIMETOUT等参数。


| 内容 | 详细描述 |
| ---- | ------ |
| app版本      | 1.0.1 |
| 发布时间     | 2023-11-01|02:27:06 |
| 应用连接方式  | 标准HTTP请求 |
| 支持版本     | HTTP/1.1 |
| 作者        |  [@wzfukui](https://github.com/wzfukui) |

## 二、app使用注意事项

1）APP已测试通过型号&版本

| 型号   | 软件版本  |
| ----- | ------- |
| 无 |  |

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
        "description": "HTTP请求头中的Content-Type，默认：application/json",
        "default_value": "application/json",
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
    "HEADER": {
        "data_type": "string",
        "description": "自定义HTTP头，KEY:VALUE，按行填写。",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 4
    },
    "BODY": {
        "data_type": "string",
        "description": "HTTP请求体（Form模式需要自行URL Encode）",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 5
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
                "PUT": "PUT",
                "TRACE": "TRACE"
            }
        ],
        "required": true,
        "order": 6
    },
    "PROXY": {
        "data_type": "string",
        "description": "代理服务器，如：http://127.0.0.1:3128",
        "default_value": "",
        "options": "",
        "required": false,
        "order": 7
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
        "order": 8
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
        "order": 9
    },
    "TIMEOUT": {
        "data_type": "integer",
        "description": "HTTP请求超时（秒）",
        "default_value": 60,
        "options": "",
        "required": false,
        "order": 10
    }
}
```

**出参说明**    

| 参数  | 类型   | 数据样例  | 说明 |
| ---- | ----- | ------- | ---- |  
| action_result.code |  integer  | 200 |  APP执行返回状态码，默认：200  |
| action_result.msg |  string  | 请求发送成功，请确认返回结果:) |  APP执行返回的消息  |
| action_result.data.http_response_code |  integer  | 200 |  HTTP返回的状态码  |
| action_result.data.http_response_text |  string  | `<html>...</html>`，`{"errcode":0,"errmsg":"ok"}` |  HTTP返回的文本结果  |

使用过程截图：

HTTP Client请求示例

> 稍后补上，github不让上传这个图片。

HTTP Client请求钉钉webhook

<img width="743" alt="om-http_client_request_dingtalk-webhook" src="https://github.com/wzfukui/OctoMationApps/assets/146505187/a9beff9e-ce8b-4c31-b273-480dba80343f">


## 三、资源配置说明

###  1）基本信息配置

| 配置项     | 样例                  | 说明                                           |
| ---------- | --------------------- | ---------------------------------------------- |
| 资源名     |     | 资源名称具备可辨识度，比如设备所在的位置       |
| 描述       |  | 描述尽可能清晰              |
| 产品供应商 |  WZZN | 产品生产厂商（可选）        |
| 产品名称   |  通用HTTP客户端  | 产品名称 （可选）    |
| 执行引擎   | 任意引擎  | 在多引擎环境下可以指派执行引擎，默认“任意引擎” |
        
### 2）资源配置参数

| 参数 | 类型 | 样例 | 必须 | 默认值 | 说明 |
| ---- | ---- | ---- | ---- | ------ | ---- |
|      |      |      |      |        |      |
