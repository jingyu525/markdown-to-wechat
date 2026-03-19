"""Configuration constants and CSS styles for markdown-to-wechat.

This module provides backward-compatible APIs that use the new style registry architecture.
"""

from typing import Dict
from pathlib import Path

# Configuration constants
TITLE_PREFIX_TO_REMOVE = '目前'


def get_wechat_css() -> str:
    """
    Return CSS styles optimized for WeChat Official Account.
    
    This function is maintained for backward compatibility.
    It now uses the new StyleRegistry architecture.
    
    Returns:
        CSS stylesheet string
    """
    from .styles import get_default_registry
    
    registry = get_default_registry()
    css_content = registry.get_all_css()
    
    return f'''
        <style>
{css_content}
        </style>
    '''


def get_template_path(template_name: str) -> Path:
    """
    Get the path to a template file.

    Args:
        template_name: Name of the template file (e.g., 'preview_template.html')

    Returns:
        Path to the template file
    """
    return Path(__file__).parent.parent.parent / 'templates' / template_name


def get_preview_styles() -> str:
    """
    Get CSS styles for preview templates.
    
    This method provides styles for preview functionality, including table styles
    that are essential for proper rendering in split preview mode.
    
    This function is maintained for backward compatibility.
    It now uses the new StyleRegistry architecture.
    
    Returns:
        CSS styles as a string (without <style> tags)
    """
    from .styles import get_default_registry
    
    registry = get_default_registry()
    return registry.get_all_css()


# Backward compatibility: HEADING_STYLES dictionary
# This is now generated from the new StyleRegistry
def _get_heading_styles_dict() -> Dict[int, str]:
    """
    Get heading styles as a dictionary mapping level to inline style string.
    
    This is for backward compatibility.
    
    Returns:
        Dictionary mapping heading level (1-6) to inline style string
    """
    from .styles import get_default_registry
    
    registry = get_default_registry()
    return {
        level: registry.get_inline_style(f'h{level}')
        for level in range(1, 7)
    }


# Create the HEADING_STYLES dictionary for backward compatibility
HEADING_STYLES: Dict[int, str] = _get_heading_styles_dict()
