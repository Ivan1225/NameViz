import json
import os
import getopt, sys

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
    data = {}
    for dirpath, dirs, files in os.walk(directory):
      for filename in files:
        fname = os.path.join(dirpath,filename)
        if fname.endswith('.java'):
            print(fname)
        #   with open(fname) as myfile:
        #     line = myfile.read()
        #     c = line.count('bogo_sq')
        #     if c > 1:
        #       print fname, c
    
    with open(outputfile, 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
   main(sys.argv[1:])
   
# name
# filename
# linenumber
# type
# vartype
# class
# method

# Stack: [class, method, if, while]
# while
#   read line
#   if class
#     add name
#     add stack
#     break
#   if method
#     add name
#     add stack
#     break
#   if var
#     add name
#     break
#   if ends with open bracket
#     add stack
#   if closing bracket
#     decrement stack
#   linenumber++
# addName()
#   getClassName
#   getMethodName