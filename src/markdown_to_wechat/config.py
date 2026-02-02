"""Configuration constants and CSS styles for markdown-to-wechat."""

from typing import Dict

# Configuration constants
TITLE_PREFIX_TO_REMOVE = '目前'

# Heading styles mapping
HEADING_STYLES: Dict[int, str] = {
    1: 'font-size:24px;font-weight:bold;color:#2c3e50;margin-top:30px;margin-bottom:20px;padding-bottom:10px;border-bottom:2px solid #3498db;',
    2: 'font-size:20px;font-weight:bold;color:#34495e;margin-top:25px;margin-bottom:15px;padding-left:10px;border-left:4px solid #3498db;',
    3: 'font-size:18px;font-weight:bold;color:#555;margin-top:20px;margin-bottom:12px;',
    4: 'font-size:17px;font-weight:bold;color:#666;margin-top:18px;margin-bottom:10px;',
    5: 'font-size:16px;font-weight:bold;color:#777;margin-top:16px;margin-bottom:8px;',
    6: 'font-size:15px;font-weight:bold;color:#888;margin-top:14px;margin-bottom:8px;'
}


def get_wechat_css() -> str:
    """Return CSS styles optimized for WeChat Official Account."""
    return '''
        <style>
            /* Base styles */
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                line-height: 1.75;
                color: #333;
                font-size: 16px;
            }

            /* Headings */
            h1 {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 30px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
            }

            h2 {
                font-size: 20px;
                font-weight: bold;
                color: #34495e;
                margin-top: 25px;
                margin-bottom: 15px;
                padding-left: 10px;
                border-left: 4px solid #3498db;
            }

            h3 {
                font-size: 18px;
                font-weight: bold;
                color: #555;
                margin-top: 20px;
                margin-bottom: 12px;
            }

            h4 {
                font-size: 17px;
                font-weight: bold;
                color: #666;
                margin-top: 18px;
                margin-bottom: 10px;
            }

            h5 {
                font-size: 16px;
                font-weight: bold;
                color: #777;
                margin-top: 16px;
                margin-bottom: 8px;
            }

            h6 {
                font-size: 15px;
                font-weight: bold;
                color: #888;
                margin-top: 14px;
                margin-bottom: 8px;
            }

            /* Paragraphs */
            p {
                margin-bottom: 16px;
                text-align: left;
                line-height: 1.75;
                word-wrap: break-word;
                word-break: break-word;
                white-space: pre-wrap;
            }

            /* Links */
            a {
                color: #3498db;
                text-decoration: none;
                border-bottom: 1px solid #3498db;
            }

            /* Bold and italic */
            strong {
                font-weight: bold;
                color: #2c3e50;
            }

            em {
                font-style: italic;
                color: #555;
            }

            /* Lists */
            ul, ol {
                margin-bottom: 16px;
                padding-left: 25px;
            }

            li {
                margin-bottom: 8px;
                line-height: 1.75;
                word-wrap: break-word;
                word-break: break-word;
            }

            /* Blockquotes */
            blockquote {
                margin: 20px 0;
                padding: 15px 20px;
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                color: #555;
                line-height: 1.75;
                word-wrap: break-word;
                word-break: break-word;
            }

            blockquote p {
                margin-bottom: 0;
            }

            /* Code blocks */
            pre {
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
                overflow-x: auto;
                font-size: 14px;
                line-height: 1.5;
            }

            code {
                font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
                background-color: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
                font-size: 0.9em;
            }

            pre code {
                background-color: transparent;
                padding: 0;
                border-radius: 0;
            }

            /* Tables */
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 14px;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }

            th {
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }

            tr:nth-child(even) {
                background-color: #f9f9f9;
            }

            /* Horizontal rules */
            hr {
                border: none;
                border-top: 2px solid #e1e4e8;
                margin: 30px 0;
            }

            /* Images */
            img {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
            }

            /* Special sections */
            .highlight-box {
                background-color: #e8f4f8;
                border: 1px solid #b8d4e3;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
            }

            .warning-box {
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
            }

            /* Custom classes for special formatting */
            .author-info {
                background-color: #f8f9fa;
                border-top: 2px solid #3498db;
                padding: 20px;
                margin-top: 30px;
                font-size: 14px;
            }
        </style>
    '''


def get_template_path(template_name: str) -> str:
    """
    Get the path to a template file.

    Args:
        template_name: Name of the template file (e.g., 'preview_template.html')

    Returns:
        Path to the template file
    """
    from pathlib import Path
    return Path(__file__).parent.parent.parent / 'templates' / template_name
