"""Manage yep project files"""
import os
import toml
from pathlib import Path
from .targets.factory import get_target_cls


class YepProject:

    def __init__(self, location_path: str):
        self._location_path = Path(location_path)
        assert self._location_path.exists()
        self.name = self._location_path.name
        self._config = None

    def yep_folder_path(self):
        return self._location_path / '.yep'
    
    def targets_folder_path(self):
        return self._location_path / '.yep' / 'targets'

    def load_config(self):
        """Load project configuration."""
        if self._config:
            return self._config
        config_path = self._location_path / '.yep' / 'project.toml'
        assert config_path.exists(), f"Project configuration not found at: {config_path}"
        # Load configuration from toml file
        self._config = toml.load(config_path)
        return self._config

    def initialize(self) -> bool:
        """Populate `.yep` folder if it does not exists."""
        if self.yep_folder_path().exists():
            print(f"Project '{self.name}' already initialized.")
            return False
        # Create '.yep' folder if it does not exist
        print(f"Initializing project '{self.name}'...")
        os.makedirs(self.yep_folder_path())
        return True

    def wrap_pipeline(self, pipeline_name, target: str, update: bool = False):
        """Generate pipeline wrapper for target."""
        config = self.load_config()
        pipeline = config['project']['pipelines'][pipeline_name]
        assert self.yep_folder_path().exists(), f"Project '{self.name}' not initialized."
        print(f"Generate pipeline wrapper of `{pipeline_name}` for target `{target}`.")
        target_folder = self.targets_folder_path() / target
        os.makedirs(target_folder, exist_ok=True)
        target_class = get_target_cls(target)
        target_instance = target_class(self._location_path, target_folder)
        pipeline_file_path = self._location_path / pipeline['file_path']
        target_instance.generate_wrapper(pipeline_name, config, pipeline_file_path, update)

    def wrap_all_pipelines(self, update: bool = False):
        """Generate pipeline wrappers for all targets."""
        config = self.load_config()
        for pipeline_name, pipeline in config['project']['pipelines'].items():
            for target in pipeline['targets']:
                self.wrap_pipeline(pipeline_name, target, update)

    def run_pipeline(self, pipeline_name, target: str, vars: dict):
        """Run pipeline on target."""
        config = self.load_config()
        pipeline = config['project']['pipelines'][pipeline_name]
        assert self.yep_folder_path().exists(), f"Project '{self.name}' not initialized."
        print(f"Run pipeline `{pipeline_name}` on target `{target}`.")
        target_folder = self.targets_folder_path() / target
        target_class = get_target_cls(target)
        target_instance = target_class(self._location_path, target_folder)
        pipeline_file_path = self._location_path / pipeline['file_path']
        return target_instance.run_pipeline(pipeline_name, config, pipeline_file_path, vars)
