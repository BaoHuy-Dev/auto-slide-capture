import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"

class ConfigManager:
    """Manages reading and writing application configuration."""

    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads the configuration from the JSON file."""
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def save_config(self) -> None:
        """Saves the current configuration to the JSON file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration value and saves the config."""
        self.config[key] = value
        self.save_config()

    def get_capture_region(self) -> Dict[str, int] | None:
        """Returns the capture region dictionary or None if not set."""
        return self.config.get("capture")

    def set_capture_region(self, left: int, top: int, width: int, height: int) -> None:
        """Sets the capture region."""
        self.set("capture", {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        })

    def get_output_folder(self) -> str:
        """Returns the output folder."""
        return self.config.get("output_folder", "")

    def set_output_folder(self, path: str) -> None:
        """Sets the output folder."""
        self.set("output_folder", path)
