from heresy.template import Template
from heresy.parser import Parser

class Environment(object):

    def __init__(self,loader = None):
        self._loader = loader
        self._template_cache = {}

    def get_template(self,name):
        if name in self._template_cache:
            return self._template_cache[name]
        if not self._loader:
            raise AttributeError("No template loader defined!")
        source = self._loader.load(name)
        template = Template(name,source,self)
        self._template_cache[name] = template
        return template

    def template_from_string(self,name,string):
        return Template(name,string,self)