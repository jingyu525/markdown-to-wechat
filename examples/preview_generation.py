"""
预览生成示例

演示如何使用 markdown-to-wechat 生成预览 HTML。
"""

from markdown_to_wechat import MarkdownToWeChatConverter, PreviewGenerator


def example_single_preview():
    """生成单页预览示例"""
    print("=== 单页预览示例 ===\n")

    # 初始化转换器和预览生成器
    converter = MarkdownToWeChatConverter()
    generator = PreviewGenerator()

    # 准备 Markdown 和 HTML 内容
    markdown_text = """
# 单页预览示例

这是一个简单的单页预览示例。

## 功能列表

- 美观的界面
- 一键复制功能
- 响应式设计
"""

    html_content = converter.convert(markdown_text)

    # 生成单页预览
    preview_html = generator.generate_preview(
        markdown_text=markdown_text,
        html_content=html_content,
        title='单页预览示例',
        output_file='single_preview.html',
        split=False
    )

    print("单页预览已生成: single_preview.html")
    print()


def example_split_preview():
    """生成分屏预览示例"""
    print("=== 分屏预览示例 ===\n")

    # 初始化转换器和预览生成器
    converter = MarkdownToWeChatConverter()
    generator = PreviewGenerator()

    # 准备 Markdown 和 HTML 内容
    markdown_text = """
# 分屏预览示例

左侧显示 Markdown 源码，右侧显示 HTML 预览。

## 特点

- 同步滚动
- 并排对比
- 方便查看转换效果
"""

    html_content = converter.convert(markdown_text)

    # 生成分屏预览
    preview_html = generator.generate_preview(
        markdown_text=markdown_text,
        html_content=html_content,
        title='分屏预览示例',
        output_file='split_preview.html',
        split=True
    )

    print("分屏预览已生成: split_preview.html")
    print()


def example_preview_from_file():
    """从文件生成预览示例"""
    print("=== 从文件生成预览示例 ===\n")

    # 创建示例 Markdown 文件
    sample_markdown = """# 从文件生成预览

这个示例演示如何从 Markdown 文件生成预览。

## 步骤

1. 创建 Markdown 文件
2. 转换为 HTML
3. 生成预览页面
4. 在浏览器中查看

## 代码

```python
converter = MarkdownToWeChatConverter()
html = converter.convert_file('input.md')
```"""

    with open('preview_input.md', 'w', encoding='utf-8') as f:
        f.write(sample_markdown)

    # 初始化转换器和预览生成器
    converter = MarkdownToWeChatConverter()
    generator = PreviewGenerator()

    # 从文件生成预览
    html_content = converter.convert_file('preview_input.md')

    # 生成分屏预览
    preview_html = generator.generate_from_file(
        markdown_file='preview_input.md',
        html_content=html_content,
        output_file='file_preview.html',
        split=True
    )

    print("从文件生成的预览已保存: file_preview.html")
    print()


def example_batch_preview():
    """批量生成预览示例"""
    print("=== 批量生成预览示例 ===\n")

    # 初始化转换器和预览生成器
    converter = MarkdownToWeChatConverter()
    generator = PreviewGenerator()

    # 准备多个文档
    documents = [
        {
            'title': '文档 1',
            'markdown': '# 文档 1\n\n这是第一个文档的内容。'
        },
        {
            'title': '文档 2',
            'markdown': '# 文档 2\n\n这是第二个文档的内容。'
        },
        {
            'title': '文档 3',
            'markdown': '# 文档 3\n\n这是第三个文档的内容。'
        }
    ]

    # 批量生成预览
    for idx, doc in enumerate(documents, 1):
        html_content = converter.convert(doc['markdown'])

        # 生成预览
        output_file = f'batch_preview_{idx}.html'
        generator.generate_preview(
            markdown_text=doc['markdown'],
            html_content=html_content,
            title=doc['title'],
            output_file=output_file,
            split=False
        )

        print(f"已生成: {output_file}")

    print(f"\n批量生成完成，共 {len(documents)} 个文档")
    print()


if __name__ == '__main__':
    # 运行所有示例
    example_single_preview()
    example_split_preview()
    example_preview_from_file()
    example_batch_preview()

    print("所有预览示例运行完成！")
    print("\n提示：在浏览器中打开生成的 HTML 文件查看预览效果。")
