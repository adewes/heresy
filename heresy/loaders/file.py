from heresy.loaders.base import BaseLoader
import os.path

class FileLoader(BaseLoader):

    def __init__(self,root_directory):
        super(FileLoader,self).__init__()
        self._root_directory = root_directory

    def load(self,path):
        full_path = os.path.abspath(self._root_directory + "/" + path)
        if not os.path.exists(full_path):
            raise IOError("Template does not exist: %s" % full_path)
        with open(full_path,"r") as input_file:
            content = input_file.read()
        return content