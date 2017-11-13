class Menu(object) :

    def __init__(self,options) :
        self.options = options

    def start_menu(self):
        print("***Menu Archiver***")
        i = -1

        while((i<0) | (i>self.options.__len__())) :
            for i in range(0,self.options.__len__()) :
                print(i, " - ", self.options[i])
            print("***Choose between 0 and ",self.options.__len__()-1,"**")
            buffer = 0
            buffer = input()
            i = int (buffer)
        return i



