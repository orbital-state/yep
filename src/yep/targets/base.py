"""Base Target class for all targets"""
from pathlib import Path
from ..reflectors.pipeline import YepPipeline
from ..reflectors.factory import get_reflector_cls, guess_reflection_language


class BaseTarget:
    def __init__(self, project_folder: Path, target_folder: Path):
        self.project_folder = project_folder
        self.target_folder = target_folder

    def get_reflector(self, yep_pipeline):
        """Return reflector instance for the target programming language."""
        programming_language = guess_reflection_language(str(yep_pipeline.file_path))
        reflector_class = get_reflector_cls(programming_language)
        return reflector_class(programming_language, yep_pipeline)

    def reflect_pipeline(self, pipeline_name, pipeline_config, pipeline_file_path) -> YepPipeline:
        # Use reflector to generate pipeline code
        assert pipeline_file_path.exists(), f"Pipeline file not found at: {pipeline_file_path}"
        yep_pipeline = YepPipeline(pipeline_name, pipeline_config, pipeline_file_path)
        reflector = self.get_reflector(yep_pipeline)
        reflector.deduce_call_chain()
        return reflector.yep_pipeline

    def generate_wrapper(self):
        raise NotImplementedError()
