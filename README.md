# Markdown to WeChat

将 Markdown 转换为微信公众号兼容的 HTML 格式，支持丰富的样式和预览功能。

## ✨ 特性

- 📝 **完整 Markdown 支持**：标题、列表、代码块、表格、引用等
- 🎨 **微信优化样式**：内联 CSS 样式，完美适配微信公众号编辑器
- 📱 **响应式设计**：自动适配移动端和桌面端
- 🖼️ **分屏预览**：支持 Markdown 和 HTML 并排对比预览
- 🚀 **命令行工具**：简单易用的 CLI，支持批量转换
- 🔧 **Python API**：可编程接口，轻松集成到你的工作流
- 🔒 **安全可靠**：HTML 转义防止 XSS 攻击

## 📦 安装

### 使用 pip 安装

```bash
pip install markdown-to-wechat
```

### 从源码安装

```bash
git clone https://github.com/yourusername/markdown-to-wechat.git
cd markdown-to-wechat
pip install -e .
```

### 可选依赖

为了更好的 Markdown 转换质量，建议安装 `markdown` 库：

```bash
pip install markdown
```

## 🚀 快速开始

### 命令行使用

#### 基本转换

```bash
# 将 Markdown 文件转换为 HTML
markdown-to-wechat article.md article.html

# 查看转换结果
open article.html
```

#### 生成分屏预览

```bash
# 生成包含 Markdown 和 HTML 的分屏预览
markdown-to-wechat article.md preview.html --split

# 或使用简写
markdown-to-wechat article.md preview.html -s
```

#### 输出到标准输出

```bash
# 不指定输出文件，结果输出到终端
markdown-to-wechat article.md
```

#### 不包含 CSS

```bash
# 只输出 HTML，不包含样式
markdown-to-wechat article.md output.html --no-css
```

### Python API 使用

#### 基本转换

```python
from markdown_to_wechat import MarkdownToWeChatConverter

# 初始化转换器
converter = MarkdownToWeChatConverter()

# 转换 Markdown 文本
markdown_text = """
# 欢迎使用

这是一个 **Markdown** 示例。

- 列表项 1
- 列表项 2

```python
print('Hello, WeChat!')
```
"""

html_content = converter.convert(markdown_text)

# 保存到文件
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
```

#### 转换文件

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()

# 转换文件
html_content = converter.convert_file(
    'input.md',
    'output.html',
    include_css=True
)

print(f"转换成功！")
```

#### 生成分屏预览

```python
from markdown_to_wechat import MarkdownToWeChatConverter, PreviewGenerator

# 转换 Markdown
converter = MarkdownToWeChatConverter()
html_content = converter.convert_file('article.md')

# 生成分屏预览
preview_generator = PreviewGenerator()
preview_html = preview_generator.generate_from_file(
    'article.md',
    html_content,
    output_file='preview.html',
    split=True
)
```

## 📖 Markdown 支持

本项目支持以下 Markdown 元素：

### 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 文本格式

```markdown
**粗体文本**
*斜体文本*
`行内代码`
[链接文本](https://example.com)
```

### 列表

```markdown
- 无序列表项 1
- 无序列表项 2

1. 有序列表项 1
2. 有序列表项 2
```

### 代码块

```markdown
```python
def hello():
    print('Hello, WeChat!')
```
```

### 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |
```

### 引用

```markdown
> 这是一段引用文本
```

### 分隔线

```markdown
---
```

## 🎯 使用场景

- **微信公众号运营**：将 Markdown 技术文档转换为微信富文本
- **技术博客**：编写博客文章，一键转换发布
- **文档编写**：编写产品文档，生成友好的预览界面
- **自动化发布**：集成到 CI/CD 流程，自动转换和发布

## 🔧 配置选项

### 自定义 CSS

如果需要自定义样式，可以修改转换器的 CSS：

```python
from markdown_to_wechat import MarkdownToWeChatConverter

converter = MarkdownToWeChatConverter()
converter.css_styles = """
<style>
    /* 自定义样式 */
    body {
        font-family: 'Your Font', sans-serif;
        line-height: 2.0;
    }
</style>
"""
```

### 标题前缀处理

默认会自动移除标题中的"目前"前缀，可以通过修改配置改变：

```python
from markdown_to_wechat.config import TITLE_PREFIX_TO_REMOVE

# 修改要移除的前缀
TITLE_PREFIX_TO_REMOVE = '自定义前缀'
```

## 📚 API 文档

详细的 API 文档请参考 [API 文档](docs/api.md)

## 🤝 贡献

欢迎贡献代码！请参考 [贡献指南](CONTRIBUTING.md)

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)

## 🙏 致谢

感谢所有为本项目做出贡献的开发者

## 📮 联系方式

- 作者：Your Name
- 邮箱：your.email@example.com
- GitHub：[https://github.com/yourusername/markdown-to-wechat](https://github.com/yourusername/markdown-to-wechat)

## 🐛 问题反馈

如果遇到问题或有功能建议，请在 [GitHub Issues](https://github.com/yourusername/markdown-to-wechat/issues) 中提交。

---

**享受使用 Markdown to WeChat！** 🎉
