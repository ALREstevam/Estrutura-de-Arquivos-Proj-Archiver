import archiver
import menu
import  filesAr

class Control(object) :
    def list_files(self) :
        pass
    def insert_files(self) :
        print("Insert the directory path :")
        dir_path = input()
        print ( "Insert the file name :" )
        file_name = input()
        new_file = filesAr.import_file(dir_path,file_name)

    def remove_files(self):
        pass
    def __init__(self):
        lis = ["Quit","List files","Insert file","Remove Files"]
s
        self.menuInit = menu.Menu(lis)
        op = self.menuInit.start_menu()

        if op == 0 :
            exit()
        elif op == 1 :
            self.list_files()
        elif op == 2:
            self.insert_files()
        else :
            self.remove_files()




