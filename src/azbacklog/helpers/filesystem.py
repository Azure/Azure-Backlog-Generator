import os
import sys


class FileSystem():
    parent_path = True
    allowed_parent_files = [
        'config.json',
        'readme.md'
    ]

    @staticmethod
    def find_work_items():
        developed_path = './workitems/'
        installed_path = os.path.join(sys.prefix, 'workitems/')
        if os.path.exists(developed_path):
            return developed_path
        elif os.path.exists(installed_path):
            return installed_path
        else:
            raise FileNotFoundError("'workitems' folder not found")

    def get_files(self, path):
        files = []
        (root, dirNames, fileNames) = next(os.walk(path))

        if self.parent_path is True:
            for fileName in fileNames:
                if fileName.lower() not in self.allowed_parent_files:
                    raise FileExistsError("parent path should not contain any files")
        elif self.parent_path is False and 'metadata.json' not in fileNames:
            raise FileNotFoundError(f"'metadata.json' does not exist in path '{path}'")

        fileNames.sort()
        for fileName in fileNames:
            if not (self.parent_path is True and fileName == 'config.json'):
                files.append(os.path.join(path, fileName))

        self.parent_path = False

        dirNames.sort()
        for dirName in dirNames:
            files.extend(self.get_files(os.path.join(root, dirName)))

        return files

    def read_file(self, path):
        content = None
        try:
            with open(path, 'r') as reader:
                content = reader.read()
                reader.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"'{path}' does not exist")
        except Exception:
            raise

        return content
