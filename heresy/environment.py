from heresy.template import Template
from heresy.parser import Parser

class Environment(object):

    def __init__(self,loader = None,use_cache = True):
        self._loader = loader
        self._use_cache = use_cache
        self._template_cache = {}

    def get_template(self, name, template_class = Template):
        if self._use_cache and name in self._template_cache and hasattr(self._loader,'is_obsolete') and not self._loader.is_obsolete(name):
            return self._template_cache[name]
        if not self._loader:
            raise AttributeError("No template loader defined!")
        source = self._loader.load(name)
        template = template_class(name,source,self)
        if self._use_cache:
            self._template_cache[name] = template
        return template

    def template_from_string(self,name,string):
        return Template(name,string,self)