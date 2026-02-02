"""Core Markdown to WeChat HTML converter."""

import re
import html
from pathlib import Path
from typing import Optional

from .config import get_wechat_css, HEADING_STYLES, TITLE_PREFIX_TO_REMOVE

# Try to import markdown library
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class MarkdownToWeChatConverter:
    """Convert Markdown to WeChat-compatible HTML."""

    def __init__(self):
        """Initialize the converter with default CSS styles."""
        self.css_styles = get_wechat_css()

    def convert(self, markdown_text: str, include_css: bool = True) -> str:
        """
        Convert Markdown to WeChat-compatible HTML.

        Args:
            markdown_text: The Markdown content to convert
            include_css: Whether to include CSS styles in output

        Returns:
            HTML string suitable for WeChat Official Account
        """
        if MARKDOWN_AVAILABLE:
            # Use markdown library for proper conversion
            extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.tables',
                'markdown.extensions.toc',
                'markdown.extensions.sane_lists',
                'markdown.extensions.smarty'
            ]

            html_content = markdown.markdown(
                markdown_text,
                extensions=extensions,
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'linenums': False
                    }
                }
            )
        else:
            # Fallback to basic conversion
            html_content = self._basic_markdown_to_html(markdown_text)

        # Apply WeChat-specific post-processing
        html_content = self._post_process_for_wechat(html_content)

        # Wrap with HTML structure
        if include_css:
            html_content = self._wrap_with_html_structure(html_content)

        return html_content

    def convert_file(
        self,
        input_file: str,
        output_file: Optional[str] = None,
        include_css: bool = True
    ) -> str:
        """
        Convert a Markdown file to WeChat-compatible HTML.

        Args:
            input_file: Path to input Markdown file
            output_file: Path to output HTML file (optional)
            include_css: Whether to include CSS styles in output

        Returns:
            HTML string

        Raises:
            FileNotFoundError: If input file does not exist
        """
        input_path = Path(input_file)

        # Validate input file
        if not input_path.exists():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        # Convert
        html_content = self.convert(markdown_text, include_css=include_css)

        # Save to file if output path specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Converted {input_file} -> {output_file}")

        return html_content

    def _basic_markdown_to_html(self, text: str) -> str:
        """
        Basic Markdown to HTML conversion (fallback when markdown library not available).

        Args:
            text: Markdown text to convert

        Returns:
            HTML string
        """
        def _process_inline_formatting(markdown_text: str) -> str:
            """
            Process inline Markdown formatting (bold, italic, code, links).

            Args:
                markdown_text: Text with inline Markdown formatting

            Returns:
                HTML-escaped text with formatting tags
            """
            processed_line = markdown_text

            # Bold
            processed_line = re.sub(
                r'\*\*(.+?)\*\*',
                r'<strong style="font-weight:bold;color:#2c3e50;">\1</strong>',
                processed_line
            )
            processed_line = re.sub(
                r'__(.+?)__',
                r'<strong style="font-weight:bold;color:#2c3e50;">\1</strong>',
                processed_line
            )

            # Italic
            processed_line = re.sub(
                r'\*(.+?)\*',
                r'<em style="font-style:italic;color:#555;">\1</em>',
                processed_line
            )
            processed_line = re.sub(
                r'_(.+?)_',
                r'<em style="font-style:italic;color:#555;">\1</em>',
                processed_line
            )

            # Inline code (escape content first for security)
            processed_line = re.sub(
                r'`([^`]+)`',
                lambda m: f'<code style="font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,Courier,monospace;background-color:#f4f4f4;padding:2px 5px;border-radius:3px;font-size:0.9em;">{html.escape(m.group(1))}</code>',
                processed_line
            )

            # Links
            processed_line = re.sub(
                r'\[([^\]]+)\]\(([^)]+)\)',
                r'<a href="\2" style="color:#3498db;text-decoration:none;border-bottom:1px solid #3498db;">\1</a>',
                processed_line
            )

            return processed_line

        # Enhanced converter for common Markdown elements
        lines = text.split('\n')
        html_lines = []
        in_code_block = False
        code_buffer = []
        in_list = False
        list_type = None

        for line in lines:
            stripped = line.strip()

            # Code blocks (must be processed first)
            if stripped.startswith('```'):
                if in_code_block:
                    # End code block
                    code_html = html.escape('\n'.join(code_buffer))
                    html_lines.append(
                        f'<pre style="background-color:#f4f4f4;border:1px solid #ddd;border-radius:5px;padding:15px;margin:20px 0;overflow-x:auto;font-size:14px;line-height:1.5;"><code style="background-color:transparent;padding:0;border-radius:0;">{code_html}</code></pre>'
                    )
                    code_buffer = []
                    in_code_block = False
                else:
                    # Start code block
                    in_code_block = True
                continue

            if in_code_block:
                code_buffer.append(line)
                continue

            # Blockquotes
            if stripped.startswith('>'):
                quote_content = _process_inline_formatting(stripped[1:].strip())
                html_lines.append(
                    f'<blockquote style="margin:20px 0;padding:15px 20px;background-color:#f8f9fa;border-left:4px solid #3498db;color:#555;"><p>{quote_content}</p></blockquote>'
                )
                continue

            # Unordered lists
            if stripped.startswith('- '):
                if not in_list:
                    html_lines.append('<ul style="margin-bottom:16px;padding-left:25px;">')
                    in_list = True
                    list_type = 'ul'
                list_content = _process_inline_formatting(stripped[2:])
                html_lines.append(f'<li style="margin-bottom:8px;">{list_content}</li>')
                continue

            # Ordered lists
            if stripped and re.match(r'^\d+\.', stripped):
                if not in_list:
                    html_lines.append('<ol style="margin-bottom:16px;padding-left:25px;">')
                    in_list = True
                    list_type = 'ol'
                list_content = _process_inline_formatting(re.sub(r"^\d+\.\s*", "", stripped))
                html_lines.append(f'<li style="margin-bottom:8px;">{list_content}</li>')
                continue

            # Close list when empty line or non-list item
            if in_list and not stripped:
                html_lines.append(f'</{list_type}>')
                in_list = False
                continue

            # Headings (refactored to eliminate duplication)
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            if heading_match:
                if in_list:
                    html_lines.append(f'</{list_type}>')
                    in_list = False

                level = len(heading_match.group(1))
                title_text = html.escape(heading_match.group(2))

                # Remove prefix if configured
                if title_text.startswith(TITLE_PREFIX_TO_REMOVE):
                    title_text = title_text[len(TITLE_PREFIX_TO_REMOVE):]

                html_lines.append(
                    f'<h{level} style="{HEADING_STYLES[level]}">{title_text}</h{level}>'
                )
                continue

            # Horizontal rule
            if stripped == '---':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                    in_list = False
                html_lines.append('<hr style="border:none;border-top:2px solid #e1e4e8;margin:30px 0;">')
                continue

            # Tables (basic support)
            if stripped.startswith('|') and stripped.endswith('|'):
                cells = [cell.strip() for cell in stripped.split('|')[1:-1]]
                if all(cell.replace('-', '').replace(' ', '') == '' for cell in cells):
                    # Separator row, skip
                    continue
                html_lines.append('<tr>')
                for cell in cells:
                    processed_cell = _process_inline_formatting(cell)
                    html_lines.append(f'<td style="border:1px solid #ddd;padding:12px;text-align:left;">{processed_cell}</td>')
                html_lines.append('</tr>')
                continue

            # Process paragraphs and inline elements
            if stripped:
                processed_line = _process_inline_formatting(stripped)
                html_lines.append(f'<p style="margin-bottom:16px;text-align:left;line-height:1.75;word-wrap:break-word;word-break:break-word;">{processed_line}</p>')

        # Close any remaining list
        if in_list:
            html_lines.append(f'</{list_type}>')

        return '\n'.join(html_lines)

    def _post_process_for_wechat(self, html_content: str) -> str:
        """
        Apply WeChat-specific post-processing to HTML content.

        WeChat Official Account editor has limitations:
        - Limited CSS support (inline styles work best)
        - No external stylesheets
        - Limited JavaScript support

        Args:
            html_content: HTML content to post-process

        Returns:
            Post-processed HTML content
        """
        # Process paragraphs to ensure proper line breaks and formatting
        html_content = re.sub(
            r'<p>',
            '<p style="margin-bottom:16px;text-align:left;line-height:1.75;word-wrap:break-word;word-break:break-word;white-space:pre-wrap;">',
            html_content
        )

        # Process tables to ensure they're responsive
        html_content = re.sub(
            r'<table>',
            '<table style="width:100%;border-collapse:collapse;margin:20px 0;">',
            html_content
        )

        # Process images to add responsive styling
        html_content = re.sub(
            r'<img',
            '<img style="max-width:100%;height:auto;display:block;margin:20px auto;"',
            html_content
        )

        # Process code blocks for better display
        html_content = re.sub(
            r'<pre>',
            '<pre style="background-color:#f4f4f4;border:1px solid #ddd;border-radius:5px;padding:15px;margin:20px 0;overflow-x:auto;font-size:14px;line-height:1.5;">',
            html_content
        )

        # Process blockquotes
        html_content = re.sub(
            r'<blockquote>',
            '<blockquote style="margin:20px 0;padding:15px 20px;background-color:#f8f9fa;border-left:4px solid #3498db;color:#555;">',
            html_content
        )

        return html_content

    def _wrap_with_html_structure(self, html_content: str, title: str = '微信公众号文章') -> str:
        """
        Wrap HTML content with full HTML document structure.

        Args:
            html_content: The HTML content to wrap
            title: Document title

        Returns:
            Complete HTML document
        """
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
{self.css_styles}
</head>
<body>
{html_content}
</body>
</html>"""

    def extract_title(self, markdown_text: str, default_title: str = '文章') -> str:
        """
        Extract title from Markdown text.

        Args:
            markdown_text: The Markdown content
            default_title: Default title if none found

        Returns:
            Extracted title
        """
        for line in markdown_text.split('\n'):
            if line.strip().startswith('# '):
                title = line.strip()[2:].strip()
                # Remove prefix if configured
                if title.startswith(TITLE_PREFIX_TO_REMOVE):
                    title = title[len(TITLE_PREFIX_TO_REMOVE):]
                return title
        return default_title
