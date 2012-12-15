#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stellar.  If not, see <http://www.gnu.org/licenses/>.

"""
Stellar
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys
sys.path.append("src")

import os
import webbrowser
import inspect
import syntax
import platform
import subprocess
import shutil

from PyQt4 import QtCore, QtGui

import cfg
from preferences import PreferencesDialog
from splashscreen import Start
from dialogs import NewProjectDialog
from spritegui import SpriteGUI
from soundgui import SoundGUI
from fontgui import FontGUI
from scriptgui import ScriptGUI
from objectgui import ObjectGUI


class QMdiAreaW(QtGui.QMdiArea):
    def __init__(self, main):
        super(QMdiAreaW, self).__init__(main)
        self.setBackground (QtGui.QBrush(QtGui.QPixmap(os.path.join("Data", "background.png"))))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


class TreeWidget(QtGui.QTreeWidget):
    def __init__(self, main):
        super(TreeWidget, self).__init__(main)
        self.header().setHidden(True)
        self.setWindowTitle('Resources')
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.main = main
        self.connect(self, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),self.DoEvent)
        self.connect(self, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem *)"), self.itemCollapsed)
        self.connect(self, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem *)"), self.itemExpanded)
        self.Path = {}
        
        self.Names = self.main.Names
        self.ImageNames = (None, 'sound.png', 'font.png', 'script.png', 'object.png', 'game.png')
        self.Parent = {}
        self.ImageName = {}
        j=0
        for i in self.Names:
            self.ImageName[i] = self.ImageNames[j]
            j+=1

    def itemCollapsed(self, obj):
        self.main.expanded[str(obj.text(0))] = False

    def itemExpanded(self, obj):
        self.main.expanded[str(obj.text(0))] = True

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        insertAction = menu.addAction("Insert")
        insertAction.triggered.connect(self.AddSprChild)
        
        duplicateAction = menu.addAction("Duplicate")
        duplicateAction.setShortcut('Alt+Ins')
        duplicateAction.setDisabled (True)
        menu.addSeparator()
        insertgroupAction = menu.addAction("Insert Group")
        insertgroupAction.setShortcut('Shift+Ins')
        insertgroupAction.setDisabled (True)
        menu.addSeparator()
        deleteAction = menu.addAction("Delete")
        deleteAction.setShortcut('Shift+Del')
        deleteAction.setDisabled (True)
        menu.addSeparator()
        renameAction = menu.addAction("Rename")
        renameAction.setShortcut('F2')
        renameAction.setDisabled (True)
        menu.addSeparator()
        propertiesAction = menu.addAction("Properties...")
        propertiesAction.setShortcut('Alt+Enter')
        propertiesAction.triggered.connect(self.DoEvent)
        action = menu.exec_(self.mapToGlobal(event.pos()))

    def DoEvent(self):
       
        def openWindow(directory):
            if item.parent().text(0) == directory:
                self.main.window = QtGui.QWidget()
                
                if directory == "Sprites":
                    self.main.sprite = SpriteGUI(self.main.window,item.text(0), self.main.dirname)
                elif directory == "Sound":
                    self.main.sound = SoundGUI(self.main.window,item.text(0), self.main.dirname)
                elif directory == "Fonts":
                    self.main.font = FontGUI(self.main.window,item.text(0))
                elif directory == "Scripts":
                    self.main.script = ScriptGUI(self.main.window,item.text(0), self.main.dirname, self.main)
                elif directory == "Objects":
                    self.main.object = ObjectGUI(self.main.window,item.text(0), self.main.dirname)
                
                if directory[-1:] == "s":
                    directory = directory[:-1]
                
                self.main.qmdiarea.addSubWindow(self.main.window)
                
                self.main.window.setVisible(True)
                self.main.window.setWindowTitle( directory + " properties: " + item.text(0) )
                if directory == "Sprite":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'sprite.png')))
                elif directory == "Sound":
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', 'sound.png')))
                else:
                    self.main.qmdiarea.activeSubWindow().setWindowIcon(QtGui.QIcon(os.path.join('Data', self.ImageName[unicode(directory + 's']))))

        
        
        item = self.currentItem()
        if not item.parent() == None:
            for name in self.Names:
                openWindow(name)
    
    def InitParent(self):
        
        for name in self.Names:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", "folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Parent[name] = QtGui.QTreeWidgetItem(self, QtCore.QStringList(name))
            self.Parent[name].setIcon(0,icon)
            
    def InitChild(self, fillarrays=False):
        dirname = self.main.dirname
        
        for name in self.Names:
            self.Path[name] = os.path.join(dirname, name)
            for ChildSource in sorted(os.listdir(self.Path[name])):                
                icon = QtGui.QIcon()
                if name == "Sprites":
                    icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[name], ChildSource)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[name])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    
                if name == "Sprites" or name == "Sound" or name == "Fonts" or name == "Rooms":
                    QtGui.QTreeWidgetItem(self.Parent[name], QtCore.QStringList(ChildSource[:-4])).setIcon(0,icon) 
                elif name == "Objects" or name == "Scripts":
                    QtGui.QTreeWidgetItem(self.Parent[name], QtCore.QStringList(ChildSource[:-3])).setIcon(0,icon)

                if fillarrays:
                    self.main.Sources[name].append(ChildSource)
        

    def addChild(self, directory, name):
        icon = QtGui.QIcon()
        
        if directory == 'Sprites':
            icon.addPixmap(QtGui.QPixmap(os.path.join(self.Path[directory], name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(os.path.join("Data", self.ImageName[directory])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                
               
        if directory == 'Scripts' or directory == 'Objects':
            QtGui.QTreeWidgetItem(self.Parent[directory], QtCore.QStringList(name)).setIcon(0,icon)
        else:
            QtGui.QTreeWidgetItem(self.Parent[directory], QtCore.QStringList(name[:-4])).setIcon(0,icon) 



class Stellar(QtGui.QMainWindow,QtGui.QTextEdit,QtGui.QTreeWidget, QtGui.QMdiArea):
    
    def __init__(self):
        super(Stellar, self).__init__()
        self.Names = ('Sprites', 'Sound', 'Fonts', 'Scripts', 'Objects', 'Rooms')
        self.Sources = {}
        
        self.subfolders = []
        for i in self.Names:
            self.subfolders.append(i)
        self.subfolders.append('Build')
        
        
        for i in self.Names:
            self.Sources[i] = []
        
        self.initUI()
        
    def initUI(self):
        
        #Saving where you opened the program for opening a new window in the future
        self.stellardir = inspect.getfile(inspect.currentframe())
        dirname, filename = os.path.split(os.path.abspath(self.stellardir))
        self.pref = "preferences.pyw"
        self.stellarnew = "Stellar.pyw"
        
        #ACTIONS -------------------------------
        
        def newAction(name, image, trigger, statusTip, shortcut='', enabled=True):
            action = QtGui.QAction(QtGui.QIcon(os.path.join('Data', image)), name, self)
            action.setShortcut(shortcut)
            action.setStatusTip(statusTip)
            action.triggered.connect(trigger)
            action.setEnabled(enabled)
            return action
        
        projectAction = newAction('New Project', 'new.png', self.newproject, 'New Project', 'Ctrl+N')
        
        loadAction = newAction('Open...', 'folder.png', self.openFile, 'Open Game.', 'Ctrl+O')
        saveAction = newAction('Save Game As...', 'save.png', self.savefile, 'Save Game As...', 'Ctrl+Shift+S')
        fsaveAction = newAction('Save', 'save.png', self.fsavefile, 'Save Game', 'Ctrl+S', False)
        
        shareAction = newAction('Share', 'publish.png', self.sharegame, 'Share your creations with the community!')
        buildAction = newAction('Build', 'build.png', self.Build, 'Build game.', '', False)
        playAction = newAction('Run', 'play.png', self.playgame, 'Test your game.', 'F5')
        playDebugAction = newAction('Run in debug mode', 'playdebug.png', self.playgame, 'Test your game on debug mode.', 'F6', False)
        terminalAction = newAction('Terminal', 'terminal.png', self.terminal, 'Open a terminal on your project folder.', 'F1')
        
        spriteAction = newAction('Add Sprite', 'sprite.png', self.addSprite, 'Add a sprite to the game.')
        soundAction = newAction('Add Sound', 'sound.png', self.addSound, 'Add a sound to the game.')
        backgroundAction = newAction('Add Background', 'gif.png', self.addBackground, 'Add a background to the game.')
        fontAction = newAction('Add Font', 'font.png', self.addFont, 'Add a font to the game.')
        objectAction = newAction('Add Object', 'object.png', self.addObject, 'Add an object to the game.')
        roomAction = newAction('Add Room', 'room.png', self.addRoom, 'Add an room to the game.')
        scriptAction = newAction('Add Script', 'addscript.png', self.addScript, 'Add A Script To The Game.')
        
        exitAction = newAction('Exit', 'exit.png', self.close, 'Exit application.', 'Ctrl+Q')
        aboutAction = newAction('About', 'info.png', self.aboutStellar, 'About Stellar.')
        preferencesAction = newAction('Preferences...', 'preferences.png', self.preferencesopen, 'Change Stellar preferences.')

        cascadeAction = newAction('Cascade', 'cascade.png', self.cascadewindows, '', '', True)
        closeallwindowsAction = newAction('Close All', 'closeall.png', self.closeallwindows, '', '', True)
        settabbedAction = newAction('Toggle Tabbed View', 'tabs.png', self.settabbedview, '', '', True)

        expandAction = newAction('Expand Resource Tree', '', self.expandtree, '', '', True)
        collapseAction = newAction('Collapse Resource Tree', '', self.collapsetree, '', '', True)
        
        self.statusBar()

        #MENU BAR --------------------------------------
        menubar = self.menuBar()
        
        def addBar(bar, action):
            if bar == 'menubar':
                self.fileMenu = menubar.addMenu(action[0])
            
            for i in range(1, len(action)):
                if action[i] == '|':
                    if bar == 'menubar':
                        self.fileMenu.addSeparator()
                    elif bar == 'toolbar':
                        self.toolbar.addSeparator()
                else:
                    if bar == 'menubar':
                        self.fileMenu.addAction(action[i])
                    elif bar == 'toolbar': 
                        self.toolbar.addAction(action[i])

        addBar('menubar', ['&File', projectAction, loadAction, '|', fsaveAction, saveAction, '|',\
                                buildAction, shareAction, '|', preferencesAction, '|', exitAction])

        addBar('menubar', ['&Edit', expandAction, collapseAction])

        addBar('menubar', ['&Resources', spriteAction, soundAction, backgroundAction, objectAction,\
                                fontAction, roomAction])
        
        addBar('menubar', ['&Scripts', scriptAction])
        addBar('menubar', ['&Run', playAction, playDebugAction])
        addBar('menubar', ['&Windows', cascadeAction, closeallwindowsAction, '|', settabbedAction])
        addBar('menubar', ['&Help', aboutAction])

        #TOOL BAR --------------------------------------
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable (True)
        
        addBar('toolbar', [ None, projectAction, fsaveAction, loadAction, '|', buildAction, shareAction, '|',\
                                playAction, terminalAction, '|', spriteAction, soundAction, backgroundAction,\
                                fontAction, scriptAction, objectAction, roomAction, '|', aboutAction, ] )

        #Qtree----------------------------------------
        self.tree = TreeWidget(self)

        #QMdiArea--------------------------------------
        self.qmdiarea= QMdiAreaW(self)
        self.qmdiareaview = False
        self.qmdiarea.setTabsClosable(True)
        self.qmdiarea.setTabsMovable(True)
        #self.addScriptsubWindow("hola")

        #WINDOW----------------------------------------
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        
        self.expanded = {'Sprites' : False, 'Sound' : False, 'Fonts' : False, 'Scripts' : False,
                         'Objects' : False, 'Rooms' : False}
        self.fname = "<New game>"
        self.dirname = ''
        self.setTitle(self.fname)
        self.center()
        self.start = Start(self)
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.splitter1.addWidget(self.tree)
        self.splitter1.addWidget(self.qmdiarea)
        self.splitter1.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter1)

    def terminal(self):
        print ("To do")

    def updatetree(self):
        self.tree.clear()
        self.tree.InitParent()
        self.tree.InitChild()

        for key in self.expanded:
            if self.expanded[key]:
                self.tree.expandItem(self.tree.Parent[key])

    def expandtree(self):
        self.tree.expandAll()
        
    def collapsetree(self):
        self.tree.collapseAll()
        
    def cascadewindows(self):
        self.qmdiarea.cascadeSubWindows()
        
    def closeallwindows(self):
        self.qmdiarea.closeAllSubWindows()
        
    def settabbedview(self):
        self.qmdiareaview ^= True

        if self.qmdiareaview:
            self.qmdiarea.setViewMode(self.qmdiarea.TabbedView)
        else:
            self.qmdiarea.setViewMode(self.qmdiarea.SubWindowView)


    def preferencesopen(self):
        prefs = PreferencesDialog(self)
        
    def newproject(self):
        newprojectdialog = NewProjectDialog(self)
        
    def setTitle(self, name):
        self.setWindowTitle('%s - Stellar %s'% (name.replace(".py", ""), cfg.__version__))

    def Build(self):
        print("To do")

    def aboutStellar(self):
        about = QtGui.QMessageBox.information(self, 'About Stellar',
            "<center><b>Stellar</b> is an open-source program inspired in 'Game Maker' for <b>Pygame/Python</b> development.<br/><br/>    The goal is to have a program to design your own games using easy-to-learn drag-and-drop actions and different easy tools for begginers.<br/>    When you become more experienced, you will have the possibilitie of writing and editing your game with the full flexibility given by <b>Python/Pygame</b>.<br/><br/>    This is an uncomplete version, it has almost nothing, but I would love to be helped by anyone interested in the project.<br/><br/>    You are free to distribute the games you create with <b>Stellar</b> in any way you like. You can even sell them.<br/>     This of course assumes that the sprites, images, and sounds you use can be distributed or sold as well.<br/><HR><br/>  You can contribute to the project on our Github:<br/><a href=\'https://github.com/Coppolaemilio/stellar'>Stellar on Git</a></center>", QtGui.QMessageBox.Ok)
            
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, "Exit Stellar", "Save Python File before Exit?",
                                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Yes:
            p = unicode(self.fname)
            d = os.path.basename(p)
            fname = os.path.join(self.dirname, d)
            self.setWindowTitle('{0} - Stellar {1}'.format(d, cfg.__version__))

            with open(fname, 'w') as f:
                data = self.textEdit.toPlainText()
                f.write(data)
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.accept()
        else:
            event.ignore()
            
    def openFile(self):
        self.openProject()
        self.closeallwindows()
        
    def openProject(self, project=None):
        if project == None:
            project = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Game', 
                        '', self.tr("Python files (*.py *.pyw)")))
            
        if project == '':
            return
        if not os.path.isfile(project):
            QtGui.QMessageBox.question(self, "Project doesn't exist",
                "this project doesn't exist or has been removed",
            QtGui.QMessageBox.Ok)
            return
            

        for folder in self.subfolders:
            if not os.path.exists(os.path.join(os.path.dirname(project), folder)):
                QtGui.QMessageBox.question(self, "Project is broken",
                    "Project is broken or doesn't contain important folders",
                    QtGui.QMessageBox.Ok)
                return

        self.dirname = os.path.dirname(project)
        self.fname = os.path.basename(project)
        

        cfg.config.set('stellar', 'recentproject', project.encode('utf-8'))
        cfg.recentproject = project
            
        with open('config.ini', 'w') as configfile:
            cfg.config.write(configfile)
            
        self.setTitle(self.fname)
        self.clearSources()
    
    
    def clearSources(self):
        for i in self.Names:
            self.Sources[i] = []

        self.tree.clear()
        self.tree.InitParent()
        self.tree.InitChild(fillarrays = True)
        self.show()
            
      

    def sharegame(self):
        webbrowser.open("http://www.pygame.org/news.html")
            
    def createProject(self, dirname, file):
        
        project = os.path.join(dirname, file+".py")
        
        if not os.path.exists(dirname):
            if not os.path.isfile(project):
                os.mkdir(dirname)
        
        for subfolder in self.subfolders:
            if not os.path.exists(os.path.join(dirname, subfolder)):
                os.mkdir(os.path.join(dirname, subfolder))

        f = open(project, 'w+')
        f.write('# this file was created with Stellar')
        f.close()

        cfg.config.set('stellar', 'recentproject', project.encode('utf-8'))
        cfg.recentproject = project
        with open('config.ini', 'w') as configfile:
            cfg.config.write(configfile)

        self.setWindowTitle('%s - Stellar %s'% (file.replace(".py", ""), cfg.__version__))
        
        
    def savefile(self):
        project = unicode(QtGui.QFileDialog.getSaveFileName(self, 'Save project as...', 
                            self.dirname, self.tr("Python files (*.py *.pyw)")))

        if project == "":
            return
        else:
            fromDir = self.dirname
            self.fname = os.path.basename(project)+".py"
            self.dirname = project
            self.createProject(self.dirname, self.fname)
            
            for source in self.Sources:
                for file in self.Sources[source]:
                    if not os.path.isfile(os.path.join(self.dirname, source, file)):
                        from_dir = os.path.join(fromDir, source, file)
                        into_dir = os.path.join(self.dirname, source, file)
                        shutil.copy(from_dir, into_dir)

            
    def fsavefile(self):
        print("To do")
 
        
    def playgame(self):
        execfile(os.path.join(self.dirname, self.fname), {})

    def addSource(self, source):
        
        def get_name(source, name):
            number = 0
            prefix = name
            name = prefix + unicode(number)
            while os.path.exists(os.path.join(self.dirname, source, name + ".py")):
                number += 1 
                name = prefix + unicode(number)
            return name
            
        def include_into_project(source, name, path=None):
            
            if source == "Sprites" or source == "Sound" or source == "Fonts":
                if path != os.path.join(self.dirname, source, name):
                    shutil.copy(path, os.path.join(self.dirname, source, name))
                    
            elif source == "Scripts" or source == "Objects":
                f = open(os.path.join(self.dirname, source, name+".py"), 'w')
                f.close()
                
            self.tree.addChild(source,name)
            self.Sources[source].append(name)
        
        
        def add_source(source, prefix):
            name = get_name(source, prefix)
            include_into_project(source, name)
            
            
        files = ""
        if source == "Sprites" or source == "Sound" or source == "Fonts":
            if source == "Sprites":
                files = "Image file (*.png *.gif *.jpg)"
            elif source == "Sounds":
                files = "Sound file (*.ogg *.wav)"
            elif source == "Fonts":
                files = "Font file (*.ttf *.ttc *.fon)"
        else:
            if source == "Scripts":
                add_source(source, "script_")
            
            elif source == "Objects":
                add_source(source, "obj_")
            elif source == "Rooms":
                pass
            elif source == "Backgrounds":
                pass
        
        if files != "":
            location = QtGui.QFileDialog.getOpenFileNames(self, 'Open' + source, 
                    '', self.tr(files))
                    
            if location !='':
                name = os.path.basename(unicode(location[0]))
                include_into_project(source, name, location[0])
        
    
        
    def addSprite(self):
        self.addSource("Sprites")
        
    def addSound(self):  
        self.addSource("Sound")
        
    def addBackground(self):
        self.addSource("Backgrounds")
        
    def addFont(self):
        self.addSource("Fonts")
        
    def addScript(self):
        self.addSource("Scripts")
        
    def addObject(self):
        self.addSource("Objects")
        
    def addRoom(self):
        self.addSource("Rooms")
         

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

      
def main():
    app = QtGui.QApplication(sys.argv)
    st = Stellar()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
