"""Base Target class for all targets"""
from pathlib import Path


class BaseTarget:
    def __init__(self, project_folder: Path, target_folder: Path):
        self.project_folder = project_folder
        self.target_folder = target_folder

    def generate_wrapper(self):
        raise NotImplementedError()
