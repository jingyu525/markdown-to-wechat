"""Unit tests for the style system architecture."""

import pytest
from markdown_to_wechat.style_registry import StyleDefinition, StyleRegistry
from markdown_to_wechat.styles import (
    get_default_styles,
    get_default_registry,
    get_heading_styles,
    get_table_styles,
    get_list_styles,
    get_text_styles,
    get_code_styles,
    get_blockquote_styles,
    get_misc_styles,
)
from markdown_to_wechat.processors import (
    TableProcessor,
    HeadingProcessor,
    ListProcessor,
    TextProcessor,
    CodeProcessor,
    BlockquoteProcessor,
    MiscProcessor,
    get_default_processors,
)
from markdown_to_wechat.style_applicator import StyleApplicator
from markdown_to_wechat.converter import MarkdownToWeChatConverter


class TestStyleDefinition:
    """Test cases for StyleDefinition."""
    
    def test_create_basic_style(self):
        """Test creating a basic style definition."""
        style = StyleDefinition.create('h1', font_size='24px', color='#333')
        
        assert style.element == 'h1'
        assert style.styles['font-size'] == '24px'
        assert style.styles['color'] == '#333'
    
    def test_inline_style_generation(self):
        """Test inline style string generation."""
        style = StyleDefinition.create('p', margin='10px', color='black')
        
        inline = style.inline_style
        assert 'margin:10px' in inline
        assert 'color:black' in inline
    
    def test_css_style_generation(self):
        """Test CSS style string generation."""
        style = StyleDefinition.create('h2', font_size='20px', font_weight='bold')
        
        css = style.css_style
        assert 'h2 {' in css
        assert 'font-size: 20px' in css
        assert 'font-weight: bold' in css
    
    def test_empty_styles(self):
        """Test handling of empty styles."""
        style = StyleDefinition(element='div', styles={})
        
        assert style.inline_style == ""
        assert style.css_style == ""
    
    def test_merge_styles(self):
        """Test merging two style definitions."""
        style1 = StyleDefinition.create('p', font_size='16px', color='black')
        style2 = StyleDefinition.create('p', font_size='18px', margin='10px')
        
        merged = style1.merge(style2)
        
        assert merged.styles['font-size'] == '18px'  # style2 overrides
        assert merged.styles['color'] == 'black'
        assert merged.styles['margin'] == '10px'


class TestStyleRegistry:
    """Test cases for StyleRegistry."""
    
    def test_register_and_get_style(self):
        """Test registering and retrieving styles."""
        registry = StyleRegistry()
        style = StyleDefinition.create('h1', font_size='24px')
        
        registry.register('h1', style)
        
        assert registry.get('h1') == style
        assert 'h1' in registry
    
    def test_get_inline_style(self):
        """Test getting inline style string."""
        registry = StyleRegistry()
        registry.register('h1', StyleDefinition.create('h1', font_size='24px', color='blue'))
        
        inline = registry.get_inline_style('h1')
        
        assert 'font-size:24px' in inline
        assert 'color:blue' in inline
    
    def test_get_css_style(self):
        """Test getting CSS style string."""
        registry = StyleRegistry()
        registry.register('p', StyleDefinition.create('p', margin='10px'))
        
        css = registry.get_css_style('p')
        
        assert 'p {' in css
        assert 'margin: 10px' in css
    
    def test_unregister_style(self):
        """Test unregistering a style."""
        registry = StyleRegistry()
        style = StyleDefinition.create('h1', font_size='24px')
        registry.register('h1', style)
        
        removed = registry.unregister('h1')
        
        assert removed == style
        assert 'h1' not in registry
    
    def test_get_all_css(self):
        """Test generating complete CSS stylesheet."""
        registry = StyleRegistry()
        registry.register('h1', StyleDefinition.create('h1', font_size='24px'))
        registry.register('p', StyleDefinition.create('p', margin='10px'))
        
        css = registry.get_all_css()
        
        assert 'h1 {' in css
        assert 'p {' in css
    
    def test_update_style(self):
        """Test updating an existing style."""
        registry = StyleRegistry()
        registry.register('h1', StyleDefinition.create('h1', font_size='24px', color='black'))
        
        registry.update('h1', color='blue')
        
        style = registry.get('h1')
        assert style.styles['font-size'] == '24px'
        assert style.styles['color'] == 'blue'
    
    def test_enable_disable(self):
        """Test enabling and disabling styles."""
        registry = StyleRegistry()
        style = StyleDefinition.create('h1', font_size='24px', enabled=True)
        registry.register('h1', style)
        
        registry.disable('h1')
        assert not registry.get('h1').enabled
        
        registry.enable('h1')
        assert registry.get('h1').enabled


