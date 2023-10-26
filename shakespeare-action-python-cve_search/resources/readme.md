# 应用名:cve_search
## 应用简介:cve信息获取
数据源：Red Hat Security Data [链接](https://access.redhat.com/documentation/en-us/red_hat_security_data_api/1.0/html/red_hat_security_data_api/index)

需要有访问外网的权限（访问https://access.redhat.com/）
### get_cve
#### 获取cve信息
#### 入参说明
|参数名字|参数说明|参数类型|参数是否必须|
|:--- |:--- |:--- |:--- |
|before |查询日期之前的CVE。[ISO 8601为预期格式] 例 2016-03-01 |string |否 |
|after |查询日期之后的CVE。[ISO 8601为预期格式] 例 2016-02-01，默认为当前的前一天 |string |否 |
|ids |用逗号分隔的ID的CVE 例 CVE-2017-8797,CVE-2014-0161 |string |否 |
|severity |严重性 low,moderate,important |string |否 |
|package |cve影响的包，多个使用英文逗号分隔。例nginx,redis |string |否 |
|product |影响的产品，该参数支持Perl兼容的正则表达式，多个英文逗号分隔，例 openstack,linux |string |否 |
|cvss_score |CVSS得分大于或等于该值的CVE，例 7.0 |string |否 |
|cvss3_score |CVSSv3得分大于或等于此值的CVE 例 7.0 |string |否 |
|page |分页，页数 |integer |否 |
|per_page |分页大小 |integer |否 |
#### 返回说明
|返回名称|说明|返回值类型|
|:--- |:--- |:--- |
|data.records.*.CVE |cve |string |
|data.records.*.severity |severity |string |
|data.records.*.public_date |public_date |string |
|data.records.*.advisories |advisories |jsonarray |
|data.records.*.bugzilla |bugzilla |string |
|data.records.*.bugzilla_description |bugzilla_description |string |
|data.records.*.cvss_score |cvss_score |string |
|data.records.*.cvss_scoring_vector |cvss_scoring_vector |string |
|data.records.*.CWE |CWE |string |
|data.records.*.affected_packages |affected_packages |jsonarray |
|data.records.*.resource_url |resource_url |string |
|data.records.*.cvss3_scoring_vector |cvss3_scoring_vector |string |
|data.records.*.cvss3_score |cvss3_score |string |
### get_cve_details
#### 检索完整的CVE详细信息
#### 入参说明
|参数名字|参数说明|参数类型|参数是否必须|
|:--- |:--- |:--- |:--- |
|id |cve id 例 CVE-2016-3706 |string |是 |
#### 返回说明
|返回名称|说明|返回值类型|
|:--- |:--- |:--- |
|data.threat_severity |threat_severity |string |
|data.public_date |public_date |string |
|data.bugzilla |bugzilla |jsonobject |
|data.cvss3 |cvss3 |jsonobject |
|data.cwe |cwe |string |
|data.details |details |string |
|data.affected_release |affected_release |jsonarray |
|data.package_state |package_state |jsonarray |
|data.upstream_fix |upstream_fix |string |
|data.references |references |string |
|data.name |name |string |
|data.csaw |csaw |boolean |