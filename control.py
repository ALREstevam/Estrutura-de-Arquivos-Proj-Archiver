import archiver
import menu
import  filesAr

class Control(object) :
    def list_files(self) :
        pass
    def insert_files(self) :
        pass
    def remove_files(self):
        pass
    def __init__(self):
        lis = ["Quit","List files","Insert file","Remove Files"]

        #print ( choices.values () )
        self.menuInit = menu.Menu(lis)
        op = self.menuInit.start_menu()

        if(op == 0) :
            exit()
        elif(op == 1) :
            self.list_files()
        elif(op == 2):
            self.insert_files()
        else :
            self.remove_files()




