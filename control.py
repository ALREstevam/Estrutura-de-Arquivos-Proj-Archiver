import archiver
import menu
import  filesAr

class Control(object) :

    def __init__(self):
        lis = ["Quit","List files","Insert file","Remove Files","Extract File"]

        self.menuInit = menu.Menu(lis)
        op = self.menuInit.start_menu()

        if op == 0 :
            exit()
        elif op == 1 :
            self.list_files()
        elif op == 2:
            self.insert_files()
        elif op == 3 :
            self.remove_files()
        else :
            self.extract_files()

    def list_files(self):
        pass

    def insert_files(self):
        print ( "Insert the directory path :" )
        dir_path = input ()
        print ( "Insert the file name :" )
        file_name = input ()


    def remove_files(self):
        pass

    def extract_files(self):
        print ( "Insert the directory path :" )
        dir_path = input ()
        print ( "Insert the file name :" )
        file_name = input ()
