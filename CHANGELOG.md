# 变更日志

本文档记录了 markdown-to-wechat 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2025-02-01

### 新增
- 初始版本发布
- 完整的 Markdown 到 HTML 转换支持
- 微信公众号兼容的样式优化
- 命令行工具（CLI）
- Python API 接口
- 单页预览功能
- 分屏对比预览功能
- 支持标题、列表、代码块、表格、引用等 Markdown 元素
- HTML 转义防止 XSS 攻击
- 内联 CSS 样式，确保微信编辑器兼容性
- 响应式设计，支持移动端和桌面端

### 安全
- 所有用户输入进行 HTML 转义
- 修复 XSS 安全漏洞

### 代码质量
- 使用 argparse 替代手动参数解析
- 消除重复代码，提高可维护性
- 添加类型注解和文档字符串
- 遵循 PEP 8 代码规范

### 文档
- 完整的 README.md
- 详细的贡献指南
- API 文档
- 使用示例代码

## [未来版本]

### 计划中
- 支持自定义主题
- 更多 Markdown 扩展
- 批量文件转换
- 图表支持（Mermaid）
- 更多预览模板
- 插件系统

---

[1.0.0]: https://github.com/yourusername/markdown-to-wechat/releases/tag/v1.0.0
