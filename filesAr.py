import os

def import_file (directory,name_file) :
   os.chdir(directory)
   new_file = open(name_file,"r+b")
   return  new_file

def export_file (directory,file) :

    read_file = open( file , 'r+b' )
    read_file = read_file.read()
    os.chdir (directory)
    new_file = open ( file, "w+b" )
    new_file.write(read_file)




