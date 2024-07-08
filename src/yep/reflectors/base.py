"""Provides BaseReflector class."""
from .pipeline import YepPipeline


class BaseReflector:
    """Base class for reflectors."""

    def __init__(self, programming_language: str, yep_pipeline: YepPipeline ) -> None:
         self.programming_language = programming_language
         self.yep_pipeline = yep_pipeline

    def parse(self):
        """Parse source code in pipeline_path."""
        raise NotImplementedError
    
    def analyze(self):
        """Analyze the parsed source code to deduce its main structure."""
        raise NotImplementedError

    def deduce_call_chain(self):
        """
        Deduce the call chain of the pipeline, that will be invoked by the pipeline wrapper.

        Enrich the pipeline data model (structure) with the call chain information.
        """
        print("Deduce the call chain of the pipeline.")
        # Use reflector to deduce call chain
        self.analyze()
