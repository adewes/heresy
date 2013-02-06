#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import cgi
import sys
import StringIO
import os.path

codeDelimiters = {"<%":"%>","<%=":"%>","<%=h":"%>"}

#1. Split file in HTML and code segments
#2. Go through code segments and look for :{ }: segments
#3. Indent the code between these segments accordingly
#4. Generate an executable *.py script

class Block(object):

  def __init__(self,content = None,firstLineNumber = 0):
    self._content = content
    self._firstLineNumber = firstLineNumber
    
  def firstLineNumber(self):
  	return self._firstLineNumber

  def setContent(self):
    self._content = content
    
  def content(self):
    return self._content
    
  def __repr__(self):
    return self.content()
    
  def __str__(self):
    return self.content()

class CodeBlock(Block):
  
  
  def __init__(self,code,delimiter,firstLineNumber):
    Block.__init__(self,code,firstLineNumber)
    self._delimiter = delimiter
    
  def delimiter(self):
    return self._delimiter
  
  def setDelimiter(self,delimiter):
    self._delimiter = delimiter
  
class TextBlock(Block):
  pass

class Parser:
  
  def __init__(self):
    self.clear()
    
  def clear(self):
    self._blocks = []
    
  def blocks(self):
  	return self._blocks
    
  def parseString(self,string):
    remainingString = string
    self.clear()
    textMode = True
    codeDelimiter = None
    reFlags = re.I | re.M | re.S
    currentLineNumber = 1
    while len(remainingString) > 0:
      if textMode:
        textBlockMatch = re.search(r"^(.*?)(\<\%\=*h*)(.*)$",remainingString,reFlags)
        if textBlockMatch == None:
          print "No code block found..."
          #There's only text in the file...
          self._blocks.append(TextBlock(remainingString,firstLineNumber = currentLineNumber))
          remainingString = ""
        else:
          if textBlockMatch.group(1) != "":
			textBlock = textBlockMatch.group(1)
			newlinesCount = len(re.findall(r'\n',textBlock))
			self._blocks.append(TextBlock(textBlock,firstLineNumber = currentLineNumber))
			currentLineNumber+=newlinesCount
          remainingString = textBlockMatch.group(3)
          codeDelimiter = textBlockMatch.group(2)
          if not codeDelimiter in codeDelimiters.keys():
            raise Exception("Invalid code delimiter: %s!" % codeDelimiter)
          textMode = False
      else:
        if codeDelimiter == None:
          raise Exception("Parsing error: Parsing a code block but the code delimiter is not defined!")
        escapedCodeEndDelimiter = re.escape(codeDelimiters[codeDelimiter])
        codeBlockMatch = re.search(r"^(.*?)"+escapedCodeEndDelimiter+r"(.*)$",remainingString,reFlags)
        if codeBlockMatch == None:
          raise Exception("Parsing error: Expected a code block terminated by %s!" % codeDelimiter)
        codeBlock = codeBlockMatch.group(1)
        newlinesCount = len(re.findall(r'\n',codeBlock))
        self._blocks.append(CodeBlock(codeBlock,codeDelimiter,firstLineNumber = currentLineNumber))
        currentLineNumber+=newlinesCount
        remainingString = codeBlockMatch.group(2) 
        textMode = True
        codeDelimiter = None
  
  def _escapeString(self,string):
    return string.replace("'''",r"\'\'\'")

  def generateCode(self):
    indentationLevel = 0
    code = "import cgi\n"
    indentationCharacter = "  "
    for block in self._blocks:
      if type(block) == TextBlock:
        text = block.content()
        code+="\n"+indentationCharacter*indentationLevel+"_stringBuffer.write('''"+self._escapeString(text)+"''')"
      else:
        codeBlock = block.content()
        lines = codeBlock.split("\n")
        for line in lines:
          increaseIndentation = False
          decreaseIndentation = False
          match = re.search(r":(\s*)$",line, re.I | re.M)
          if match:
            line=line[:-len(match.group(1))]
            increaseIndentation = True
          else:
            match = re.search(r"(-\s*)$",line,re.I | re.M)
            if match:
              line=line[:-len(match.group(1))]
              decreaseIndentation = True
          if block.delimiter() == '<%':
            code+="\n"+indentationCharacter*indentationLevel+line.strip()
          elif block.delimiter() == '<%=':
            code+="\n"+indentationCharacter*indentationLevel+"_stringBuffer.write(str("+line.strip()+"))"
          elif block.delimiter() == '<%=h':
            code+="\n"+indentationCharacter*indentationLevel+"_stringBuffer.write(cgi.escape(str("+line.strip()+")))"
          else:
            raise Exception("Code generator: Unknown code delimiter: %s" % codeBlock.delimiter())
          if increaseIndentation:
            indentationLevel+=1
          if decreaseIndentation:
            indentationLevel-=1
    if indentationLevel != 0:
      raise Exception("Code generator: Code brackets do not match!")
    return code.lstrip().rstrip()
