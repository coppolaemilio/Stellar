import os
from PyQt4 import QtCore, QtGui

class ScriptList(QtGui.QWidget):
    
    def __init__(self, main,parent=None):
        super(ScriptList, self).__init__(parent)
        self.names = []
        self.main = main
                           
        font = QtGui.QFont()
        font.setPointSize(12)
        names = ['Class Constructor','Pygame Main Loop','Back']
        grid = QtGui.QGridLayout()
        j = 0
        pos = [(0, 0), (1, 0),(2,0)]

        for i in names:
            self.names.append(['',"%s" %(i)])

        for i in self.names:
            i[0] = QtGui.QPushButton(i[1], self)
            i[0].setText(i[1])
            i[0].setFont(font)
            grid.addWidget(i[0], pos[j][0], pos[j][1])
            j = j + 1


        QtCore.QObject.connect(self.names[0][0], QtCore.SIGNAL("clicked()"), self.AddClass)
        QtCore.QObject.connect(self.names[1][0], QtCore.SIGNAL("clicked()"), self.AddMainLoop)
        QtCore.QObject.connect(self.names[2][0], QtCore.SIGNAL("clicked()"), self.Back)

        self.setLayout(grid) 
        self.setGeometry(200, 200, 300, 80)
        self.setWindowIcon(QtGui.QIcon(os.path.join('data', 'icon.png')))
        self.setWindowTitle('List of Scripts - Stellar 0.2.1')
        self.center()
        self.show()

    def AddClass(self):
        self.main.textEdit.insertPlainText("class Name(object):\n    def __init__(self):\n")
        self.close()
        
    def AddMainLoop(self):
        self.main.textEdit.insertPlainText("""import pygame
from pygame.locals import *
from sys import exit


def main():

    #Variables
    screen_width = 800
    screen_height = 600


    #Initializes modules
    pygame.init()
    pygame.font.init()


    #Make The Pygame Window
    screen = pygame.display.set_mode((screen_width, screen_height))
    #screen = pygame.display.set_mode((screen_width, screen_height),screen.get_flags()^FULLSCREEN,32)


    #Frames Per Second
    clock = pygame.time.Clock()
    fps = 32


    #Load Images here


    #Load Animated Images here


    #Main Game Loop
    while True:
        mouse = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()


        #Blit everything here
        screen.fill((255,255,255)) #Remove if not needed
        

        #Exit Handler
        for event in pygame.event.get():
            if event.type==QUIT or event.type==KEYDOWN and event.key==K_ESCAPE:
                pygame.quit()
                exit()


        #Update Clock
        clock.tick(fps)
        pygame.display.update()

if __name__ == "__main__":
    main()

""")
        self.close()
    def Back(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
