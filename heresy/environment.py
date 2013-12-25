from heresy.template import Template
from heresy.parser import Parser

class Environment(object):

    def __init__(self,loader):
        self._loader = loader

    def get_template(self,name):
        source = self._loader.load(name)
        parser = Parser()
        parser.parseString(source)
        code = parser.generateCode()
        return Template(name,source,code,self)

