
# APP文档帮助文档

## 一、APP介绍


描述：产品介绍  


| 内容 | 详细描述 |
| ---- | ------ |
| app版本      | 1.0.0 |
| 发布时间     | 2023-10-05|10:53:06 |
| 应用连接方式  |  |
| 支持版本     |  |
| 作者        |  |

## 二、app使用注意事项

1）APP已测试通过型号&版本

| 型号   | 软件版本  |
| ----- | ------- |
| 无 |  |

2）作者提示
> 
> 

3）更新说明
> 
>


## 三、动作说明

### 1）requests
动作描述：HTTP请求
对应接口：

**入参说明**

| 参数  | 类型 | 数据样例 | 必须 | 默认值 | 说明   |
| ---- | ----- | ---- | ---- | ---- | ---- |
| url |  string  |  | True |  |  HTTP请求的url  |
| headers |  string  |  | False | {'User-Agent': 'HG-APP'} |  HTTP请求的请求头, 参数Demo: {'Content-Type': 'application/json', 'User-Agent': 'HG-APP'}  |
| ssl_verify |  boolean  |  | True | False |  HTTP请求的SSL验证  |
| data |  string  |  | False |  |  HTTP请求的请求体  |
| proxy |  string  |  | False |  |  HTTP请求代理, 参数Demo: {'http://':'http://localhost:8080','https://':'http://localhost:8081'}  |
| method |  string  |  | True | GET |  HTTP请求的请求方式  |

**出参说明**    

| 参数  | 类型   | 数据样例  | 说明 |
| ---- | ----- | ------- | ---- |  
| action_result.code |  integer  |  |  HTTP返回Code  |
| action_result.data |  string  |  |  HTTP返回的Json结果  |
| action_result.text |  string  |  |  HTTP返回的文本结果  |

## 三、资源配置说明

###  1）基本信息配置

| 配置项     | 样例                  | 说明                                           |
| ---------- | --------------------- | ---------------------------------------------- |
| 资源名     |     | 资源名称具备可辨识度，比如设备所在的位置       |
| 描述       |  | 描述尽可能清晰              |
| 产品供应商 |  wuzhi | 产品生产厂商（可选）        |
| 产品名称   |  http  | 产品名称 （可选）    |
| 执行引擎   | 任意引擎  | 在多引擎环境下可以指派执行引擎，默认“任意引擎” |
        
### 2）资源配置参数

| 参数 | 类型 | 样例 | 必须 | 默认值 | 说明 |
| ---- | ---- | ---- | ---- | ------ | ---- |
|      |      |      |      |        |      |