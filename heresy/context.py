import cgi

class BlockGuard(object):

    def __init__(self,name,context):
        self._name = name
        self._context = context
        self._content = ""
        self._append = False

    def __call__(self,append = False):
        self._append = append
        return self

    def __enter__(self):
        self._last_writer = self._context.writer
        if self._content and not self._append:
            self._context.writer = lambda *args,**kwargs : True
        else:
            self._context.writer = self.write
        return self

    def __unicode__(self):
        return self._content

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __exit__(self,type = None,value = None,traceback = None):
        self._context.writer = self._last_writer
        return False

    def write(self,value,escape = False):
        if escape:
            string = cgi.escape(str(value))
        else:
            string = str(value)
        self._content+=string

    def clear(self):
        self._content = ""

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
            if isinstance(attribute,BlockGuard):
                attribute.clear()
                attribute.write(value)
                return
        super(BlockManager,self).__setattr__(name,value)

class RenderContext(dict):

    def __init__(self,context):
        super(RenderContext,self).__init__(context)
        self._environment = None        
        self._writer = lambda *args,**kwargs: True
        self._blocks = BlockManager(self)
        self.layout = None

    def __getitem__(self,key):
        if hasattr(self,key):
            return getattr(self,key)
        return super(RenderContext,self).__getitem__(key)

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self,writer):
        self._writer = writer

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self,environment):
        self._environment = environment

    @property
    def blocks(self):
        return self._blocks

    def write(self,value,*args,**kwargs):
        return self.writer(value,*args,**kwargs)

    def extends(self,filename):
        self.layout = filename

    def include(self,filename,**kwargs):
        template = self.environment.get_template(filename)
        context = RenderContext(kwargs)
        return template.render(context)