class TestDefaultStyles:
    """Test cases for default style definitions."""
    
    def test_get_heading_styles(self):
        """Test getting heading styles."""
        styles = get_heading_styles()
        
        assert 'h1' in styles
        assert 'h6' in styles
        assert len(styles) == 6
    
    def test_get_table_styles(self):
        """Test getting table styles."""
        styles = get_table_styles()
        
        assert 'table' in styles
        assert 'th' in styles
        assert 'td' in styles
    
    def test_get_all_default_styles(self):
        """Test getting all default styles."""
        styles = get_default_styles()
        
        # Should include all categories
        assert 'h1' in styles  # headings
        assert 'table' in styles  # tables
        assert 'ul' in styles  # lists
        assert 'p' in styles  # text
        assert 'pre' in styles  # code
        assert 'blockquote' in styles
    
    def test_get_default_registry(self):
        """Test getting default registry."""
        registry = get_default_registry()
        
        assert len(registry) > 0
        assert 'h1' in registry
        assert 'table' in registry


class TestProcessors:
    """Test cases for element processors."""
    
    def test_table_processor(self):
        """Test TableProcessor."""
        registry = get_default_registry()
        processor = TableProcessor()
        
        html = '<table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>'
        result = processor.process(html, registry)
        
        assert 'style=' in result
        assert 'border:1px solid #ddd' in result
    
    def test_heading_processor(self):
        """Test HeadingProcessor."""
        registry = get_default_registry()
        processor = HeadingProcessor()
        
        html = '<h1>Title</h1><h2>Subtitle</h2>'
        result = processor.process(html, registry)
        
        assert 'font-size:24px' in result  # h1
        assert 'font-size:20px' in result  # h2
    
    def test_list_processor(self):
        """Test ListProcessor."""
        registry = get_default_registry()
        processor = ListProcessor()
        
        html = '<ul><li>Item</li></ul><ol><li>Item</li></ol>'
        result = processor.process(html, registry)
        
        assert 'padding-left:25px' in result
        assert 'margin-bottom:8px' in result
    
    def test_text_processor(self):
        """Test TextProcessor."""
        registry = get_default_registry()
        processor = TextProcessor()
        
        html = '<p>Text</p><a href="#">Link</a><strong>Bold</strong><em>Italic</em>'
        result = processor.process(html, registry)
        
        assert 'line-height:1.75' in result  # p
        assert 'color:#3498db' in result  # a
    
    def test_preserve_existing_attributes(self):
        """Test that processors preserve existing attributes."""
        registry = get_default_registry()
        processor = HeadingProcessor()
        
        html = '<h1 id="title" class="heading">Title</h1>'
        result = processor.process(html, registry)
        
        assert 'id="title"' in result
        assert 'class="heading"' in result
        assert 'style=' in result
    
    def test_no_duplicate_styles(self):
        """Test that processors don't add duplicate style attributes."""
        registry = get_default_registry()
        processor = HeadingProcessor()
        
        html = '<h1 style="color:red;">Title</h1>'
        result = processor.process(html, registry)
        
        # Should not add another style attribute
        assert result.count('style=') == 1
    
    def test_get_default_processors(self):
        """Test getting all default processors."""
        processors = get_default_processors()
        
        assert len(processors) > 0
        # Should be sorted by priority (descending)
        priorities = [p.priority for p in processors]
        assert priorities == sorted(priorities, reverse=True)


