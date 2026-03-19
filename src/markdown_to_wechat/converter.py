"""Core Markdown to WeChat HTML converter."""

import re
import html
from pathlib import Path
from typing import Optional

from .config import get_wechat_css, HEADING_STYLES, TITLE_PREFIX_TO_REMOVE
from .style_registry import StyleRegistry
from .style_applicator import StyleApplicator
from .styles import get_default_registry

# Try to import markdown library
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class MarkdownToWeChatConverter:
    """Convert Markdown to WeChat-compatible HTML."""

    def __init__(self):
        """Initialize the converter with default CSS styles and style applicator."""
        self.css_styles = get_wechat_css()
        
        # Initialize new architecture components
        self.registry = get_default_registry()
        self.applicator = StyleApplicator(self.registry)
        self.applicator.register_defaults()

    def _split_table_row(self, row: str) -> list:
        """
        Split a table row into cells, handling escaped pipe characters.
        
        Args:
            row: Table row string starting and ending with |
            
        Returns:
            List of cell contents
        """
        cells = []
        current_cell = ""
        i = 1
        end = len(row) - 1
        
        while i < end:
            char = row[i]
            if char == '\\' and i + 1 < end and row[i + 1] == '|':
                current_cell += '|'
                i += 2
                continue
            elif char == '|':
                cells.append(current_cell.strip())
                current_cell = ""
            else:
                current_cell += char
            i += 1
        
        if current_cell or cells:
            cells.append(current_cell.strip())
        
        return cells

    def _is_markdown_list_line(self, line: str) -> bool:
        stripped = line.lstrip()
        if re.match(r'^(\-|\*|\+)\s+', stripped):
            return True
        return re.match(r'^\d+\.\s+', stripped) is not None

    def _normalize_list_spacing(self, markdown_text: str) -> str:
        lines = markdown_text.split('\n')
        result = []
        in_code_block = False
        prev_was_list = False
        prev_was_blank = True

        for line in lines:
            stripped = line.strip()

            if stripped.startswith('```'):
                in_code_block = not in_code_block
                result.append(line)
                prev_was_list = False
                prev_was_blank = stripped == ''
                continue

            if in_code_block:
                result.append(line)
                prev_was_list = False
                prev_was_blank = stripped == ''
                continue

            is_list_line = self._is_markdown_list_line(line)

            if is_list_line and not prev_was_list and not prev_was_blank:
                result.append('')

            if prev_was_list and not is_list_line and stripped and not prev_was_blank:
                result.append('')

            result.append(line)
            prev_was_list = is_list_line
            prev_was_blank = stripped == ''

        return '\n'.join(result)

    def _strip_leading_breaks(self, text: str) -> str:
        return re.sub(r'^(<br\s*/?>\s*)+', '', text, flags=re.IGNORECASE)

    def _get_html_list_type(self, line: str) -> Optional[str]:
        cleaned = self._strip_leading_breaks(line).strip()
        if re.match(r'^(\-|\*|\+)\s+', cleaned):
            return 'ul'
        if re.match(r'^\d+\.\s+', cleaned):
            return 'ol'
        return None

    def _strip_html_list_marker(self, line: str, list_type: str) -> str:
        cleaned = self._strip_leading_breaks(line).strip()
        if list_type == 'ol':
            return re.sub(r'^\d+\.\s+', '', cleaned, count=1)
        return re.sub(r'^(\-|\*|\+)\s+', '', cleaned, count=1)

    def _fix_paragraph_lists(self, html_content: str) -> str:
        def replace_paragraph(match: re.Match) -> str:
            inner = match.group(1)
            lines = inner.split('\n')
            list_type = None
            first_index = None

            for index, line in enumerate(lines):
                current_type = self._get_html_list_type(line)
                if current_type:
                    list_type = current_type
                    first_index = index
                    break

            if list_type is None:
                return match.group(0)

            list_lines = []
            index = first_index
            while index < len(lines):
                line = lines[index]
                current_type = self._get_html_list_type(line)
                if current_type:
                    if current_type != list_type:
                        return match.group(0)
                    list_lines.append(line)
                elif line.strip() == '':
                    pass
                else:
                    break
                index += 1

            if not list_lines:
                return match.group(0)

            before_html = '\n'.join(lines[:first_index]).strip()
            after_html = '\n'.join(lines[index:]).strip()

            list_items = [
                self._strip_html_list_marker(line, list_type)
                for line in list_lines
            ]
            list_items = [item for item in list_items if item.strip()]

            if not list_items:
                return match.group(0)

            parts = []
            if before_html:
                parts.append(f'<p>{before_html}</p>')

            list_html = ''.join([f'<li>{item}</li>' for item in list_items])
            parts.append(f'<{list_type}>{list_html}</{list_type}>')

            if after_html:
                parts.append(f'<p>{after_html}</p>')

            return '\n'.join(parts)

        return re.sub(r'<p>(.*?)</p>', replace_paragraph, html_content, flags=re.S)

    def convert(self, markdown_text: str, include_css: bool = True) -> str:
        """
        Convert Markdown to WeChat-compatible HTML.

        Args:
            markdown_text: The Markdown content to convert
            include_css: Whether to include CSS styles in output

        Returns:
            HTML string suitable for WeChat Official Account
        """
        normalized_text = self._normalize_list_spacing(markdown_text)

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
                normalized_text,
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
            html_content = self._basic_markdown_to_html(normalized_text)

        html_content = self._fix_paragraph_lists(html_content)

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

            # Inline code MUST be processed first to protect its content from other formatting
            # Use a placeholder to protect code content
            code_placeholders = []
            def save_code(match):
                code_content = html.escape(match.group(1))
                placeholder = f'\x00CODE{len(code_placeholders)}\x00'
                code_placeholders.append(f'<code style="font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,Courier,monospace;background-color:#f4f4f4;padding:2px 5px;border-radius:3px;font-size:0.9em;">{code_content}</code>')
                return placeholder
            
            processed_line = re.sub(r'`([^`]+)`', save_code, processed_line)

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

            # Links
            processed_line = re.sub(
                r'\[([^\]]+)\]\(([^)]+)\)',
                r'<a href="\2" style="color:#3498db;text-decoration:none;border-bottom:1px solid #3498db;">\1</a>',
                processed_line
            )

            # Restore code placeholders
            for i, code_html in enumerate(code_placeholders):
                processed_line = processed_line.replace(f'\x00CODE{i}\x00', code_html)

            return processed_line

        # Enhanced converter for common Markdown elements
        lines = text.split('\n')
        html_lines = []
        in_code_block = False
        code_buffer = []
        in_list = False
        list_type = None
        in_table = False
        table_header_done = False
        in_blockquote = False
        blockquote_buffer = []

        for line in lines:
            stripped = line.strip()

            # Code blocks (must be processed first)
            if stripped.startswith('```'):
                if in_code_block:
                    # End code block
                    code_html = html.escape('\n'.join(code_buffer))
                    code_html = code_html.replace(' ', '&nbsp;')
                    code_html = code_html.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
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

            # Blockquotes - handle multi-line blockquotes
            if stripped.startswith('>'):
                if in_table:
                    html_lines.append('</tbody></table>')
                    in_table = False
                    table_header_done = False
                if in_list:
                    html_lines.append(f'</{list_type}>')
                    in_list = False
                if not in_blockquote:
                    in_blockquote = True
                    blockquote_buffer = []
                # Use original line to detect hard line breaks (trailing two spaces)
                quote_content = line.lstrip()
                if quote_content.startswith('>'):
                    quote_content = quote_content[1:]
                # Check for hard line break (trailing two spaces)
                has_hard_break = quote_content.endswith('  ')
                if has_hard_break:
                    quote_content = quote_content.rstrip()  # Only strip to preserve the marker
                else:
                    quote_content = quote_content.strip()
                blockquote_buffer.append((quote_content, has_hard_break))
                continue
            else:
                if in_blockquote:
                    # Process buffered lines into paragraphs
                    # Group lines by hard breaks and empty lines
                    paragraphs = []
                    current_para = []
                    for i, (line_content, has_hard_break) in enumerate(blockquote_buffer):
                        if line_content:
                            current_para.append((line_content, has_hard_break))
                        else:
                            # Empty line - end current paragraph
                            if current_para:
                                paragraphs.append(current_para)
                                current_para = []
                    if current_para:
                        paragraphs.append(current_para)
                    
                    para_html_parts = []
                    for para_lines in paragraphs:
                        # Join lines within paragraph, using <br> for hard breaks
                        para_content = []
                        for j, (line_content, has_hard_break) in enumerate(para_lines):
                            para_content.append(_process_inline_formatting(line_content))
                            # Add <br> if this line has hard break and it's not the last line
                            if has_hard_break and j < len(para_lines) - 1:
                                para_content.append('<br>')
                        para_html_parts.append(
                            f'<p style="margin-bottom:16px;text-align:left;line-height:1.75;word-wrap:break-word;word-break:break-word;white-space:pre-wrap;">{"".join(para_content)}</p>'
                        )
                    
                    para_html = ''.join(para_html_parts)
                    html_lines.append(
                        f'<blockquote style="margin:20px 0;padding:15px 20px;background-color:#f8f9fa;border-left:4px solid #3498db;color:#555;">{para_html}</blockquote>'
                    )
                    in_blockquote = False
                    blockquote_buffer = []

            # Unordered lists
            if stripped.startswith('- '):
                if in_table:
                    html_lines.append('</tbody></table>')
                    in_table = False
                    table_header_done = False
                if not in_list:
                    html_lines.append('<ul style="margin-bottom:16px;padding-left:25px;">')
                    in_list = True
                    list_type = 'ul'
                list_content = _process_inline_formatting(stripped[2:])
                html_lines.append(f'<li style="margin-bottom:8px;">{list_content}</li>')
                continue

            # Ordered lists
            if stripped and re.match(r'^\d+\.', stripped):
                if in_table:
                    html_lines.append('</tbody></table>')
                    in_table = False
                    table_header_done = False
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
                if in_table:
                    html_lines.append('</tbody></table>')
                    in_table = False
                    table_header_done = False
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
                if in_table:
                    html_lines.append('</tbody></table>')
                    in_table = False
                    table_header_done = False
                if in_list:
                    html_lines.append(f'</{list_type}>')
                    in_list = False
                html_lines.append('<hr style="border:none;border-top:2px solid #e1e4e8;margin:30px 0;">')
                continue

            # Tables (improved support with proper structure)
            if stripped.startswith('|') and stripped.endswith('|'):
                if in_list:
                    html_lines.append(f'</{list_type}>')
                    in_list = False
                cells = self._split_table_row(stripped)
                
                if all(cell.replace('-', '').replace(' ', '') == '' for cell in cells):
                    table_header_done = True
                    continue
                
                if not in_table:
                    html_lines.append('<table style="width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;">')
                    in_table = True
                    table_header_done = False
                
                if not table_header_done:
                    html_lines.append('<thead><tr>')
                    for cell in cells:
                        processed_cell = _process_inline_formatting(cell)
                        html_lines.append(f'<th style="border:1px solid #ddd;padding:12px;text-align:left;background-color:#3498db;color:white;font-weight:bold;">{processed_cell}</th>')
                    html_lines.append('</tr></thead><tbody>')
                else:
                    html_lines.append('<tr>')
                    for cell in cells:
                        processed_cell = _process_inline_formatting(cell)
                        html_lines.append(f'<td style="border:1px solid #ddd;padding:12px;text-align:left;">{processed_cell}</td>')
                    html_lines.append('</tr>')
                continue
            
            # Close table when we hit a non-table line
            if in_table and not stripped.startswith('|'):
                html_lines.append('</tbody></table>')
                in_table = False
                table_header_done = False

            # Process paragraphs and inline elements
            if stripped:
                processed_line = _process_inline_formatting(stripped)
                html_lines.append(f'<p style="margin-bottom:16px;text-align:left;line-height:1.75;word-wrap:break-word;word-break:break-word;">{processed_line}</p>')

        # Close any remaining list
        if in_list:
            html_lines.append(f'</{list_type}>')
        
        # Close any remaining table
        if in_table:
            html_lines.append('</tbody></table>')

        # Close any remaining blockquote
        if in_blockquote:
            paragraphs = []
            current_para = []
            for i, (line_content, has_hard_break) in enumerate(blockquote_buffer):
                if line_content:
                    current_para.append((line_content, has_hard_break))
                else:
                    if current_para:
                        paragraphs.append(current_para)
                        current_para = []
            if current_para:
                paragraphs.append(current_para)
            
            para_html_parts = []
            for para_lines in paragraphs:
                para_content = []
                for j, (line_content, has_hard_break) in enumerate(para_lines):
                    para_content.append(_process_inline_formatting(line_content))
                    if has_hard_break and j < len(para_lines) - 1:
                        para_content.append('<br>')
                para_html_parts.append(
                    f'<p style="margin-bottom:16px;text-align:left;line-height:1.75;word-wrap:break-word;word-break:break-word;white-space:pre-wrap;">{"".join(para_content)}</p>'
                )
            
            para_html = ''.join(para_html_parts)
            html_lines.append(
                f'<blockquote style="margin:20px 0;padding:15px 20px;background-color:#f8f9fa;border-left:4px solid #3498db;color:#555;">{para_html}</blockquote>'
            )

        return '\n'.join(html_lines)

    def _post_process_for_wechat(self, html_content: str) -> str:
        """
        Apply WeChat-specific post-processing to HTML content.

        WeChat Official Account editor has limitations:
        - Limited CSS support (inline styles work best)
        - No external stylesheets
        - Limited JavaScript support

        Uses the new StyleApplicator architecture to inject inline styles.

        Args:
            html_content: HTML content to post-process

        Returns:
            Post-processed HTML content
        """
        # Use StyleApplicator to inject all inline styles
        html_content = self.applicator.apply_styles(html_content)
        
        # Fix spaces in code blocks for WeChat editor (WeChat compresses normal spaces)
        # Only replace spaces in text content, not in HTML attributes
        def fix_pre_spaces(match: re.Match) -> str:
            pre_attrs = match.group(1) or ''
            inner_content = match.group(2)
            
            # Check if there's a <code> tag inside
            code_match = re.match(r'^\s*(<code[^>]*>)(.*?)(</code>)\s*$', inner_content, re.S)
            if code_match:
                code_open = code_match.group(1)
                code_content = code_match.group(2)
                code_close = code_match.group(3)
                code_content = code_content.replace(' ', '&nbsp;')
                code_content = code_content.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
                return f'<pre{pre_attrs}>{code_open}{code_content}{code_close}</pre>'
            else:
                # No <code> tag, replace spaces directly
                inner_content = inner_content.replace(' ', '&nbsp;')
                inner_content = inner_content.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
                return f'<pre{pre_attrs}>{inner_content}</pre>'

        html_content = re.sub(
            r'<pre([^>]*)>(.*?)</pre>',
            fix_pre_spaces,
            html_content,
            flags=re.S
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
