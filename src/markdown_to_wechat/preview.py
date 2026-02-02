"""Preview generator for markdown-to-wechat."""

import html
from pathlib import Path
from typing import Optional

from .config import get_template_path


class PreviewGenerator:
    """Generate preview HTML files for converted content."""

    def __init__(self):
        """Initialize preview generator."""
        pass

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

        # Replace placeholders
        template = template.replace('{{TITLE}}', html.escape(title))
        template = template.replace('{{MARKDOWN}}', html.escape(markdown_text))
        template = template.replace('{{CONTENT}}', html_content)

        return template

    def generate_from_file(
        self,
        markdown_file: str,
        html_content: str,
        output_file: Optional[str] = None,
        split: bool = False
    ) -> str:
        """
        Generate preview from a Markdown file.

        Args:
            markdown_file: Path to Markdown file
            html_content: Converted HTML content
            output_file: Path to save preview file (optional)
            split: Whether to generate split preview

        Returns:
            Generated HTML preview content
        """
        # Read Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

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
