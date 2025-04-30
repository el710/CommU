# --- file: storage/storage.py ---
import os
from pathlib import Path
import json
import logging

class FileStorage:
    def __init__(self, base_path="."):
        Path(base_path).mkdir(parents=True, exist_ok=True)
        self.base_path = base_path

    def save(self, obj, overwrite: bool = False) -> bool:
        filename = obj.get_file_name()
        path = os.path.join(self.base_path, filename)

        if not overwrite and os.path.isfile(path):
            return False

        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj.to_dict(), f)
        return True

    def load(self, obj) -> bool:
        # logging.info(f"load {obj}")
        filename = obj.get_file_name()
        path = os.path.join(self.base_path, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                obj.from_dict(data)
            return True
        except Exception as exc:
            logging.info(f"Failed to load file {path}: {exc}")
            return False

    def delete(self, obj) -> bool:
        filename = obj.get_file_name()
        path = os.path.join(self.base_path, filename)

        try:
            os.remove(path)
            return True
        except Exception as exc:
            logging.info(f"Failed to delete file {path}: {exc}")
            return False
