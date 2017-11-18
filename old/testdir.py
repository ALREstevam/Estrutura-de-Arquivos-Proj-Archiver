import os

def import_file (directory,name_file) :
   os.chdir(directory)
   new_file = open(name_file,"r+b")


   return  new_file

def export_file (directory,file) :
    name = file.name
    read_file = file.read()
    os.chdir (directory)
    new_file = open ( name, "w+b" )
    file.write(read_file)



dir = input()
nfile = input()
file = import_file(dir,nfile)
print(file)
dir = input()
export_file(dir,file)