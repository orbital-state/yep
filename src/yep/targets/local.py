"""Local target implementation."""

import os
from pathlib import Path
from .base import BaseTarget
from ..reflectors.pipeline import YepPipeline


class LocalTarget(BaseTarget):
        
    def generate_wrapper(self, pipeline_name, pipeline_config, pipeline_file_path, update: bool = False):
        """Generate pipeline wrapper for local target."""
        # Init wrapper location
        wrapper_path = self.target_folder / 'wrapper.py'
        if wrapper_path.exists() and not update:
            print(f"Wrapper already exists at: {wrapper_path}")
            return
        with open(wrapper_path, 'w') as f:
            f.write(f"# Wrapper for local target\n")
            f.write(f"print('Run pipeline on local target.')\n")
            f.write(f"# Add your pipeline code here\n")
        print(f"Wrapper generated at: {wrapper_path}")

        # Reflect pipeline structure from source code
        yep_pipeline = self.reflect_pipeline(pipeline_name, pipeline_config, pipeline_file_path)
        # Walk data model (structure) of reflector.yep_pipeline to generate code
        