from heresy.loaders.base import BaseLoader
import os

class FileLoader(BaseLoader):

    def __init__(self,paths=None):
        if paths is None:
            paths = ['']
        super(FileLoader,self).__init__()
        self._paths = [os.path.abspath(p) for p in paths]
        self._mtimes = {}

    def add_path(self,path):
        self._paths.append(os.path.abspath(path))

    def remove_path(self,path):
        if path in self._paths:
            self._paths.remove(path)

    def is_obsolete(self,filename):
        full_path = self.get_full_path(filename)
        if not full_path in self._mtimes:
            return False
        stats = os.stat(full_path)
        if stats.st_mtime > self._mtimes[full_path]:
            return True
        return False

    def get_full_path(self,filename):
        for path in self._paths:
            full_path = os.path.abspath(os.path.join(path, filename))
            if os.path.exists(full_path) and os.path.isfile(full_path):
                return full_path
        raise IOError("Template not found: %s" % filename)

    def load(self,filename):
        full_path = self.get_full_path(filename)
        with open(full_path,"r") as input_file:
            content = input_file.read()
        stats = os.stat(full_path)
        self._mtimes[full_path] = stats.st_mtime
        return content
            