# APP文档帮助文档（AliyunWAF)

## 一、APP介绍

<!--产品描述（从官网下载），给对接的产品顺便打个广告-->

Web应用防火墙（WAF）对网站或者APP的业务流量进行恶意特征识别及防护，将正常、安全的流量回源到服务器。避免网站服务器被恶意入侵，保障业务的核心数据安全，解决因恶意攻击导致的服务器性能异常问题。
注意，需要 pip install alibabacloud_waf_openapi20190910==1.1.8

| 内容         | 详细描述       |
| ------------ | -------------- |
| app版本      | 1.0.0          |
| 发布时间     | 2021-07-20   |
| 应用连接方式 |    API     |
| 支持版本     | API版本2019-09-10  |
| API文档   |   https://next.api.aliyun.com/document/waf-openapi/2019-09-10/overview |
| 作者         |  wuzhi       |


## 二、app使用注意事项

1）APP已测试通过型号&版本

| 型号      | 软件版本       |
| ------------ | -------------- |
|    Web应用防火墙（企业版）  |    API版本2019-09-10   |

2）注意

目前依赖库：
> pip install aliyun-python-sdk-core        2.13.35

> pip install aliyun-python-sdk-waf-openapi     1.1.5

3）报错原因
1. 如在健康检查——获取实例ID时失败，请先确认SID及SKEY是否正确
   
2. 如提示未购买或未开通WAF，确认账户拥有waf时，请确认下资源设置里的service_address、domain_id参数，注意要区分海内外(链接左上角有服务地域)：
   > https://next.api.aliyun.com/api/waf-openapi/2019-09-10/DescribeInstanceInfo?params={}
   



## 三、动作说明

###  

### 1）通用入参说明

**入参说明**

| 参数         | 类型   | 数据样例                 | 必须 | 默认值 | 说明                                              |
| ------------ | -------- | ------------------------ | ---- | ------ | ------------------------------------------------- |
| domain         |  字符串  | www.example.com   | 是   |      |  已添加的域名名称，网站域名必须已经接入WAF进行防护  |
| DefenseType           |  字符串  |   waf  | 是   |    waf   |  防护功能模块  |
| whileip /blackip           |  字符串  | 1.1.1.1,2.2.2.2,3.3.3.3  | 是   |      |需加名单的IP |


**出参说明**

| 参数                          | 类型   | 数据样例                       | 默认值 | 说明         |
| action_result.data.source_data | 字符串   |         {"RequestId":"23105791-0776-4B64-91FF-62C1B52694D4","InstanceInfo":{"PayType":0}}       |     |   接口源始数据      |




## 三、资源配置说明（此APP当前版本暂时无需配置资源）

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
| service_address | 字符串| cloudfw.aliyuncs.com  | 是   |    cloudfw.aliyuncs.com    | 服务地址 |
| domain_id | 字符串| cn-beijing  | 是   |    cloudfw.aliyuncs.com    |  区域ID |
| accesskey_id | 字符串| LTAI5tRC***EmZ11 | 是   |      | 访问ID |
| accesskey_secret | 字符串| c9QReGE8w***5hXvrLpflHwaKcXN  | 是   |       | 访问密钥 |
| InstanceId | 字符串| waf-cn-xxxxx1k  | 是   |       | 实例ID/名称，可从【控制台】-【费用】-【订单】-【我的订单】进入到对应的订单详情查看，例如：web应用防火墙(包月)，实例名称：xxx |


