from heresy.parser import Parser

import sys
import StringIO
import os.path

class BlockGuard(object):

  def __init__(self,name,stringBuffer,gv):
    self._name = name
    self._gv = gv
    self._stringBuffer = stringBuffer

  def __enter__(self):
    if not "_stringBuffer" in self._gv:
      self._gv["_stringBuffer"] = None
    self._outerStringBuffer = self._gv["_stringBuffer"]
    self._gv["_stringBuffer"] = self._stringBuffer
    return self._stringBuffer

  def __assign__(self,value):
    self.clear()
    self._stringBuffer.write(str(value))

  def clear(self):
    self._stringBuffer.truncate(0)

  def __repr__(self):
    return self._stringBuffer.getvalue()
    
  def __exit__(self,type = None,value = None,traceback = None):
    self._gv["_stringBuffer"] = self._outerStringBuffer    
    return False
    
def render(filename = None,blocks = {},gv = {},lv = {},template_paths = []):
  filepath = findFile(filename,template_paths)
  with open(filepath,'r') as f:
    parser = Parser()
    parser.parseString(f.read())
    code = parser.generateCode()
    return execCode(code,blocks = blocks,gv = gv,lv = lv,template_paths = template_paths)

def findFile(filename,template_paths):
    search_paths = ['']
    search_paths.extend(template_paths)
    for path in search_paths:
        full_path = path+filename
        if os.path.exists(full_path) and os.path.isfile(full_path):
            return full_path
    raise IOError(("Cannot find file %s! I tried the following search paths: " % filename)+str(search_paths))

def execCode(code,blocks = dict(),gv = globals(),lv = locals(),template_paths = []):

    def block(name,blocks = blocks):
        if not name in blocks.keys():
            blocks[name] = StringIO.StringIO()
        return BlockGuard(name,blocks[name],gv)
    
    def extends(filename):
        _meta['extends'] = filename
    
    def include(filename,**kwargs):
        print "Including %s" % filename
        return render(filename,blocks,gv,kwargs,template_paths)['main'].getvalue()

    _meta = {}
    
    gv['block'] = block
    gv['include'] = include
    gv['extends'] = extends

    block('main').clear()
        
    with block("main") as stringBuffer:
        gv["_stringBuffer"] = stringBuffer
        exec code in gv,lv

    if 'extends' in _meta:
        print "Extending %s" % _meta['extends']
        render(_meta['extends'],blocks,gv,lv,template_paths)

    return blocks

if __name__ == '__main__':
    blocks = render(sys.argv[1],template_paths = sys.argv[2:])
    print blocks['main'].getvalue()
