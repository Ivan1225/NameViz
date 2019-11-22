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
    if(outputfile == ''):
        print ('usage is: search.py -d <inputdirectory> -o <outputfile>')
    
    data = {}
    
    # for dirpath, dirs, files in os.walk("."):
    #   for filename in files:
    #     fname = os.path.join(dirpath,filename)
    #     if fname.endswith('.java'):
    #       with open(fname) as myfile:
    #         line = myfile.read()
    #         c = line.count('bogo_sq')
    #         if c > 1:
    #           print fname, c
    
    with open('data.txt', 'w') as outfile:
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