"""Provides BaseReflector class."""


class BaseReflector:
    """Base class for reflectors."""

    def __init__(self, programming_language) -> None:
         self.programming_language = programming_language

    def parse(self, pipeline_path):
        """Parse source code in pipeline_path."""
        raise NotImplementedError
    
    def analyze(self, pipeline_path):
        """Analyze the parsed source code to deduce its main structure."""
        raise NotImplementedError
