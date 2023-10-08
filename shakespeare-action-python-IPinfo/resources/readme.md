# IPinfo——IP地理位置数据库

## 基本信息

- 版本：1.0.0
- 开发者：chris
- 发布时间：2023-10-05
- 运行依赖：互联网

> IPinfo.io, The trusted source for IP address data Accurate IP address data that keeps pace with secure, specific, and forward-looking use cases.

## 应用配置说明

- **官方网站**：https://ipinfo.io
- **API Token获取方式**：https://ipinfo.io/account/token
- **API文档**：https://ipinfo.io/developers/data-types#geolocation-data

## 动作说明

### **ip_geolocation**：查询IP地址的地理位置

通过ipinfo.io的接口查询给定IP地址（IPv4或IPv6）的Geo位置信息。主要包括：国家、地区、城市、坐标、组织、邮编、时区等。

> 注意：有些字段可能没有数据，默认为空，如：127.0.0.1没有国家信息。

**入参示例：**
```json
{
    "ip": "8.8.8.8"
}

```

**输出示例：**

```json
{
  "code": 200,
  "msg": "",
  "data": {
    "ip": "8.8.8.8",
    "city": "Mountain View",
    "region": "California",
    "country": "US",
    "loc": "37.4056,-122.0775",
    "org": "AS15169 Google LLC",
    "timezone": "",
    "postal": "America/Los_Angeles"
  }
}
```


## Change History
- 2023-10-05 V1.0.0, Init


