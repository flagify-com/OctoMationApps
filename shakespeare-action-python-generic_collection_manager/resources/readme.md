# Generic_Collection_Manager通用集合管理工具

[toc]

## 一、APP介绍

通用集合管理工具，用于管理编排自动化系统中通用集合，包括功能：
- 列举集合名称及元素
- 创建和删除集合
- 创建、删除、修改集合元素

**各类操作均为原子化操作，涉及到批量处理、判断元素是否在集合中等需求，建议通过剧本中规则节点的判断逻辑实现。**


| 内容      | 详细描述       |
|:--------|:-----------|
| app上次版本 | 2.0.0      |
| app更新版本 | 2.0.1      |
| 发布时间    | 2022-12-20 |
| 更新时间    | 2024-08-26 |
| 原开发者     | S*B        |
| 更新人     | [wzfukui](https://github.com/wzfukui)   |
| 对接方式  | API |
| 开发语言    |  Python 3.6+  |
| 更新地址 |[flagify-com/OctoMationApps](https://github.com/flagify-com/OctoMationApps)|

## 二、APP使用注意事项


1）**发布或修改记录**

| 更新时间       | 更新记录                                    | 更新人| 更新版本  |
|------------|-----------------------------------------|----|-------|
| 2022-12-20 | APP发布（Python版）                          |tput -S'：确认SSH客户端通道row、col信息：| S*B   | 1.1.0 |
| 2023-06-09 | 元素新增或覆盖动作添加生效时间参数逻辑；过期时间逻辑调整            | Han | 1.6.0 |
| 2023-07-04 | 向指定集合添加元素动作：修复添加url字符元素问题；捕获接口原报错信息输出   | Han | 1.6.1 |
| 2024-03-21 | db_util文件get_db函数修改SDK取Mysql连接信息 | Han | 1.6.1 |
| 2024-05-29 | 向指定集合添加元素动作：修复通用集合修改已存在元素备注字段问题         | Han | 1.6.2 |
| 2024-06-20 | 修改【判断元素存在于指定通用集合中】动作：输出渲染               | Han | 1.6.4 |
| 2024-07-27 | 添加集合元素时，结果中增加duplicated，表示是否有重复元素               | wzfukui | 1.6.5 |
| 2024-08-19 | 修复IP子网掩码方式，API报格式错误的问题               | wzfukui | 1.6.6 |
| 2024-08-26 | 废弃MySQL连接方式，纯API对接，降低依赖，删除不必要的功能（批量、导出excel）    | wzfukui | 2.0.0 |

2）**API使用说明**
- 列举集合所有元素，会因为元素过多而耗费大量时间，不宜高频使用，即使使用，也建议使用异步动作完成
- 所有功能是通过API接口方式完成的，速度和效率上肯定部署直接数据库操作。但因为集合操作除了涉及到数据库同步，还涉及到zk信息同步，因此并发不要太高，如有必要可以在前面节点，随机Sleep。
- IP地址集合是另一种高性能集合，为保证应用功能聚焦和稳定性，由单独的APP实现，
- **创建一个已经存在的集合/元素，默认返回为0， 创建成功**
- **删除一个不存在集合/元素元，默认返回为0， 删除成功**

## 三、资源配置说明 

| 参数 | 类型 | 样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:-----|:-----|:-----|:-----|
| hg_host | 字符串 | | 是 | | API 服务器URL，例https://192.168.1.1 |
| hg_token | password | | 是 | | API Token，通过系统设置界面生成API Token |
| conn_time_out | 整数 | | 是 | 10 | 请求API服务连接时间超时，单位：秒 |



## 四、动作说明

### list_generic_collections

**描述**：集合_返回所有通用集合名单列表

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| batch_size | 整数 | | 否 | 30 | API每页批次返回数量 |
| max_count | 整数 | | 否 | 200 | 最大返回数量 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.collections | JSON数组 | | | 所有集合的属性及元素情况，组成的数组 |
| action_result.data.collections.*.id | 整数 | | | 集合的ID号 |
| action_result.data.collections.*.name | 字符串 | | | 集合名称 |
| action_result.data.collections.*.cnName | 字符串 | | | 集合中文名 |
| action_result.data.collections.*.description | 字符串 | | | 集合描述 |
| action_result.data.collections.*.num | 整数 | | | 集合元素数量 |
| action_result.data.collections.*.createTime | 字符串 | | | 集合创建时间 |
| action_result.data.count | 整数 | | | 本次查询到的集合总数量 |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### create_generic_collection

**描述**：集合_创建一个通用集合

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_name | 字符串 | | 是 | | 集合的名称，仅支持：英文/数字/下划线，最长64字符 |
| collection_cnname | 字符串 | | 是 | | 集合的中文名称，最长64字符 |
| collection_description | 字符串 | | 否 | | 集合的描述信息，最长64字符 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.element_id | 整数 | | | 集合ID号（数字） |
| action_result.data.duplicated | 布尔值 | | | 集合创建前是否已经存在 |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |


### delete_generic_collection

**描述**：集合_删除一个通用集合

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_id | 整数 | | 否 | | 集合的ID号，一长串数字，如：11268278432702172 |
| collection_name | 字符串 | | 否 | | 集合名称（集合ID与集合名称，两者不能同时为空） |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### list_generic_collection_items

**描述**：集合_返回指定集合的元素列表（耗时，不建议在剧本中直接使用，建议使用异步动作执行）

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_id | 整数 | | 否 | | 集合ID号，一长串数字，如：1126827843270217 |
| collection_name | 字符串 | | 否 | | 集合名称，例：BLACKLIST，集合名称与ID不能同时为空 |
| batch_size | 整数 | | 否 | 30 | API每页批次返回数量 |
| max_count | 整数 | | 否 | 200 | 最大返回数量 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.elements | JSON数组 | | | 所有元素的信息，组成的数组 |
| action_result.data.elements.*.id | 整数 | | | 元素的ID号 |
| action_result.data.elements.*.value | 字符串 | | | 元素的值 |
| action_result.data.elements.*.remark | 字符串 | | | 元素的备注 |
| action_result.data.elements.*.collectionId | 整数 | | | 元素所在集合的ID号 |
| action_result.data.elements.*.collectionName | 字符串 | | | 元素所在集合的名称 |
| action_result.data.elements.*.createTime | 字符串 | | | 元素创建时间 |
| action_result.data.elements.*.updateTime | 字符串 | | | 元素更新时间 |
| action_result.data.count | 整数 | | | 本次查询到的元素总数量 |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### get_generic_collection_element_info

**描述**：元素_获取集合中指定元素的信息

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_id | 整数 | | 否 | | 集合ID号，一长串数字，如：1126827843270217 |
| collection_name | 字符串 | | 否 | | 集合名称，例：BLACKLIST，集合名称与ID不能同时为空 |
| element_value | 字符串 | | 是 | | 元素的值（精准匹配） |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.id | 整数 | | | 元素的ID号 |
| action_result.data.value | 字符串 | | | 元素的值 |
| action_result.data.remark | 字符串 | | | 元素的备注 |
| action_result.data.collectionId | 整数 | | | 元素的所在集合ID |
| action_result.data.collectionName | 字符串 | | | 元素的所在集合名 |
| action_result.data.createTime | 字符串 | | | 元素的创建时间 |
| action_result.data.updateTime | 字符串 | | | 元素的更新时间 |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |


### add_generic_collection_item

**描述**：元素_向通用集合添加元素

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_name | 字符串 | | 是 | | 集合名称，例：BLACKLIST |
| element_value | 字符串 | | 是 | | 元素值 |
| element_remark | 字符串 | | 否 | | 元素备注 |
| update_if_exist | 布尔值 | | 否 | false | 元素已经存在时，是否强制更新备注 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.duplicated | 布尔值 | | false | 元素是否已经存在 |
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### update_generic_collection_element

**描述**：元素_更新集合元素信息（备注）

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_name | 字符串 | | 是 | | 集合名称，例：BLACKLIST |
| element_value | 字符串 | | 是 | | 元素的值，元素ID和值不能同时为空 |
| element_remark | 字符串 | | 是 | | 元素备注 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.summary.statusCode | 整数 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### delete_generic_collection_element

**描述**：元素_从集合中删除元素

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_name | 字符串 | | 是 | | 集合名称，例：BLACKLIST，不能为空 |
| element_value | 字符串 | | 是 | | 元素的值，不能为空 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.summary.statusCode | 字符串 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### check_generic_collection_element_exists

**描述**：元素_判断元素在集合中是否存在

**入参说明**

| 参数 | 类型 | 数据样例 | 必须 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|:-----|
| collection_name | 字符串 | | 是 | | 集合名称，例：BLACKLIST，不能为空 |
| element_value | 字符串 | | 是 | | 元素的值，不能为空 |

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.data.element_exist | 布尔值 | | false | 元素是否存在 |
| action_result.summary.statusCode | 字符串 | | 0 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

### health_check

**描述**：健康检查

**入参说明**

此动作没有入参。

**出参说明**

| 参数 | 类型 | 数据样例 | 默认值 | 说明 |
|:-----|:-----|:---------|:-----|:-----|
| action_result.summary.statusCode | 字符串 | | 200 | 返回错误码 |
| action_result.summary.msg | 字符串 | | | 返回错误消息 |

