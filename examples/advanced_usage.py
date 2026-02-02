"""
高级使用示例

演示 markdown-to-wechat 的高级功能。
"""

from markdown_to_wechat import MarkdownToWeChatConverter, PreviewGenerator
from markdown_to_wechat.config import TITLE_PREFIX_TO_REMOVE


def example_custom_css():
    """自定义 CSS 示例"""
    print("=== 自定义 CSS 示例 ===\n")

    # 初始化转换器
    converter = MarkdownToWeChatConverter()

    # 自定义 CSS
    custom_css = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        line-height: 2.0;
        color: #333;
    }

    h1 {
        color: #ff6b6b;
        border-bottom: 3px solid #ff6b6b;
    }

    .highlight-box {
        background-color: #f0f8ff;
        border: 2px solid #4169e1;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
</style>
"""

    # 替换默认 CSS
    converter.css_styles = custom_css

    # 使用自定义 CSS 转换
    markdown = "# 自定义样式标题\n\n这是使用自定义样式的示例。"
    html_content = converter.convert(markdown)

    # 保存
    with open('custom_css_output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("已使用自定义 CSS 生成: custom_css_output.html")
    print()


def example_custom_title_prefix():
    """自定义标题前缀示例"""
    print("=== 自定义标题前缀示例 ===\n")

    # 读取默认配置
    print(f"默认标题前缀: '{TITLE_PREFIX_TO_REMOVE}'")

    # 创建带有前缀的 Markdown
    markdown = """
# 目前技术趋势

## 目前市场分析

这是分析当前技术趋势的文章。
"""

    converter = MarkdownToWeChatConverter()

    # 提取标题（会自动移除"目前"前缀）
    title = converter.extract_title(markdown)
    print(f"提取的标题: '{title}'")

    # 转换
    html_content = converter.convert(markdown)

    # 保存
    with open('custom_prefix_output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("已处理标题前缀: custom_prefix_output.html")
    print()


def example_batch_conversion():
    """批量转换示例"""
    print("=== 批量转换示例 ===\n")

    # 初始化转换器
    converter = MarkdownToWeChatConverter()

    # 准备多个 Markdown 文件
    files = [
        ('article1.md', '# 文章 1\n\n这是第一篇文章。'),
        ('article2.md', '# 文章 2\n\n这是第二篇文章。'),
        ('article3.md', '# 文章 3\n\n这是第三篇文章。')
    ]

    # 创建文件
    for filename, content in files:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    # 批量转换
    for markdown_file, _ in files:
        output_file = markdown_file.replace('.md', '.html')
        try:
            converter.convert_file(markdown_file, output_file)
            print(f"✅ {markdown_file} -> {output_file}")
        except Exception as e:
            print(f"❌ {markdown_file} 转换失败: {e}")

    print()


def example_error_handling():
    """错误处理示例"""
    print("=== 错误处理示例 ===\n")

    converter = MarkdownToWeChatConverter()

    # 尝试转换不存在的文件
    try:
        converter.convert_file('nonexistent.md')
    except FileNotFoundError as e:
        print(f"捕获到文件不存在错误: {e}")

    # 尝试生成预览但不存在的模板
    generator = PreviewGenerator()
    try:
        # 注意：这会失败，因为模板不存在
        html = converter.convert('# Test')
        preview = generator.generate_preview(
            markdown_text='# Test',
            html_content=html,
            title='Test',
            output_file='test.html',
            split=False
        )
    except FileNotFoundError as e:
        print(f"捕获到模板文件不存在错误: {e}")

    print()


def example_complex_document():
    """复杂文档示例"""
    print("=== 复杂文档示例 ===\n")

    converter = MarkdownToWeChatConverter()

    # 创建复杂的 Markdown 文档
    complex_markdown = """
# 技术文档完整示例

## 1. 简介

本文档展示 markdown-to-wechat 的所有功能。

## 2. 文本格式

### 2.1 强调文本

- **粗体文本** 用于强调
- *斜体文本* 用于标记
- `行内代码` 用于代码片段

### 2.2 链接

访问 [GitHub](https://github.com) 或 [官方网站](https://example.com)。

## 3. 列表

### 3.1 无序列表

- 项目 A
- 项目 B
  - 子项目 B.1
  - 子项目 B.2
- 项目 C

### 3.2 有序列表

1. 第一步
2. 第二步
3. 第三步

## 4. 代码

### 4.1 行内代码

这是一个 `inline code` 示例。

### 4.2 代码块

```python
def complex_function(param1, param2):
    """
    这是一个复杂的函数。

    Args:
        param1: 第一个参数
        param2: 第二个参数

    Returns:
        返回值
    """
    result = param1 + param2
    return result
```

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}
```

## 5. 引用

> 这是一段引用文本。
>
> 可以包含多个段落。

## 6. 表格

| 姓名 | 年龄 | 职业 |
|------|------|------|
| 张三 | 25 | 工程师 |
| 李四 | 30 | 设计师 |
| 王五 | 28 | 产品经理 |

## 7. 分隔线

---

## 8. 结论

这就是一个完整的技术文档示例。
"""

    # 转换复杂文档
    html_content = converter.convert(complex_markdown)

    # 生成预览
    generator = PreviewGenerator()
    preview = generator.generate_preview(
        markdown_text=complex_markdown,
        html_content=html_content,
        title='技术文档完整示例',
        output_file='complex_document_preview.html',
        split=True
    )

    print("复杂文档预览已生成: complex_document_preview.html")
    print()


if __name__ == '__main__':
    # 运行所有高级示例
    example_custom_css()
    example_custom_title_prefix()
    example_batch_conversion()
    example_error_handling()
    example_complex_document()

    print("所有高级示例运行完成！")
