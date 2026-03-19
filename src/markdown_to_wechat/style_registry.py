"""Style registry and definition for centralized style management."""

from dataclasses import dataclass, field
from typing import Dict, Optional, List
import re


@dataclass
class StyleDefinition:
    """
    Style definition for a single HTML element.
    
    Provides both inline style (for WeChat) and CSS style (for preview).
    
    Attributes:
        element: HTML element name (e.g., 'h1', 'table', 'th')
        styles: Dictionary of CSS properties and values
        priority: Processing priority (higher = processed first)
        enabled: Whether this style is active
    """
    
    element: str
    styles: Dict[str, str] = field(default_factory=dict)
    priority: int = 0
    enabled: bool = True
    
    @property
    def inline_style(self) -> str:
        """Convert styles to inline style string."""
        if not self.styles:
            return ""
        # Filter out non-CSS properties (like priority, enabled)
        css_styles = {
            k: v for k, v in self.styles.items()
            if k not in ['priority', 'enabled']
        }
        return ";".join(f"{k}:{v}" for k, v in css_styles.items())
    
    @property
    def css_style(self) -> str:
        """Convert styles to CSS style string."""
        if not self.styles:
            return ""
        properties = ";\n    ".join(f"{k}: {v}" for k, v in self.styles.items())
        return f"{self.element} {{\n    {properties};\n}}"
    
    @classmethod
    def create(cls, element: str, **style_props) -> 'StyleDefinition':
        """
        Factory method to create a StyleDefinition from keyword arguments.
        
        Args:
            element: HTML element name
            **style_props: CSS properties as keyword arguments
                          Use underscores for hyphens (e.g., font_size='16px')
                          Special keywords: priority, enabled
        
        Returns:
            StyleDefinition instance
        
        Example:
            >>> style = StyleDefinition.create('h1', font_size='24px', color='#333', priority=100)
        """
        # Extract special parameters
        priority = style_props.pop('priority', 0)
        enabled = style_props.pop('enabled', True)
        
        # Convert underscores to hyphens for CSS properties
        styles = {}
        for key, value in style_props.items():
            css_key = key.replace('_', '-')
            styles[css_key] = value
        
        return cls(element=element, styles=styles, priority=priority, enabled=enabled)
    
    def merge(self, other: 'StyleDefinition') -> 'StyleDefinition':
        """
        Merge this style with another, with other taking precedence.
        
        Args:
            other: Another StyleDefinition to merge
        
        Returns:
            New StyleDefinition with merged styles
        """
        merged_styles = {**self.styles, **other.styles}
        return StyleDefinition(
            element=self.element,
            styles=merged_styles,
            priority=max(self.priority, other.priority),
            enabled=self.enabled and other.enabled
        )


class StyleRegistry:
    """
    Centralized style registry for managing all element styles.
    
    Single source of truth for style definitions.
    Provides both inline styles (for WeChat) and CSS styles (for preview).
    
    Example:
        >>> registry = StyleRegistry()
        >>> registry.register('h1', StyleDefinition.create('h1', font_size='24px'))
        >>> inline = registry.get_inline_style('h1')
        >>> css = registry.get_css_style('h1')
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._styles: Dict[str, StyleDefinition] = {}
    
    def register(self, element: str, style_def: StyleDefinition) -> None:
        """
        Register a style definition for an element.
        
        Args:
            element: HTML element name
            style_def: Style definition to register
        """
        self._styles[element] = style_def
    
    def unregister(self, element: str) -> Optional[StyleDefinition]:
        """
        Remove a style definition from the registry.
        
        Args:
            element: HTML element name
        
        Returns:
            Removed style definition, or None if not found
        """
        return self._styles.pop(element, None)
    
    def get(self, element: str) -> Optional[StyleDefinition]:
        """
        Get style definition for an element.
        
        Args:
            element: HTML element name
        
        Returns:
            Style definition, or None if not found
        """
        return self._styles.get(element)
    
    def get_inline_style(self, element: str) -> str:
        """
        Get inline style string for an element.
        
        Args:
            element: HTML element name
        
        Returns:
            Inline style string, or empty string if not found
        """
        style_def = self.get(element)
        return style_def.inline_style if style_def else ""
    
    def get_css_style(self, element: str) -> str:
        """
        Get CSS style string for an element.
        
        Args:
            element: HTML element name
        
        Returns:
            CSS style string, or empty string if not found
        """
        style_def = self.get(element)
        return style_def.css_style if style_def else ""
    
    def get_all_css(self, include_disabled: bool = False) -> str:
        """
        Generate complete CSS stylesheet from all registered styles.
        
        Args:
            include_disabled: Whether to include disabled styles
        
        Returns:
            Complete CSS stylesheet string
        """
        css_rules = []
        for element, style_def in sorted(
            self._styles.items(), 
            key=lambda x: x[1].priority,
            reverse=True
        ):
            if include_disabled or style_def.enabled:
                css_rules.append(style_def.css_style)
        
        return "\n\n".join(css_rules)
    
    def get_all_elements(self) -> List[str]:
        """
        Get list of all registered elements.
        
        Returns:
            List of element names
        """
        return list(self._styles.keys())
    
    def update(self, element: str, **style_props) -> None:
        """
        Update styles for an existing element.
        
        Args:
            element: HTML element name
            **style_props: CSS properties to update
        """
        existing = self.get(element)
        if existing:
            new_styles = existing.styles.copy()
            for key, value in style_props.items():
                css_key = key.replace('_', '-')
                new_styles[css_key] = value
            existing.styles = new_styles
        else:
            # Create new if doesn't exist
            self.register(element, StyleDefinition.create(element, **style_props))
    
    def enable(self, element: str) -> None:
        """Enable a style definition."""
        style_def = self.get(element)
        if style_def:
            style_def.enabled = True
    
    def disable(self, element: str) -> None:
        """Disable a style definition."""
        style_def = self.get(element)
        if style_def:
            style_def.enabled = False
    
    def __contains__(self, element: str) -> bool:
        """Check if element is registered."""
        return element in self._styles
    
    def __len__(self) -> int:
        """Get number of registered styles."""
        return len(self._styles)
