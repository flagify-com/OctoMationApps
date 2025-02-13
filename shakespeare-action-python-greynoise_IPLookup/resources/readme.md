# Greynoise IP 查询应用

## **简介**
本应用是一个基于 Greynoise API 的工具，用于查询单个 IP 地址的相关信息（如是否为恶意 IP、分类等）。通过简单的接口调用，用户可以快速获取 IP 的上下文数据。

## **功能**
- 查询单个 IP 地址的 Greynoise 数据。
- 提供标准化的 JSON 响应格式，包含以下字段：
  - `ip`: 查询的 IP 地址。
  - `noise`: 是否为噪声流量（`true` 或 `false`）。
  - `classification`: IP 的分类（如 `benign`、`malicious` 等）。


## **使用方法**
需要提供 Greynoise API Token。
> **注意**：请从 [Greynoise 官网](https://greynoise.io/) 获取你的 API Token。

## **注意事项**

1. **API 限制**:
   - Greynoise 社区版 API 每分钟最多允许 10 次请求。如果需要更高的速率限制，请升级到付费版本。


4. **Greynoise 文档**:
   - 更多关于 Greynoise API 的信息，请参考官方文档：[Greynoise API 文档](https://docs.greynoise.io/reference/noisecontextip-1)。
