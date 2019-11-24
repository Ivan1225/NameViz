import json
import jsonpickle
import os
import getopt, sys
import re

class Name:
    def __init__(self, name, filename, line, nametype, vartype, parent):
        self.name = name
        self.filename = filename
        self.line = line
        self.nametype = nametype
        self.vartype = vartype
        self.subnames = []
        self.parent = parent
    def addName(self, name):
        self.subnames.append(name)

def main(argv):

    directory = ''
    outputfile = ''
    try:
          opts, args = getopt.getopt(argv,"d:o:")
    except getopt.GetoptError:
      print ('usage is: search.py -d <inputdirectory> -o <outputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-d':
         directory = arg
      elif opt == '-o':
         outputfile = arg
    if(directory == ''):
        print ('usage is: search.py -d <inputdirectory> -o <outputfile>')
        sys.exit(2)
    if(outputfile == ''):
        print ('usage is: search.py -d <inputdirectory> -o <outputfile>')
        sys.exit(2)
    if(os.path.isdir(directory) == False):
        print ('error: ', directory, ' is not a valid directory')
        sys.exit(2)
    data = []
    stack = []
    for dirpath, dirs, files in os.walk(directory):
      for filename in files:
        fname = os.path.join(dirpath,filename)
        if fname.endswith('.java'):
          topNode = Name(None, filename, None, None, None, None)
          currentNode = topNode
          data.append(currentNode)
          linecount = 0
          with open(fname) as myfile:
            print('parsing: ' + filename + '...')
            for line in myfile:
                classmatch = re.search('(?<=class)(\s)+[^\s]+', line)
                interfacematch = re.search('(?<=interface)(\s)+[^\s]+', line)
                enummatch = re.search('(?<=enum)(\s)+[^\s]+', line)
                methodmatch = re.search('[a-zA-Z]+[a-zA-Z0-9$_]*(\[\]|<[a-zA-Z]+[a-zA-Z0-9$_]*>)? +[a-zA-Z]+[a-zA-Z0-9$_]* *(?=\()', line)
                varmatch = re.findall('([a-zA-Z]+[a-zA-Z0-9$_]*(\[\]|<[a-zA-Z]+[a-zA-Z0-9$_]*>)?( +)[a-zA-Z]+[a-zA-Z0-9$_]*( *)(?=(=|;)))', line)
                constantmatch = re.findall('static( +)([a-zA-Z]+[a-zA-Z0-9$_]*(\[\]|<[a-zA-Z]+[a-zA-Z0-9$_]*>)?( +)[a-zA-Z]+[a-zA-Z0-9$_]*( *)(?=(=|;)))', line)
                openbracketmatch = re.findall('{', line)
                closebracketmatch = re.findall('}', line)
                if classmatch != None:
                  newNode = Name(classmatch.group(0).strip(), filename, linecount, 'ClassName', None, currentNode)
                  currentNode.addName(newNode)
                  stack.append('node')
                  currentNode = newNode
                elif interfacematch != None:
                  newNode = Name(interfacematch.group(0).strip(), filename, linecount, 'InterfaceName', None, currentNode)
                  currentNode.addName(newNode)
                  stack.append('node')
                  currentNode = newNode
                elif enummatch != None:
                  newNode = Name(enummatch.group(0).strip(), filename, linecount, 'EnumName', None, currentNode)
                  currentNode.addName(newNode)
                  stack.append('node')
                  currentNode = newNode
                elif methodmatch != None:
                  methodNameWithType = methodmatch.group(0).strip()
                  methodNameWithTypeArr = methodNameWithType.split(' ')
                  methodName = methodNameWithTypeArr[len(methodNameWithTypeArr)-1]
                  newNode = Name(methodName, filename, linecount, 'MethodName', None, currentNode)
                  currentNode.addName(newNode)
                  stack.append('node')
                  currentnode = newNode
                elif varmatch != []:
                  for match in varmatch:
                    nameWithType = match[0].strip()
                    nameTypeArr = nameWithType.split(' ')
                    name = nameTypeArr[len(nameTypeArr) - 1]
                    vartype = nameTypeArr[0]
                    nameType = 'VariableName'
                    if constantmatch != []:
                      for cons in constantmatch:
                        if (match[0] in cons):
                          nameType = 'ConstantName'
                          break
                    if (vartype != 'return'):
                      newNode = Name(name, filename, linecount, nameType, vartype, currentNode)
                      currentNode.addName(newNode)
                if openbracketmatch != []:
                  for obracket in openbracketmatch:
                    stack.append('{')
                if closebracketmatch != []:
                  for cbracket in closebracketmatch:
                    stack.pop()
                    if len(stack) == 0:
                        currentNode = topNode
                    elif stack[len(stack)-1] != '{':
                      currentNode = currentNode.parent
                      if currentNode == None:
                        currentNode = topNode
                      stack.pop()
                linecount += 1
            print('parsing: ' + filename +' complete!')
            print('----------------------')
    with open(outputfile, 'w') as outfile:
        outfile.write(jsonpickle.encode(data))

if __name__ == "__main__":
   main(sys.argv[1:])