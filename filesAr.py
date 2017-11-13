import os

def import_file (directory,name_file) :
   os.chdir(directory)
   new_file = open(name_file,"rb")
   return  name_file

def export_file (directory,file) :
    os.chdir (directory)
    new_file = open ( file , "wb" )



