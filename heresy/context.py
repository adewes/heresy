import cgi

class RenderContext(dict):

    exports = ['blocks', 'extends', 'include', 'environment', 'write']

    def __init__(self,context):
        self._environment = None        
        if not isinstance(context,dict):
            raise TypeError("context is not a dictionary!")

        self._write_buffer = []
        self._builtins = {}
        self._blocks = BlockManager(self)

        self.layout = None

        for name in self.exports:
            self.builtins[name] = getattr(self, name)
        
        self.variables = context
        
    @property
    def write_buffer(self):
        return self._write_buffer

    @write_buffer.setter
    def write_buffer(self, value):
        self._write_buffer = value

    @property
    def globals(self):
        return self._globals

    @property
    def blocks(self):
        return self._blocks

    @property
    def variables(self):
        return self._variables

    @property
    def builtins(self):
        return self._builtins

    @variables.setter
    def variables(self,variables):
        self._variables = variables
        self.update_globals()

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self,environment):
        self._environment = environment

    def write(self, value):
        self._write_buffer.append(value)

    def update_globals(self):
        self._globals = self.variables.copy()
        self._globals.update(self.builtins)

    def extends(self,filename):
        self.layout = filename

    def include(self,filename,**kwargs):
        template = self.environment.get_template(filename)
        last_variables = self.variables
        try:
            self.variables = kwargs
            return template.render_include(self)
        finally:
            self.variables = last_variables

class BlockGuard(object):

    def __init__(self, name, context):
        self._name = name
        self._context = context
        self._write_buffer = []
        self._overwrite = False

    def __call__(self, overwrite=False):
        self._overwrite = overwrite
        return self

    def __enter__(self):
        self._last_write_buffer = self._context.write_buffer
        if not self._write_buffer or self._overwrite:
            self._write_buffer = []
            self._context.write_buffer = self._write_buffer
        else:
            self._context.write_buffer = []
        return self

    def __exit__(self,type = None,value = None,traceback = None):
        self._context.write_buffer = self._last_write_buffer
        return False

    def __str__(self):
        return ''.join(self._write_buffer)

    def clear(self):
        self._write_buffer = []

    def write(self, value):
        if not value:
            return
        self._write_buffer.append(value)


class BlockManager(object):

    def __init__(self,context):
        self.__dict__['_context'] = context

    def __getattr__(self, name):
        super().__setattr__(name, BlockGuard(name, self._context))
        return getattr(self, name)

    def __str__(self):
        if hasattr(self,'main'):
            return str(self.main)
        return ""

    def __setattr__(self, name, value):
        if hasattr(self, name):
            attribute = getattr(self,name)
            if isinstance(attribute, BlockGuard) and not isinstance(value, BlockGuard):
                attribute.clear()
                attribute.write("%s" % value)
                return
        super(BlockManager,self).__setattr__(name, value)
