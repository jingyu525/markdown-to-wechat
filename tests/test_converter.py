"""Unit tests for converter module."""

import pytest
from pathlib import Path
from markdown_to_wechat import MarkdownToWeChatConverter


class TestMarkdownToWeChatConverter:
    """Test cases for MarkdownToWeChatConverter."""

    def test_converter_initialization(self):
        """Test that converter can be initialized."""
        converter = MarkdownToWeChatConverter()
        assert converter is not None
        assert converter.css_styles is not None

    def test_basic_heading_conversion(self):
        """Test basic heading conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '# Heading 1'
        html = converter.convert(markdown)
        assert '<h1' in html
        assert 'Heading 1' in html

    def test_multiple_headings(self):
        """Test conversion of multiple heading levels."""
        converter = MarkdownToWeChatConverter()
        markdown = '''# H1
## H2
### H3
#### H4
##### H5
###### H6'''
        html = converter.convert(markdown)
        assert '<h1' in html
        assert '<h2' in html
        assert '<h3' in html
        assert '<h4' in html
        assert '<h5' in html
        assert '<h6' in html

    def test_bold_and_italic(self):
        """Test bold and italic text conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '**bold** and *italic*'
        html = converter.convert(markdown)
        assert '<strong' in html or '<b' in html
        assert '<em' in html or '<i' in html
        assert 'bold' in html
        assert 'italic' in html

    def test_list_conversion(self):
        """Test list conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '''- Item 1
- Item 2
- Item 3'''
        html = converter.convert(markdown)
        assert '<ul' in html
        assert '<li' in html
        assert 'Item 1' in html
        assert 'Item 2' in html
        assert 'Item 3' in html

    def test_ordered_list(self):
        """Test ordered list conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '''1. First
2. Second
3. Third'''
        html = converter.convert(markdown)
        assert '<ol' in html
        assert '<li' in html

    def test_code_block(self):
        """Test code block conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '''```python
print('Hello')
```'''
        html = converter.convert(markdown)
        assert '<pre' in html
        assert '<code' in html
        assert 'print' in html

    def test_inline_code(self):
        """Test inline code conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = 'This is `code`'
        html = converter.convert(markdown)
        assert '<code' in html
        assert 'code' in html

    def test_link_conversion(self):
        """Test link conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '[Link text](https://example.com)'
        html = converter.convert(markdown)
        assert '<a' in html
        assert 'href="https://example.com"' in html or "href='https://example.com'" in html
        assert 'Link text' in html

    def test_blockquote(self):
        """Test blockquote conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '> This is a quote'
        html = converter.convert(markdown)
        assert '<blockquote' in html
        assert 'This is a quote' in html

    def test_multiline_blockquote(self):
        """Test multi-line blockquote conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '''> Line 1
>
> Line 2
>
> Line 3'''
        html = converter.convert(markdown, include_css=False)
        assert '<blockquote' in html
        assert html.count('<blockquote') == 1
        assert 'Line 1' in html
        assert 'Line 2' in html
        assert 'Line 3' in html

    def test_blockquote_with_empty_lines(self):
        """Test blockquote with empty lines between paragraphs."""
        converter = MarkdownToWeChatConverter()
        markdown = '''> First paragraph
>
> Second paragraph'''
        html = converter.convert(markdown, include_css=False)
        assert '<blockquote' in html
        assert html.count('<blockquote') == 1
        assert html.count('<p') >= 2

    def test_single_vs_multiline_blockquote(self):
        """Test that single and multi-line blockquotes work correctly."""
        converter = MarkdownToWeChatConverter()
        markdown_single = '> Single quote'
        html_single = converter.convert(markdown_single, include_css=False)
        assert html_single.count('<blockquote') == 1
        
        markdown_multi = '''> Line 1
> Line 2'''
        html_multi = converter.convert(markdown_multi, include_css=False)
        assert html_multi.count('<blockquote') == 1

    def test_blockquote_hard_line_break(self):
        """Test blockquote with hard line breaks (trailing two spaces)."""
        converter = MarkdownToWeChatConverter()
        markdown = '''> **适合人群**：希望深度定制 OpenClaw 的开发者 / 想构建自己工具链的产品经理  
> **阅读时长**：约 18 分钟  
> **前置条件**：熟悉 OpenClaw 基础操作，了解 YAML 格式，有基础 CLI 使用经验'''
        html = converter.convert(markdown, include_css=False)
        assert '<blockquote' in html
        assert html.count('<blockquote') == 1
        assert '<br>' in html
        assert '适合人群' in html
        assert '阅读时长' in html
        assert '前置条件' in html

    def test_blockquote_hard_line_break_mixed(self):
        """Test blockquote with mixed hard breaks and paragraph breaks."""
        converter = MarkdownToWeChatConverter()
        markdown = '''> Line 1 with break  
> Line 2 with break  
> Line 3
>
> New paragraph'''
        html = converter.convert(markdown, include_css=False)
        assert '<blockquote' in html
        assert html.count('<blockquote') == 1
        assert '<br>' in html
        assert html.count('<p') >= 2

    def test_table(self):
        """Test table conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '''| Col1 | Col2 |
|------|------|
| Val1 | Val2 |'''
        html = converter.convert(markdown)
        assert '<table' in html or '<tr' in html

    def test_horizontal_rule(self):
        """Test horizontal rule conversion."""
        converter = MarkdownToWeChatConverter()
        markdown = '---'
        html = converter.convert(markdown)
        assert '<hr' in html

    def test_xss_prevention(self):
        """Test that HTML is escaped to prevent XSS attacks."""
        converter = MarkdownToWeChatConverter()
        malicious_markdown = '# <script>alert("XSS")</script>'
        html = converter.convert(malicious_markdown)
        assert '<script>' not in html
        assert '&lt;script&gt;' in html

    def test_title_extraction(self):
        """Test title extraction from markdown."""
        converter = MarkdownToWeChatConverter()
        markdown = '''# Main Title

Some content'''
        title = converter.extract_title(markdown)
        assert title == 'Main Title'

    def test_title_extraction_with_prefix(self):
        """Test title extraction with prefix removal."""
        converter = MarkdownToWeChatConverter()
        markdown = '''# 目前技术趋势

Some content'''
        title = converter.extract_title(markdown)
        assert title == '技术趋势'

    def test_title_extraction_default(self):
        """Test title extraction with default title."""
        converter = MarkdownToWeChatConverter()
        markdown = '''No heading here
Just some content'''
        title = converter.extract_title(markdown, default_title='Default')
        assert title == 'Default'

    def test_convert_with_css(self):
        """Test conversion with CSS included."""
        converter = MarkdownToWeChatConverter()
        markdown = '# Test'
        html = converter.convert(markdown, include_css=True)
        assert '<style' in html

    def test_convert_without_css(self):
        """Test conversion without CSS."""
        converter = MarkdownToWeChatConverter()
        markdown = '# Test'
        html = converter.convert(markdown, include_css=False)
        # Should not have style tag
        assert html.count('<style') == 0

    def test_convert_file_not_found(self):
        """Test that file conversion raises error for missing file."""
        converter = MarkdownToWeChatConverter()
        with pytest.raises(FileNotFoundError):
            converter.convert_file('nonexistent.md')
