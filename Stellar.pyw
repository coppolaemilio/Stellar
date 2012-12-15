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
from tree import TreeWidget


class QMdiAreaW(QtGui.QMdiArea):
    def __init__(self, main):
        super(QMdiAreaW, self).__init__(main)
        self.setBackground (QtGui.QBrush(QtGui.QPixmap(os.path.join("Data", "background.png"))))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)



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
        
        actions = self.initActions()
        self.statusBar()
        self.initBars(actions)
        
        #Qtree----------------------------------------
        self.tree = TreeWidget(self)

        #QMdiArea--------------------------------------
        self.qmdiarea= QMdiAreaW(self)
        self.qmdiareaview = False
        self.qmdiarea.setTabsClosable(True)
        self.qmdiarea.setTabsMovable(True)
        
        self.initWindow()

    def initWindow(self):
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
        
    def initActions(self):
        def newAction(name, image, trigger, statusTip, shortcut='', enabled=True):
            action = QtGui.QAction(QtGui.QIcon(os.path.join('Data', image)), name, self)
            action.setShortcut(shortcut)
            action.setStatusTip(statusTip)
            action.triggered.connect(trigger)
            action.setEnabled(enabled)
            return action
            
        action={}
        action['project'] = newAction('New Project', 'new.png', self.newproject, 'New Project', 'Ctrl+N')
        
        action['load'] = newAction('Open...', 'folder.png', self.openFile, 'Open Game.', 'Ctrl+O')
        action['save'] = newAction('Save Game As...', 'save.png', self.savefile, 'Save Game As...', 'Ctrl+Shift+S')
        action['fsave'] = newAction('Save', 'save.png', self.fsavefile, 'Save Game', 'Ctrl+S', False)
        
        action['share'] = newAction('Share', 'publish.png', self.sharegame, 'Share your creations with the community!')
        action['build'] = newAction('Build', 'build.png', self.Build, 'Build game.', '', False)
        action['play'] = newAction('Run', 'play.png', self.playgame, 'Test your game.', 'F5')
        action['playDebug'] = newAction('Run in debug mode', 'playdebug.png', self.playgame, 'Test your game on debug mode.', 'F6', False)
        action['terminal'] = newAction('Terminal', 'terminal.png', self.terminal, 'Open a terminal on your project folder.', 'F1')
        
        action['sprite'] = newAction('Add Sprite', 'sprite.png', self.addSprite, 'Add a sprite to the game.')
        action['sound'] = newAction('Add Sound', 'sound.png', self.addSound, 'Add a sound to the game.')
        action['background'] = newAction('Add Background', 'gif.png', self.addBackground, 'Add a background to the game.')
        action['font'] = newAction('Add Font', 'font.png', self.addFont, 'Add a font to the game.')
        action['object'] = newAction('Add Object', 'object.png', self.addObject, 'Add an object to the game.')
        action['room'] = newAction('Add Room', 'room.png', self.addRoom, 'Add an room to the game.')
        action['script'] = newAction('Add Script', 'addscript.png', self.addScript, 'Add A Script To The Game.')
        
        action['exit'] = newAction('Exit', 'exit.png', self.close, 'Exit application.', 'Ctrl+Q')
        action['about'] = newAction('About', 'info.png', self.aboutStellar, 'About Stellar.')
        action['preferences'] = newAction('Preferences...', 'preferences.png', self.preferencesopen, 'Change Stellar preferences.')

        action['cascade'] = newAction('Cascade', 'cascade.png', self.cascadewindows, '', '', True)
        action['closeallwindows'] = newAction('Close All', 'closeall.png', self.closeallwindows, '', '', True)
        action['settabbed'] = newAction('Toggle Tabbed View', 'tabs.png', self.settabbedview, '', '', True)

        action['expand'] = newAction('Expand Resource Tree', '', self.expandtree, '', '', True)
        action['collapse'] = newAction('Collapse Resource Tree', '', self.collapsetree, '', '', True)
        
        return action
        
    def initBars(self, dictActions):
        
        def getAction(dictActions, action):
            for key in dictActions.keys():
                if action == key:
                    return dictActions[key]
        
        
        def addBar(bar, action):
            if action[0] != None:
                bar = bar.addMenu(action[0])
            for i in range(1, len(action)):
                if action[i] == '|':
                    bar.addSeparator()
                else:
                    action[i] = getAction(dictActions, action[i])
                    bar.addAction(action[i])
                    
        
        menubar = self.menuBar()
        addBar(menubar, ['&File', 'project', 'load', '|', 'fsave', 'save', '|',\
                                'build', 'share', '|', 'preferences', '|', 'exit'])

        addBar(menubar, ['&Edit', 'expand', 'collapse'])

        addBar(menubar, ['&Resources', 'sprite', 'sound', 'background', 'object',\
                                'font', 'script', 'room'])
        
        addBar(menubar, ['&Run', 'play', 'playDebug'])
        addBar(menubar, ['&Windows', 'cascade', 'closeallwindows', '|', 'settabbed'])
        addBar(menubar, ['&Help', 'about'])

        #TOOL BAR --------------------------------------
        toolbar = self.addToolBar('Toolbar')
        toolbar.setMovable (True)
        
        addBar(toolbar, [ None, 'project', 'fsave', 'load', '|', 'build', 'share', '|',\
                                'play', 'terminal', '|', 'sprite', 'sound', 'background',\
                                'font', 'script', 'object', 'room', '|', 'about' ] )

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
            elif not os.path.isfile(project):
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
        else:
            project = project + ".py"
            
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

            cfg.config.set('stellar', 'recentproject', project.encode('utf-8'))
            cfg.recentproject = project
            with open('config.ini', 'w') as configfile:
                cfg.config.write(configfile)

            
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
