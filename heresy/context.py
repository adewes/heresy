import cgi

class RenderContext(object):

    exports = ['blocks','extends','include','environment']

    def __init__(self,context):
        self._environment = None        
        self.dict = context
        self._write_buffer = []
        self._blocks = BlockManager(self)
        self.layout = None
        self.dict['write'] = [].append
        for name in self.exports:
            self.dict[name] = getattr(self,name)

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self,environment):
        self._environment = environment

    @property
    def blocks(self):
        return self._blocks

    def extends(self,filename):
        self.layout = filename

    def include(self,filename,**kwargs):
        template = self.environment.get_template(filename)
        context = RenderContext(kwargs)
        return template.render(context)

class BlockGuard(object):

    def __init__(self,name,context):
        self._name = name
        self._context = context
        self._write_buffer = []
        self._append = False

    def __call__(self,append = False):
        self._append = append
        return self

    def __enter__(self):
        self._last_write = self._context.dict['write']
        if self._write_buffer and not self._append:
            self._context.dict['write'] = [].append
        else:
            self._context.dict['write'] = self._write_buffer.append
        return self

    def __exit__(self,type = None,value = None,traceback = None):
        self._context.dict['write'] = self._last_write
        return False

    def __unicode__(self):
        return ''.join(self._write_buffer)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def clear(self):
        self._write_buffer = []

    def write(self,value):
        if value:
            self._write_buffer.append(value)

class BlockManager(object):

    def __init__(self,context):
        self._context = context

    def __getattr__(self,name):
        setattr(self,name,BlockGuard(name,self._context))
        return getattr(self,name)

    def __unicode__(self):
        if hasattr(self,'main'):
            return unicode(self.main)
        return u""

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __setattr__(self,name,value):
        if hasattr(self,name):
            attribute = getattr(self,name)
            if isinstance(attribute,BlockGuard) and not isinstance(value,BlockGuard):
                attribute.clear()
                attribute.write("%s" % value)
                return
        super(BlockManager,self).__setattr__(name,value)
