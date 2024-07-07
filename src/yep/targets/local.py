"""Local target implementation."""

import os
from pathlib import Path
from .base import BaseTarget


class LocalTarget(BaseTarget):
    def generate_wrapper(self):
        """Generate pipeline wrapper for local target."""
        print("Generate pipeline wrapper for local target.")
        wrapper_path = self.target_folder / 'wrapper.py'
        with open(wrapper_path, 'w') as f:
            f.write(f"# Wrapper for local target\n")
            f.write(f"print('Run pipeline on local target.')\n")
            f.write(f"# Add your pipeline code here\n")
        print(f"Wrapper generated at: {wrapper_path}")