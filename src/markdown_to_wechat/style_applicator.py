"""Style applicator for coordinating element processors."""

from typing import List
from .style_registry import StyleRegistry
from .processors import ElementProcessor, get_default_processors


class StyleApplicator:
    """
    Coordinates element processors to apply inline styles to HTML.
    
    This is the main entry point for applying styles to HTML content.
    It manages a collection of processors and executes them in priority order.
    
    Example:
        >>> registry = get_default_registry()
        >>> applicator = StyleApplicator(registry)
        >>> applicator.register_defaults()
        >>> html = applicator.apply_styles('<h1>Title</h1>')
    """
    
    def __init__(self, registry: StyleRegistry):
        """
        Initialize the style applicator.
        
        Args:
            registry: Style registry to get styles from
        """
        self.registry = registry
        self._processors: List[ElementProcessor] = []
    
    def register_processor(self, processor: ElementProcessor) -> None:
        """
        Register an element processor.
        
        Processors are executed in priority order (highest first).
        
        Args:
            processor: ElementProcessor instance to register
        """
        self._processors.append(processor)
        # Re-sort by priority
        self._processors.sort(key=lambda p: p.priority, reverse=True)
    
    def unregister_processor(self, processor_type: type) -> None:
        """
        Remove processors of a specific type.
        
        Args:
            processor_type: Type of processor to remove (e.g., TableProcessor)
        """
        self._processors = [
            p for p in self._processors 
            if not isinstance(p, processor_type)
        ]
    
    def register_defaults(self) -> None:
        """Register all default processors."""
        for processor in get_default_processors():
            self.register_processor(processor)
    
    def clear_processors(self) -> None:
        """Remove all registered processors."""
        self._processors = []
    
    def apply_styles(self, html_content: str) -> str:
        """
        Apply inline styles to HTML content.
        
        Executes all registered processors in priority order.
        
        Args:
            html_content: HTML content to process
        
        Returns:
            HTML content with inline styles applied
        """
        for processor in self._processors:
            html_content = processor.process(html_content, self.registry)
        
        return html_content
    
    def apply_styles_for_elements(
        self, 
        html_content: str, 
        elements: List[str]
    ) -> str:
        """
        Apply styles only for specific elements.
        
        Useful for selective processing.
        
        Args:
            html_content: HTML content to process
            elements: List of element names to process
        
        Returns:
            HTML content with inline styles applied for specified elements
        """
        for processor in self._processors:
            # Check if processor handles any of the requested elements
            if any(elem in processor.elements for elem in elements):
                html_content = processor.process(html_content, self.registry)
        
        return html_content
    
    def get_processor_count(self) -> int:
        """
        Get number of registered processors.
        
        Returns:
            Number of processors
        """
        return len(self._processors)
    
    def get_registered_elements(self) -> List[str]:
        """
        Get list of all elements handled by registered processors.
        
        Returns:
            List of element names
        """
        elements = []
        for processor in self._processors:
            elements.extend(processor.elements)
        return list(set(elements))  # Remove duplicates
