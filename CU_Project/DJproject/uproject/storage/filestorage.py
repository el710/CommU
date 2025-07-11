
import os
import fnmatch
from pathlib import Path
import json
import logging

class FileStorage:
    def __init__(self, base_path=".", username:str=None):
        if username:
            path = os.path.join(base_path, username)
        else:
            path = base_path

        Path(path).mkdir(parents=True, exist_ok=True)
        self.base_path = path
    
    def find_all(self, pattern:str="*.*", recursive=False):
        """
            Find files in the base directory that match the filename pattern.
            
            Args:
                pattern: Pattern to match (e.g., '*.txt', 'file.docx', '*.*').
                recursive: Whether to search subdirectories recursively.
            Returns:
                List[str]: List of matching file paths.
        """
        list_files = []
        
        if recursive:
            for root, _, files in os.walk(self.base_path):
                for filename in files:
                    if fnmatch.fnmatch(filename, pattern):
                        ## list_files.append(os.path.join(root, filename)) - full path
                        list_files.append(filename)
        else:
            for filename in os.listdir(self.base_path):
                full_path = os.path.join(self.base_path, filename)
                if os.path.isfile(full_path) and fnmatch.fnmatch(filename, pattern):
                    list_files.append(filename)
        
        return list_files

    def save(self, obj, overwrite: bool = False) -> bool:
        # logging.info(f"save obj: {obj.get_token()}")
        filename = obj.file_name
        # logging.info(f"save file: {filename}\n")

        path = os.path.join(self.base_path, filename)

        if not overwrite and os.path.isfile(path):
            return False

        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj.to_dict(), f)
        return True

    def load(self, obj, filename:str=None) -> bool:
        # logging.info(f"load {obj}")
        if filename == None: filename = obj.file_name
        path = os.path.join(self.base_path, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # logging.info(f"load data: {data}")
                obj.from_dict(data)
                # logging.info(f"obj data: {obj.to_dict()}\n")
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


if __name__ == "__main__":

    WORK_PATH = os.path.join(os.getcwd(), "file_store")
    st = FileStorage(WORK_PATH, "user")
    list = st.find_all(pattern="*.stp")
    for item in list:
        print(os.path.splitext(item)[0])


    print(st.find_all(pattern="*.ctp"))
    print(st.find_all(pattern="*.ptp"))
