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
    stack = []
    for dirpath, dirs, files in os.walk(directory):
      for filename in files:
        fname = os.path.join(dirpath,filename)
        if fname.endswith('.java'):
          currentnode = Name(None, filename, None, None, None)
          data.append(currentnode)
          linecount = 0
          with open(fname) as myfile:
              for line in myfile:
                #   classmatch = re.search('class (?<=abc)', line)
                #   if classmatch.group(0)
                #     newNode = Name(classmatch.group(0), filename, linecount, 'ClassName', None, currentNode)
                #     currentNode.addName(newNode)
                #     currentnode = newNode
                #     stack.append('Class')
                #     continue
                #   elif method
                #     add name
                #     add stack
                #     continue
                #   elif var
                #     add name
                #     continue
                #   elif ends with open bracket
                #     add stack
                #   elif closing bracket
                #     decrement stack
                #     *** you need someway to check here if you need to go back up the tree.
                #     *** such as always name classes 'class' and then check if the top element is 'class'
                #   linenumber++
    
    with open(outputfile, 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
   main(sys.argv[1:])