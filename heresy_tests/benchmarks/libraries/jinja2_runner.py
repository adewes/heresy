import jinja2
from jinja2 import BaseLoader, TemplateNotFound

class Loader(BaseLoader):

    def __init__(self, d):
        self.d = d 

    def get_source(self, environment, template):
        if not template in self.d:
            raise TemplateNotFound(template)
        return self.d[template], template, lambda: True

def test(template_name,context,templates):
    env = jinja2.Environment(loader = Loader(templates))
    template = env.get_template(template_name)

    def run_test():
        """Jinja-2 template"""
        res = template.render(**context)
        return res

    return run_test