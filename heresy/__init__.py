from heresy.loaders import FileLoader
from heresy.environment import Environment
from heresy.context import RenderContext
from heresy.template import Template

import os
import sys

if __name__ == '__main__':
    loader = FileLoader([os.getcwd()])
    env = Environment(loader)
    template = env.get_template(sys.argv[1])
    template.compile()
    context = RenderContext({'foobar' : 'bizzfuzz in da house!!','recurse' : True})
    blocks = template.render(context)
    print blocks.main