import heresy.loaders
from heresy import Environment

class Loader(heresy.loaders.base.BaseLoader):

    def __init__(self,d):
        self.d = d

    def is_obsolete(self,key):
        return False

    def load(self,key):
        if not key in self.d:
            raise KeyError("Template not found: %s" % key)
        return self.d[key]

def test(template_name,context,templates):

    loader = Loader(templates)
    env = Environment(loader)
    heresy_context = heresy.RenderContext(context)
    heresy_tmpl = env.get_template(template_name)
    heresy_tmpl.compile()
    
    def run_test():
        """Heresy template"""
        res = heresy_tmpl.render(heresy_context)
        return res

    return run_test