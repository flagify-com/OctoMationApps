# 活动列表ActiveList管理器

## 基本信息

- 项目名称：活动列表ActiveList管理器
- 项目描述：一个基于Python的活动列表管理器，可以帮助你管理你的信息记录，包括：添加、删除、统计、清空等
- 项目作者：[wzfukui](https://github.com/wzfukui)
- 项目版本：v1.1.4
- 项目语言：Python 3.6+

## 用途介绍

通过活动列表，你可以存储某一类型的活动的日志/记录，如：某个IP地址的工具记录。在此基础上，可以针对过往记录基于时间窗口进行统计。

典型应用场景：

- **IP地址封**：单个IP地址攻击次数，每4小时攻击次数大于3，则封禁该IP地址
- **攻击行为去重**：相同的“源地址+事件类型+严重度”作为一条记录保存，1天N次后，则直接拦截源地址，否则只告警

## 主要功能
  - ✅初始化活动列表：根据指定的活动列表名称，创建活动列表（本质上是在数据库中建了一个表）
  - ✅添加活动记录：item_name, item_value, item_remark，支持`覆盖更新`和`追加`两种方式
  - ✅清空活动列表：删除活动列表中的所有记录
  - ✅删除活动列表：彻底不再使用改活动列表，可能导致依赖该活动类表的剧本无法正常运行
  - ✅按照时间窗口统计某个key的活动记录数：输入key_name、截止时间（默认当前时间）、向前统计的时间窗口（单位：分钟），返回改时间窗口内所有key_name的活动记录数量
  - ✅列举所有活动列表：列举当前所有的活动列表名称
  - ✅活动列表查存：查询某个活动列表中某个key是否存在
  - ✅速览活动列表：查看活动列表中最近10条记录
  - ✅活动列表中记录行的趋势统计：支持按照天/时/分三个方式统计活动记录趋势

## 活动列表内容样例


| _key        | _value      | _remark | create_time | update_time | expire_time |
|-------------|-------------|-------------|-------------|-------------|-------------|
| 192.168.1.1 | SQL注入 | NULL | 2021-01-01 00:00:00 | 2021-01-01 00:00:00 | NULL |
| 192.168.1.2 | XSS | NULL | 2021-01-02 00:00:00 | 2021-01-02 00:00:00 | NULL |
| 192.168.1.3 | XSS | NULL | 2021-01-03 00:00:00 | 2021-01-03 00:00:00 | NULL |
| 192.168.1.2 | SQL注入 | NULL | 2021-01-03 00:00:00 | 2021-01-03 00:00:00 | NULL |

## 注意事项
- 需要运行在能够访问SOAR平台MySQL数据库的执行引擎上运行
- 目前版本还不支持MySQL SSL加密连接（因部分mysql.connector版本不支持）
- 使用活动列表之前，需要先初始化该列表
- 活动列表名称必须是没有空格的字符串，且只能包含字母、数字、下划线、中划线
- 项目中使用的MySQL数据库表（自动增加前缀`_al_`）结构设计为：
  - _key：活动列表名称，最大长度512，支持索引
  - _value：活动列表中某个key对应的value值，支持索引
  - _remark：活动列表中某个key对应的备注信息
  - create_time：记录行创建时间，支持索引
  - update_time：记录行修改时间，支持索引
  - expire_time：记录行过期时间（暂不支持，留待扩展）
- 事件去重剧本有类似的逻辑，但本APP更加通用，可能性能稍弱一点

## 数据库表结构

| Field       | Type         | Null | Key | Default           | Extra                       |
|-------------|--------------|------|-----|-------------------|----------|
| _key        | varchar(512) | YES  | MUL | NULL              |          |
| _value      | text         | YES  |     | NULL              |          |
| _remark     | text         | YES  |     | NULL              |          |
| create_time | datetime     | YES  | MUL | CURRENT_TIMESTAMP |          |
| update_time | datetime     | YES  | MUL | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| expire_time | datetime     | YES  |     | NULL              |          |

## 数据样例

### quick_view_active_list

```josn
{
  "msg": "",
  "code": 200,
  "data": {
    "records": [
      {
        "update_time": "2024-07-03 13:43:37",
        "create_time": "2024-07-03 13:43:37",
        "_remark": "",
        "_value": "7.7.7.7",
        "_key": "7.7.7.7"
      },
      {
        "update_time": "2024-07-03 13:43:31",
        "create_time": "2024-07-03 13:43:31",
        "_remark": "",
        "_value": "7.7.7.7",
        "_key": "7.7.7.7"
      },
      {
        "update_time": "2024-07-03 13:43:14",
        "create_time": "2024-07-03 13:43:14",
        "_remark": "",
        "_value": "7.7.7.7",
        "_key": "7.7.7.7"
      },
      {
        "update_time": "2024-07-03 13:08:37",
        "create_time": "2024-07-03 13:08:37",
        "_remark": "",
        "_value": "4.4.4.6",
        "_key": "4.4.4.6"
      },
      {
        "update_time": "2024-07-03 13:08:25",
        "create_time": "2024-07-03 13:08:25",
        "_remark": "",
        "_value": "4.4.4.5",
        "_key": "4.4.4.5"
      },
      {
        "update_time": "2024-07-03 13:08:10",
        "create_time": "2024-07-03 13:08:10",
        "_remark": "",
        "_value": "4.4.4.4",
        "_key": "4.4.4.4"
      },
      {
        "update_time": "2024-07-03 10:40:45",
        "create_time": "2024-07-03 10:40:45",
        "_remark": "",
        "_value": "4.4.4.4",
        "_key": "3.33.3.3"
      },
      {
        "update_time": "2024-07-03 10:32:46",
        "create_time": "2024-07-03 10:32:46",
        "_remark": "",
        "_value": "2.2.2.2",
        "_key": "2.2.2.2"
      },
      {
        "update_time": "2024-07-03 10:32:32",
        "create_time": "2024-07-03 10:32:32",
        "_remark": "",
        "_value": "1.1.1.1",
        "_key": "1.1.1.1"
      }
    ],
    "err_msg": "查询成功",
    "total_count": 9,
    "err_code": 0,
    "activelist_name": "attack"
  }
}
```

### get_records_time_trend

```json
{
  "msg": "",
  "code": 200,
  "data": {
    "records": [
      {
        "xTime": "0703_1308",
        "xCount": 3
      },
      {
        "xTime": "0703_1343",
        "xCount": 3
      }
    ],
    "err_msg": "查询成功",
    "total_count": 2,
    "err_code": 0,
    "activelist_name": "attack"
  }
}
```

## 依赖

- MySQL Connector：`pip install mysql-connector-python`

## Relese Notes
- 2024-06-02 v1.0.0 发布第一个版本
- 2024-07-03 v1.1.1 增加查存、统计和速览功能，部分动作增加渲染
- 2024-07-03 v1.1.2 修改readme错别字
- 2024-07-26 v1.1.3 增加_value索引，优化建表语句
- 2024-07-27 v1.1.4 移除exists检查，修改时间趋势动作名称