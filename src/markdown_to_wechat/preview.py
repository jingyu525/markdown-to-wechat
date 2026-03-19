"""Preview generator for markdown-to-wechat."""

import html
import re
from pathlib import Path
from typing import Optional

from .config import get_template_path, get_preview_styles


class PreviewGenerator:
    """Generate preview HTML files for converted content."""

    def __init__(self):
        """Initialize preview generator."""
        pass

    def _extract_html_content(self, html_content: str) -> str:
        """
        Extract the main content from a complete HTML document.
        
        If the input is a complete HTML document (with <html>, <body> tags),
        this method extracts only the body content. Otherwise, returns the
        input as-is.
        
        Args:
            html_content: HTML content (can be complete document or fragment)
            
        Returns:
            HTML content fragment (without <html>, <head>, <body> tags)
        """
        # Check if it's a complete HTML document
        if '<html' in html_content.lower() and '<body' in html_content.lower():
            # Extract body content
            body_match = re.search(
                r'<body[^>]*>(.*?)</body>',
                html_content,
                re.DOTALL | re.IGNORECASE
            )
            if body_match:
                return body_match.group(1).strip()
        
        # Return as-is if not a complete document
        return html_content

    def generate_preview(
        self,
        markdown_text: str,
        html_content: str,
        title: str,
        output_file: Optional[str] = None,
        split: bool = False
    ) -> str:
        """
        Generate preview HTML from Markdown and converted HTML content.

        Args:
            markdown_text: Original Markdown text
            html_content: Converted HTML content
            title: Document title
            output_file: Path to save preview file (optional)
            split: Whether to generate split preview (markdown + HTML side by side)

        Returns:
            Generated HTML preview content

        Raises:
            FileNotFoundError: If template file not found
        """
        if split:
            preview_html = self._generate_split_preview(markdown_text, html_content, title)
        else:
            preview_html = self._generate_single_preview(html_content, title)

        # Save to file if path specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(preview_html)
            print(f"✅ Generated preview: {output_file}")

        return preview_html

    def _generate_single_preview(self, html_content: str, title: str) -> str:
        """
        Generate single-page preview HTML.

        Args:
            html_content: HTML content to embed
            title: Document title

        Returns:
            Complete preview HTML
        """
        template_path = get_template_path('preview_template.html')

        if not template_path.exists():
            raise FileNotFoundError(
                f"Preview template not found at {template_path}"
            )

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Replace placeholders
        template = template.replace('{{TITLE}}', html.escape(title))
        template = template.replace('{{CONTENT}}', html_content)

        return template

    def _generate_split_preview(
        self,
        markdown_text: str,
        html_content: str,
        title: str
    ) -> str:
        """
        Generate split preview HTML (Markdown + HTML side by side).

        Args:
            markdown_text: Original Markdown text
            html_content: Converted HTML content
            title: Document title

        Returns:
            Complete split preview HTML
        """
        template_path = get_template_path('preview_split_template.html')

        if not template_path.exists():
            raise FileNotFoundError(
                f"Split preview template not found at {template_path}"
            )

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Extract content if it's a complete HTML document
        html_content = self._extract_html_content(html_content)

        # Get preview styles
        preview_styles = get_preview_styles()

        # Replace placeholders
        template = template.replace('{{TITLE}}', html.escape(title))
        template = template.replace('{{MARKDOWN}}', html.escape(markdown_text))
        template = template.replace('{{CONTENT}}', html_content)
        template = template.replace('{{STYLES}}', preview_styles)

        return template

    def generate_from_file(
        self,
        markdown_file: str,
        html_content: Optional[str] = None,
        output_file: Optional[str] = None,
        split: bool = False
    ) -> str:
        """
        Generate preview from a Markdown file.
        
        This method can either use provided HTML content or convert the Markdown
        file internally. When converting internally, it ensures proper handling
        of CSS styles for preview mode.

        Args:
            markdown_file: Path to Markdown file
            html_content: Converted HTML content (optional, will be generated if not provided)
            output_file: Path to save preview file (optional)
            split: Whether to generate split preview

        Returns:
            Generated HTML preview content
        """
        # Read Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        # If HTML content not provided, convert internally
        if html_content is None:
            from .converter import MarkdownToWeChatConverter
            converter = MarkdownToWeChatConverter()
            # Always use include_css=False for preview to avoid nested HTML documents
            html_content = converter.convert(markdown_text, include_css=False)

        # Extract title
        from .converter import MarkdownToWeChatConverter
        converter = MarkdownToWeChatConverter()
        title = converter.extract_title(markdown_text, default_title=Path(markdown_file).stem)

        # Generate preview
        return self.generate_preview(
            markdown_text,
            html_content,
            title,
            output_file,
            split
        )
