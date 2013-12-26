from heresy.parser import Parser

class Template(object):

    def __init__(self,url,source,environment):
        self._url = url
        self._source = source
        self._code = None
        self._environment = environment

    def compile(self):
        parser = Parser()
        parser.parseString(self._source)
        self._code = parser.generateCode()

    @property
    def code(self):
        if not self._code:
            self.compile()
        return self._code

    @property
    def environment(self):
        return self._environment

    def render(self,context):
        context.environment = self.environment
        with context.blocks.main:
            exec self.code in context.dict
        if context.layout:
            template = self.environment.get_template(context.layout)
            context.layout = None
            context.blocks.main = ""
            return template.render(context)
        return context.blocks
