from heresy.parser import Parser
from heresy.runner import *

if __name__ == '__main__':
    blocks = render(sys.argv[1],template_paths = sys.argv[2:])
    print blocks['main'].getvalue()