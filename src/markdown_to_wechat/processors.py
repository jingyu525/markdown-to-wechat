"""Element processors for injecting inline styles into HTML."""

import re
from abc import ABC, abstractmethod
from typing import List, Optional
from .style_registry import StyleRegistry


class ElementProcessor(ABC):
    """
    Abstract base class for element processors.
    
    Each processor handles specific HTML elements and injects inline styles.
    """
    
    @property
    @abstractmethod
    def elements(self) -> List[str]:
        """Return list of elements this processor handles."""
        pass
    
    @property
    def priority(self) -> int:
        """
        Processing priority (higher = processed first).
        
        Override in subclasses if needed.
        """
        return 0
    
    @abstractmethod
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """
        Process HTML content and inject styles.
        
        Args:
            html_content: HTML content to process
            registry: Style registry to get styles from
        
        Returns:
            Processed HTML content with inline styles
        """
        pass
    
    def _inject_style_to_tag(
        self, 
        html_content: str, 
        tag: str, 
        style: str
    ) -> str:
        """
        Inject inline style to a specific tag.
        
        Preserves existing attributes and avoids duplicate style attributes.
        
        Args:
            html_content: HTML content
            tag: Tag name (e.g., 'h1', 'th')
            style: Inline style string to inject
        
        Returns:
            HTML content with style injected
        """
        if not style:
            return html_content
        
        # Pattern to match opening tag (including self-closing tags like <hr />)
        # Matches: <tag>, <tag attr="value">, <tag/>, <tag attr="value"/>
        # Negative lookahead (?![^>]*style=) ensures we don't match tags with existing style
        # Capture group 1: all attributes including the optional /
        pattern = rf'<{tag}(?![^>]*style=)([^>]*?)(/?>)'
        
        def replace_tag(match):
            attrs = match.group(1).strip()
            closing = match.group(2)
            # Handle self-closing tags (attrs may contain trailing /)
            if attrs.endswith('/'):
                attrs = attrs[:-1].strip()
                closing = '/>'
            elif closing == '/>':
                closing = '/>'
            # Build the tag with style
            if attrs:
                return f'<{tag} {attrs} style="{style}"{closing}'
            else:
                return f'<{tag} style="{style}"{closing}'
        
        return re.sub(pattern, replace_tag, html_content, flags=re.IGNORECASE)


class TableProcessor(ElementProcessor):
    """Processor for table elements (table, th, td)."""
    
    @property
    def elements(self) -> List[str]:
        return ['table', 'th', 'td']
    
    @property
    def priority(self) -> int:
        return 90
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for table elements."""
        # Process table
        table_style = registry.get_inline_style('table')
        html_content = self._inject_style_to_tag(html_content, 'table', table_style)
        
        # Process th
        th_style = registry.get_inline_style('th')
        html_content = self._inject_style_to_tag(html_content, 'th', th_style)
        
        # Process td
        td_style = registry.get_inline_style('td')
        html_content = self._inject_style_to_tag(html_content, 'td', td_style)
        
        return html_content


class HeadingProcessor(ElementProcessor):
    """Processor for heading elements (h1-h6)."""
    
    @property
    def elements(self) -> List[str]:
        return [f'h{i}' for i in range(1, 7)]
    
    @property
    def priority(self) -> int:
        return 100
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for heading elements."""
        for level in range(1, 7):
            tag = f'h{level}'
            style = registry.get_inline_style(tag)
            html_content = self._inject_style_to_tag(html_content, tag, style)
        
        return html_content


class ListProcessor(ElementProcessor):
    """Processor for list elements (ul, ol, li)."""
    
    @property
    def elements(self) -> List[str]:
        return ['ul', 'ol', 'li']
    
    @property
    def priority(self) -> int:
        return 80
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for list elements."""
        # Process ul and ol
        ul_style = registry.get_inline_style('ul')
        html_content = self._inject_style_to_tag(html_content, 'ul', ul_style)
        
        ol_style = registry.get_inline_style('ol')
        html_content = self._inject_style_to_tag(html_content, 'ol', ol_style)
        
        # Process li
        li_style = registry.get_inline_style('li')
        html_content = self._inject_style_to_tag(html_content, 'li', li_style)
        
        return html_content


class TextProcessor(ElementProcessor):
    """Processor for text elements (p, a, strong, em)."""
    
    @property
    def elements(self) -> List[str]:
        return ['p', 'a', 'strong', 'em']
    
    @property
    def priority(self) -> int:
        return 70
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for text elements."""
        # Process p
        p_style = registry.get_inline_style('p')
        html_content = self._inject_style_to_tag(html_content, 'p', p_style)
        
        # Process a
        a_style = registry.get_inline_style('a')
        html_content = self._inject_style_to_tag(html_content, 'a', a_style)
        
        # Process strong
        strong_style = registry.get_inline_style('strong')
        html_content = self._inject_style_to_tag(html_content, 'strong', strong_style)
        
        # Process em
        em_style = registry.get_inline_style('em')
        html_content = self._inject_style_to_tag(html_content, 'em', em_style)
        
        return html_content


class CodeProcessor(ElementProcessor):
    """Processor for code elements (pre, code)."""
    
    @property
    def elements(self) -> List[str]:
        return ['pre', 'code']
    
    @property
    def priority(self) -> int:
        return 50
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for code elements."""
        # Process pre
        pre_style = registry.get_inline_style('pre')
        html_content = self._inject_style_to_tag(html_content, 'pre', pre_style)
        
        # Process code
        code_style = registry.get_inline_style('code')
        html_content = self._inject_style_to_tag(html_content, 'code', code_style)
        
        return html_content


class BlockquoteProcessor(ElementProcessor):
    """Processor for blockquote element."""
    
    @property
    def elements(self) -> List[str]:
        return ['blockquote']
    
    @property
    def priority(self) -> int:
        return 40
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for blockquote element."""
        style = registry.get_inline_style('blockquote')
        html_content = self._inject_style_to_tag(html_content, 'blockquote', style)
        return html_content


class MiscProcessor(ElementProcessor):
    """Processor for miscellaneous elements (hr, img)."""
    
    @property
    def elements(self) -> List[str]:
        return ['hr', 'img']
    
    @property
    def priority(self) -> int:
        return 30
    
    def process(self, html_content: str, registry: StyleRegistry) -> str:
        """Inject styles for miscellaneous elements."""
        # Process hr
        hr_style = registry.get_inline_style('hr')
        html_content = self._inject_style_to_tag(html_content, 'hr', hr_style)
        
        # Process img
        img_style = registry.get_inline_style('img')
        html_content = self._inject_style_to_tag(html_content, 'img', img_style)
        
        return html_content


def get_default_processors() -> List[ElementProcessor]:
    """
    Get list of all default processors.
    
    Returns:
        List of ElementProcessor instances sorted by priority
    """
    processors = [
        HeadingProcessor(),
        TableProcessor(),
        ListProcessor(),
        TextProcessor(),
        CodeProcessor(),
        BlockquoteProcessor(),
        MiscProcessor(),
    ]
    
    # Sort by priority (descending)
    return sorted(processors, key=lambda p: p.priority, reverse=True)
