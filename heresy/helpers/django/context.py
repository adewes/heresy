from __future__ import absolute_import

from heresy.context import RenderContext as HeresyContext
from django.template import Context as DjangoContext

class RenderContext(HeresyContext):

    def __init__(self, context,*args,**kwargs):
        flat_context = {}
        if isinstance(context, DjangoContext):
            for d in reversed(context.dicts):
                flat_context.update(d)
        else:
            flat_context = context
        return super(RenderContext, self).__init__(flat_context,*args,**kwargs)