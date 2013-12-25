
class Template(object):

    def __init__(self,url,source,code,environment):
        self._url = url
        self._source = source
        self._code = code
        self._environment = environment

    @property
    def code(self):
        return self._code

    @property
    def environment(self):
        return self._environment

    def render(self,context):

        context.environment = self.environment
        
        code = self.code
        with context.blocks.main:
            exec code in context
        if context.layout:
            template = self.environment.get_template(context.layout)
            context.layout = None
            context.blocks.main = ""
            return template.render(context)

        return context.blocks
