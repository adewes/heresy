#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import cgi
import sys
from io import StringIO
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
        self._lineNumbers = []
        self._source = ""
        
    def blocks(self):
        return self._blocks
        
    def parseString(self,string):
        remainingString = string
        self.clear()
        self._source = string
        textMode = True
        codeDelimiter = None
        reFlags = re.I | re.M | re.S
        currentLineNumber = 1
        while len(remainingString) > 0:
            if textMode:
                textBlockMatch = re.search(r"^(.*?)(\<\%\=*h*)(.*)$",remainingString,reFlags)
                if textBlockMatch == None:
                    #There's only text in the file left...
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

    def getSourceExcerpt(self,lineNumber):
        lines = self._source.split("\n")
        start_line = max(0,lineNumber-2)
        end_line = min(len(lines),lineNumber+1)
        return "\n".join(lines[start_line:end_line])
        
    def translateLineNumber(self,lineNumber):
        ind = -1
        matchedLineNumber = -1
        for i,number in enumerate(self._lineNumbers):
            if number <= lineNumber:
                ind = i
                matchedLineNumber = number
            else:
                break
        if ind >= 0:
            offset = lineNumber - matchedLineNumber
            return self._blocks[ind].firstLineNumber()+offset
        return -1

    def _escapeString(self,string):
        return string.replace("'''",r"\'\'\'")

    def generateCode(self,strip_whitespace = True,ignore_exceptions = True):

        def _getCurrentLineNumber(string):
            return len(string.split("\n"))-1


        indentationLevel = 0
        indentationCharacter = "    "

        def ind(d = 0):
            return (indentationLevel+d)*indentationCharacter

        code = "import cgi"
        self._lineNumbers = []
        text_to_write = ""
        for block in self._blocks:
            self._lineNumbers.append(_getCurrentLineNumber(code))
            if type(block) == TextBlock:
                text = block.content()
                if text and (not strip_whitespace or text.strip()):
                    code+="\n"+indentationCharacter*indentationLevel+"write('''"+self._escapeString(text)+"''')"
            else:
                codeBlock = block.content()
                lines = codeBlock.split("\n")
                for line in lines:
                    indentationDiff = 0
                    match = re.search(r":(\s*)$",line, re.I | re.M)
                    if match:
                        if len(match.group(1)):
                            line=line[:-len(match.group(1))]
                        indentationDiff = 1
                    else:
                        match = re.search(r"(end)\s*$",line,re.I | re.M)
                        if match:
                            line=line[:-len(match.group(0))]
                            indentationDiff = -1
                    if block.delimiter() == '<%':
                        code+="\n"+ind()+line.strip()
                    elif block.delimiter() == '<%=':
                        if ignore_exceptions:
                            code+="\n"+ind()+ \
                                  "try:\n"+ind(1)+"write(\"%s\" % ("+line.strip()+"))"+ \
                                  "\n"+ind()+"except (AttributeError,KeyError):\n"+ind(1)+"pass"
                        else:
                            code+="\n"+indentationCharacter*indentationLevel+"write(\"%s\" % ("+line.strip()+"))"
                    elif block.delimiter() == '<%=h':
                        code+="\n"+indentationCharacter*indentationLevel+"write(cgi.escape(\"%s\" % ("+line.strip()+")))"
                    else:
                        raise Exception("Code generator: Unknown code delimiter: %s" % codeBlock.delimiter())
                    indentationLevel+=indentationDiff
        if indentationLevel != 0:
            raise Exception("Code generator: Code brackets do not match!")
        return code.lstrip().rstrip()
