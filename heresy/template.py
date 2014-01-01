from heresy.parser import Parser

class Template(object):

    def __init__(self,url,source,environment):
        self._url = url
        self._source = source
        self._code = None
        self._bytecode = None
        self._environment = environment

    def compile(self):
        parser = Parser()
        parser.parseString(self._source)
        self._code = parser.generateCode()
        self._bytecode = compile(self._code,self._url,'exec')

    @property
    def code(self):
        if not self._code:
            self.compile()
        return self._code

    @property
    def bytecode(self):
        if not self._bytecode:
            self.compile()
        return self._bytecode

    @property
    def environment(self):
        return self._environment

    def render_include(self,context):
        exec self.bytecode in context.globals

    def render(self,context):
        context.environment = self.environment
        with context.blocks.main:
            exec self.bytecode in context.globals
        if context.layout:
            template = self.environment.get_template(context.layout)
            context.layout = None
            context.blocks.main = ""
            return template.render(context)
        return context.blocks