class TestStyleApplicator:
    """Test cases for StyleApplicator."""
    
    def test_register_processor(self):
        """Test registering a processor."""
        registry = get_default_registry()
        applicator = StyleApplicator(registry)
        
        processor = HeadingProcessor()
        applicator.register_processor(processor)
        
        assert applicator.get_processor_count() == 1
    
    def test_apply_styles(self):
        """Test applying styles to HTML."""
        registry = get_default_registry()
        applicator = StyleApplicator(registry)
        applicator.register_defaults()
        
        html = '<h1>Title</h1><p>Text</p><table><tr><th>Header</th></tr></table>'
        result = applicator.apply_styles(html)
        
        # Should have inline styles
        assert 'style=' in result
        assert 'font-size:24px' in result  # h1
        assert 'line-height:1.75' in result  # p
        assert 'background-color:#3498db' in result  # th
    
    def test_apply_styles_for_specific_elements(self):
        """Test applying styles only for specific elements."""
        registry = get_default_registry()
        applicator = StyleApplicator(registry)
        applicator.register_defaults()
        
        html = '<h1>Title</h1><p>Text</p>'
        result = applicator.apply_styles_for_elements(html, ['h1'])
        
        # h1 should have style
        assert 'font-size:24px' in result
        # p should not have style (not in elements list)
        assert '<p>' in result
        assert '<p style=' not in result
    
    def test_processor_priority_order(self):
        """Test that processors are executed in priority order."""
        registry = get_default_registry()
        applicator = StyleApplicator(registry)
        
        # Register processors manually
        applicator.register_processor(MiscProcessor())  # priority 30
        applicator.register_processor(HeadingProcessor())  # priority 100
        applicator.register_processor(TableProcessor())  # priority 90
        
        processors = applicator._processors
        
        # Should be sorted by priority (descending)
        assert processors[0].priority == 100
        assert processors[1].priority == 90
        assert processors[2].priority == 30


class TestIntegration:
    """Integration tests for the complete style system."""
    
    def test_converter_uses_new_architecture(self):
        """Test that MarkdownToWeChatConverter uses the new architecture."""
        converter = MarkdownToWeChatConverter()
        
        # Should have registry and applicator
        assert hasattr(converter, 'registry')
        assert hasattr(converter, 'applicator')
        assert converter.applicator.get_processor_count() > 0
    
    def test_end_to_end_conversion(self):
        """Test end-to-end Markdown to HTML conversion."""
        converter = MarkdownToWeChatConverter()
        
        markdown = """# Title

## Subtitle

This is a paragraph with **bold** and *italic*.

- Item 1
- Item 2

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
        
        html = converter.convert(markdown, include_css=False)
        
        # Should have inline styles for all elements
        assert 'font-size:24px' in html  # h1
        assert 'font-size:20px' in html  # h2
        assert 'font-weight:bold' in html  # strong
        assert 'background-color:#3498db' in html  # th
        assert 'padding-left:25px' in html  # ul
    
    def test_backward_compatibility(self):
        """Test backward compatibility with config.py."""
        from markdown_to_wechat.config import HEADING_STYLES, get_wechat_css
        
        # HEADING_STYLES should still work
        assert 1 in HEADING_STYLES
        assert 'font-size:24px' in HEADING_STYLES[1]
        
        # get_wechat_css should still work
        css = get_wechat_css()
        assert '<style>' in css
        assert 'h1 {' in css
    
    def test_wechat_compatible_styles(self):
        """Test that generated styles are WeChat-compatible."""
        converter = MarkdownToWeChatConverter()
        
        markdown = """# Title

> This is a quote

```
code block
```
"""
        
        html = converter.convert(markdown, include_css=False)
        
        # Should only use inline styles, no <style> tags in body
        body_start = html.find('<body>')
        if body_start > 0:
            body_content = html[body_start:]
            assert '<style>' not in body_content
        
        # All elements should have inline styles
        assert 'style=' in html
