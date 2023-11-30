# 应用名:nvd_cve
## 应用简介:cve数据获取
数据源：NATIONAL VULNERABILITY DATABASE [链接](https://nvd.nist.gov/developers/vulnerabilities)

需要有访问外网的权限（访问https://nvd.nist.gov/developers/vulnerabilities）
### health_check
#### 健康检查
#### 入参说明
|参数名字|参数说明|参数类型|参数是否必须|
|:--- |:--- |:--- |:--- |

#### 返回说明
|返回名称|说明|返回值类型|
|:--- |:--- |:--- |
|summary.msg |msg健康检查信息 |string |
|summary.statusCode |状态码200正常 |integer |
### get_cve
#### 获取指定时间段内某个产品的cve数据
#### 入参说明
|参数名字|参数说明|参数类型|参数是否必须|
|:--- |:--- |:--- |:--- |
|keywordSearch |产品名关键字，例如chrome |string |是 |
|pubStartDate | 查询漏洞公布日期范围，起始时间，默认为当前日期的前一天 |date |否 |
|pubEndDate | 查询漏洞公布日期范围，截止时间，默认为今天 | date |是 |
|cvssV3Severity |严重等级，默认获取所有等级的数据 |string | 否 |
|resultsPerPage | 分页参数，每页多少条数据，默认为10 |integer |否 |
|startIndex |分页起始值，默认从0开始 |integer |否 |

#### 返回说明
|返回名称|说明|返回值类型|
|:--- |:--- |:--- |
|data.records.*.cve_id | cve id |string |
|data.records.*.descriptions | 漏洞描述 |string |
|data.records.*.published |发布日期 |string |
|data.records.*.references |参考信息 |string |
|data.resultsPerPage |分页参数，每页大小 |integer |
|data.startIndex |分页参数，起始值 | integer |
|data.totalResults | 查询总数 | integer|