"""Manage yep project files"""
import os
from pathlib import Path
from .targets.factory import get_target


class YepProject:

    def __init__(self, location_path: str):
        self._location_path = Path(location_path)
        assert self._location_path.exists()
        self.name = self._location_path.name

    def yep_folder_path(self):
        return self._location_path / '.yep'
    
    def targets_folder_path(self):
        return self._location_path / '.yep' / 'targets'

    def initialize(self) -> bool:
        """Populate `.yep` folder if it does not exists."""
        if self.yep_folder_path().exists():
            print(f"Project '{self.name}' already initialized.")
            return False
        # Create '.yep' folder if it does not exist
        print(f"Initializing project '{self.name}'...")
        os.makedirs(self.yep_folder_path())
        return True

    def wrap(self, target: str):
        """Generate pipeline wrapper for target."""
        assert self.yep_folder_path().exists(), f"Project '{self.name}' not initialized."
        print(f"Generate pipeline wrapper for {target}.")
        target_folder = self.targets_folder_path() / target
        os.makedirs(target_folder, exist_ok=True)
        target_class = get_target(target)
        target_instance = target_class(self._location_path, target_folder)
        target_instance.generate_wrapper()
