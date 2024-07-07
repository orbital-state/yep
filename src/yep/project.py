"""Manage yep project files"""
import os
from pathlib import Path


class YepProject:

    def __init__(self, location_path: str):
        self._location_path = Path(location_path)
        assert self._location_path.exists()
        self.name = self._location_path.name

    def yep_folder_path(self):
        return self._location_path / '.yep'
    
    def initialize(self) -> bool:
        """Populate `.yep` folder if it does not exists."""
        if self.yep_folder_path().exists():
            print(f"Project '{self.name}' already initialized.")
            return False
        # Create '.yep' folder if it does not exist
        os.makedirs(self.yep_folder_path())
        return True
