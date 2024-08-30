# 变量生成器

- Version: 1.0.1
- author: [wzfukui](https://github.com/wzfukui)
- created: Oct 29,2023
- udpated: Aug 27,2024

# 使用说明

给定一个输入：`in_变量01`，就会得到一个对应的输出`ov_变量01`。用户也可以在输入变量上使用函数，最终完成输出变量的生成。

当你希望在某个节点执行前，先做一些变量的准备，可以使用变量生成器帮你一次性准备好。例如，在HTTP Client请求前，通过变量生成器组织HTTP头参数以及签名结果，之后提交HTTP Client发起请求。

默认提供：
- 6个string及标签
- 3个int及标签
- 2个long及标签
- 2个double及标签
- 1个boolean及标签
- 1个jsonarry及标签
- 1个jsonobject及标签

## Relese Notes
- 2023-10-29 发布1.0.0版本
- 2024-08-27 发布1.0.1版本，支持long、jsonobject和jsonarray类型变量，修改变量获取方式