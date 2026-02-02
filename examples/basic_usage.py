"""
基本使用示例

演示如何使用 markdown-to-wechat 进行基本的 Markdown 到 HTML 转换。
"""

from markdown_to_wechat import MarkdownToWeChatConverter


def example_basic_conversion():
    """基本转换示例"""
    print("=== 基本转换示例 ===\n")

    # 初始化转换器
    converter = MarkdownToWeChatConverter()

    # 准备 Markdown 文本
    markdown_text = """
# 欢迎使用 Markdown to WeChat

这是一个 **Markdown** 转 *HTML* 的示例。

## 功能特性

- 完整的 Markdown 支持
- 微信公众号兼容的样式
- 响应式设计

## 代码示例

```python
def hello():
    print('Hello, WeChat!')
```

## 表格示例

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |

## 引用示例

> 这是一段引用文本，适合突出显示重要信息。
"""

    # 转换为 HTML
    html_content = converter.convert(markdown_text, include_css=True)

    # 输出结果（或保存到文件）
    print("转换完成！")
    print(f"HTML 长度: {len(html_content)} 字符")

    # 保存到文件
    with open('basic_output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("已保存到 basic_output.html")
    print()


def example_file_conversion():
    """文件转换示例"""
    print("=== 文件转换示例 ===\n")

    # 初始化转换器
    converter = MarkdownToWeChatConverter()

    # 转换文件
    html_content = converter.convert_file(
        'input.md',
        'file_output.html',
        include_css=True
    )

    print("文件转换完成！")
    print(f"输出文件: file_output.html")
    print()


def example_extract_title():
    """提取标题示例"""
    print("=== 提取标题示例 ===\n")

    converter = MarkdownToWeChatConverter()

    # 带标题的 Markdown
    markdown = """
# 微信公众号运营指南

本文介绍如何高效运营微信公众号。
"""

    # 提取标题
    title = converter.extract_title(markdown)

    print(f"提取的标题: {title}")
    print()


def example_without_css():
    """不包含 CSS 的转换示例"""
    print("=== 不包含 CSS 的转换示例 ===\n")

    converter = MarkdownToWeChatConverter()

    markdown = "# 简单标题\n\n内容"

    # 转换时不包含 CSS
    html_content = converter.convert(markdown, include_css=False)

    print("转换完成（无 CSS）")
    print(f"HTML 长度: {len(html_content)} 字符")
    print()


if __name__ == '__main__':
    # 创建一个示例 Markdown 文件
    sample_markdown = """# 示例文章

这是一个示例文章，用于演示 Markdown to WeChat 的基本功能。

## 主要功能

1. **标题支持** - 支持 h1 到 h6 标题
2. **列表支持** - 支持有序和无序列表
3. **代码高亮** - 支持代码块和行内代码
4. **表格支持** - 基本的表格渲染

## 代码示例

```python
def example():
    return 'Hello'
```

## 链接示例

访问 [官方网站](https://example.com) 了解更多信息。
"""

    with open('input.md', 'w', encoding='utf-8') as f:
        f.write(sample_markdown)

    print("已创建示例文件 input.md\n")

    # 运行所有示例
    example_basic_conversion()
    example_file_conversion()
    example_extract_title()
    example_without_css()

    print("所有示例运行完成！")
