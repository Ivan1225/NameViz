import json
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
    nodestack = []
    bracketstack = []
    for dirpath, dirs, files in os.walk(directory):
      for filename in files:
        fname = os.path.join(dirpath,filename)
        if fname.endswith('.java'):
          currentNode = Name(None, filename, None, None, None, None)
          data.append(currentNode)
          linecount = 0
          with open(fname) as myfile:
            for line in myfile:
                classmatch = re.search('(?<=class)(\s)+[^\s]+', line)
                interfacematch = re.search('(?<=interface)(\s)+[^\s]+', line)
                enummatch = re.search('(?<=enum)(\s)+[^\s]+', line)
                methodmatch = re.search()
                varmatch = re.search()
                constantmatch = re.search()
                openbracketmatch = re.search('{')
                closebracketmatch = re.search('}')
                if classmatch != None:
                  newNode = Name(classmatch.group(0).strip(), filename, linecount, 'ClassName', None, currentNode)
                  currentNode.addName(newNode)
                  nodestack.append(currentNode)
                  currentnode = newNode
                  continue
                elif interfacematch != None:
                  newNode = Name(interfacematch.group(0).strip(), filename, linecount, 'InterfaceName', None, currentNode)
                  currentNode.addName(newNode)
                  nodestack.append(currentNode)
                  currentnode = newNode
                  continue
                elif enummatch != None:
                  newNode = Name(enummatch.group(0).strip(), filename, linecount, 'EnumName', None, currentNode)
                  currentNode.addName(newNode)
                  nodestack.append(currentNode)
                  currentnode = newNode
                  continue
                elif methodmatch != None:
                  newNode = Name(methodmatch.group(0).strip(), filename, linecount, 'MethodName', None, currentNode)
                  currentNode.addName(newNode)
                  nodestack.append(currentNode)
                  currentnode = newNode
                  continue
                elif varmatch != None:
                  newNode = Name(varmatch.group(0).strip(), filename, linecount, 'VariableName', None, currentNode)
                  currentNode.addName(newNode)
                  continue
                elif constantmatch != None:
                  newNode = Name(varmatch.group(0).strip(), filename, linecount, 'ConstantName', None, currentNode)
                  currentNode.addName(newNode)
                  continue
                if openbracketmatch != None:
                  bracketstack.append('{')
                if closebracketmatch != None:
                  bracketstack.pop()
                  if bracketstack.count == 0:
                    currentnode = nodestack.pop()
                linecount += 1
    
    with open(outputfile, 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
   main(sys.argv[1:])