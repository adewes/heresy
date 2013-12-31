from heresy.loaders.base import BaseLoader
import os.path

class FileLoader(BaseLoader):

    def __init__(self,paths = []):
        super(FileLoader,self).__init__()
        self._paths = [os.path.abspath(p) for p in paths]
        print self._paths

    def add_path(self,path):
        self._paths.append(os.path.abspath(path))

    def remove_path(self,path):
        if path in self._paths:
            self._paths.remove(path)

    def load(self,filename):
        for path in self._paths:
            full_path = path + "/" + filename
            if os.path.exists(full_path) and os.path.isfile(full_path):
                with open(full_path,"r") as input_file:
                    content = input_file.read()
                return content
        raise IOError("Template not found: %s" % filename)
            