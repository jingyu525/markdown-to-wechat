"""Default style definitions for WeChat HTML conversion."""

from typing import Dict
from .style_registry import StyleDefinition, StyleRegistry


def get_heading_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for heading elements (h1-h6).
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['h1'] = StyleDefinition.create(
        element='h1',
        font_size='24px',
        font_weight='bold',
        color='#2c3e50',
        margin_top='30px',
        margin_bottom='20px',
        padding_bottom='10px',
        border_bottom='2px solid #3498db',
        priority=100
    )
    
    styles['h2'] = StyleDefinition.create(
        element='h2',
        font_size='20px',
        font_weight='bold',
        color='#34495e',
        margin_top='25px',
        margin_bottom='15px',
        padding_left='10px',
        border_left='4px solid #3498db',
        priority=100
    )
    
    styles['h3'] = StyleDefinition.create(
        element='h3',
        font_size='18px',
        font_weight='bold',
        color='#555',
        margin_top='20px',
        margin_bottom='12px',
        priority=100
    )
    
    styles['h4'] = StyleDefinition.create(
        element='h4',
        font_size='17px',
        font_weight='bold',
        color='#666',
        margin_top='18px',
        margin_bottom='10px',
        priority=100
    )
    
    styles['h5'] = StyleDefinition.create(
        element='h5',
        font_size='16px',
        font_weight='bold',
        color='#777',
        margin_top='16px',
        margin_bottom='8px',
        priority=100
    )
    
    styles['h6'] = StyleDefinition.create(
        element='h6',
        font_size='15px',
        font_weight='bold',
        color='#888',
        margin_top='14px',
        margin_bottom='8px',
        priority=100
    )
    
    return styles


def get_table_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for table elements.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['table'] = StyleDefinition.create(
        element='table',
        width='100%',
        border_collapse='collapse',
        margin='20px 0',
        font_size='14px',
        priority=90
    )
    
    styles['th'] = StyleDefinition.create(
        element='th',
        border='1px solid #ddd',
        padding='12px',
        text_align='left',
        background_color='#3498db',
        color='white',
        font_weight='bold',
        priority=91
    )
    
    styles['td'] = StyleDefinition.create(
        element='td',
        border='1px solid #ddd',
        padding='12px',
        text_align='left',
        priority=91
    )
    
    return styles


def get_list_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for list elements.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['ul'] = StyleDefinition.create(
        element='ul',
        margin_bottom='16px',
        padding_left='25px',
        priority=80
    )
    
    styles['ol'] = StyleDefinition.create(
        element='ol',
        margin_bottom='16px',
        padding_left='25px',
        priority=80
    )
    
    styles['li'] = StyleDefinition.create(
        element='li',
        line_height='1.75',
        word_wrap='break-word',
        word_break='break-word',
        margin_bottom='0',
        priority=81
    )
    
    return styles


def get_text_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for text elements.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['p'] = StyleDefinition.create(
        element='p',
        margin_bottom='16px',
        text_align='left',
        line_height='1.75',
        word_wrap='break-word',
        word_break='break-word',
        white_space='pre-wrap',
        priority=70
    )
    
    styles['a'] = StyleDefinition.create(
        element='a',
        color='#3498db',
        text_decoration='none',
        border_bottom='1px solid #3498db',
        priority=60
    )
    
    styles['strong'] = StyleDefinition.create(
        element='strong',
        font_weight='bold',
        color='#2c3e50',
        priority=60
    )
    
    styles['em'] = StyleDefinition.create(
        element='em',
        font_style='italic',
        color='#555',
        priority=60
    )
    
    return styles


def get_code_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for code elements.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['pre'] = StyleDefinition.create(
        element='pre',
        background_color='#f4f4f4',
        border='1px solid #ddd',
        border_radius='5px',
        padding='15px',
        margin='20px 0',
        overflow_x='auto',
        font_size='14px',
        line_height='1.5',
        priority=50
    )
    
    styles['code'] = StyleDefinition.create(
        element='code',
        font_family='"SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace',
        background_color='#f4f4f4',
        padding='2px 5px',
        border_radius='3px',
        font_size='0.9em',
        priority=51
    )
    
    return styles


def get_blockquote_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for blockquote element.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['blockquote'] = StyleDefinition.create(
        element='blockquote',
        margin='20px 0',
        padding='15px 20px',
        background_color='#f8f9fa',
        border_left='4px solid #3498db',
        color='#555',
        line_height='1.75',
        word_wrap='break-word',
        word_break='break-word',
        priority=40
    )
    
    return styles


def get_misc_styles() -> Dict[str, StyleDefinition]:
    """
    Get style definitions for miscellaneous elements.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    styles['hr'] = StyleDefinition.create(
        element='hr',
        border='none',
        border_top='2px solid #e1e4e8',
        margin='30px 0',
        priority=30
    )
    
    styles['img'] = StyleDefinition.create(
        element='img',
        max_width='100%',
        height='auto',
        display='block',
        margin='20px auto',
        priority=30
    )
    
    return styles


def get_default_styles() -> Dict[str, StyleDefinition]:
    """
    Get all default style definitions.
    
    Returns:
        Dictionary mapping element names to StyleDefinitions
    """
    styles = {}
    
    # Merge all style categories
    styles.update(get_heading_styles())
    styles.update(get_table_styles())
    styles.update(get_list_styles())
    styles.update(get_text_styles())
    styles.update(get_code_styles())
    styles.update(get_blockquote_styles())
    styles.update(get_misc_styles())
    
    return styles


def get_default_registry() -> StyleRegistry:
    """
    Get a StyleRegistry populated with all default styles.
    
    Returns:
        StyleRegistry instance with all default styles registered
    """
    registry = StyleRegistry()
    
    for element, style_def in get_default_styles().items():
        registry.register(element, style_def)
    
    return registry


# For backward compatibility with config.py
def get_heading_styles_dict() -> Dict[int, str]:
    """
    Get heading styles as a dictionary mapping level to inline style string.
    
    This is for backward compatibility with config.py HEADING_STYLES.
    
    Returns:
        Dictionary mapping heading level (1-6) to inline style string
    """
    registry = get_default_registry()
    return {
        level: registry.get_inline_style(f'h{level}')
        for level in range(1, 7)
    }
