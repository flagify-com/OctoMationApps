- 开发人员：heng.zhang@cloudfall.cn
- 发布时间：2024.02.29

# 应用配置

- url: 防火墙地址，格式为 http[s]://IP地址或域名:port
- api_key: 具有访问防火墙 API 权限的 API Key，参考 [链接](https://docs.paloaltonetworks.com/pan-os/9-0/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key)

# 动作说明

## block_ip
### 功能
通过 Palo Alto NGFW API 标记 IP，被标记的 IP 会自动进入到动态地址组（Dynamic Address Group），动态地址组会被用于防火墙策略，从而实现自动封禁 IP。

Palo Alto NGFW 自动封禁 IP 流程可以参考 [链接](https://pan.dev/panos/docs/tutorials/automating-ip-blocking/)。

### 参数
- ip：需要查询的 IP 地址  
- ip_tag: IP 标签，上述链接里 Step 1: Create a Dynamic Address Group Address Group 中的 match 内容
