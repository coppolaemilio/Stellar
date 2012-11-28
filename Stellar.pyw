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
import os
import webbrowser
import inspect
import syntax
import platform
import subprocess
import shutil

from PyQt4 import QtCore, QtGui

import cfg
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
                    if name == 'Sprites':
                        self.main.Sprites.append(ChildSource)
                    elif name == 'Sound':
                        self.main.Sound.append(ChildSource)
                    elif name == 'Fonts':
                        self.main.Fonts.append(ChildSource)
                    elif name == 'Scripts':
                        self.main.Scripts.append(ChildSource)
                    elif name == 'Objects':
                        self.main.Objects.append(ChildSource)
                    elif name == 'Rooms':
                        self.main.Rooms.append(ChildSource)
        

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
        self.Sprites=[]
        self.Sound=[]
        self.Fonts=[]
        self.Scripts=[]
        self.Objects=[]
        self.Rooms=[]
        
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
        
        loadAction = newAction('Open...', 'folder.png', self.openfile, 'Open Game.', 'Ctrl+O')
        saveAction = newAction('Save Game As...', 'save.png', self.savefile, 'Save Game As...', 'Ctrl+Shift+S')
        fsaveAction = newAction('Save', 'save.png', self.fsavefile, 'Save Game', 'Ctrl+S', False)
        
        shareAction = newAction('Share', 'publish.png', self.sharegame, 'Share your creations with the community!')
        buildAction = newAction('Build', 'build.png', self.Build, 'Build game.', '', False)
        playAction = newAction('Run', 'play.png', self.playgame, 'Test your game.', 'F5')
        playDebugAction = newAction('Run in debug mode', 'playdebug.png', self.playgame, 'Test your game on debug mode.', 'F6', False)
        
        spriteAction = newAction('Add Sprite', 'sprite.png', self.addsprite, 'Add a sprite to the game.')
        animatedspriteAction = newAction('Add Animated Sprite', 'gif.png', self.addAnimatedSprite, 'Add an animated sprite to the game.')
        soundAction = newAction('Add Sound', 'sound.png', self.addsound, 'Add a sound to the game.')
        fontAction = newAction('Add Font', 'font.png', self.addfont, 'Add a font to the game.')
        objectAction = newAction('Add Object', 'object.png', self.addobject, 'Add an object to the game.')
        roomAction = newAction('Add Room', 'room.png', self.addroom, 'Add an room to the game.')
        scriptAction = newAction('Add Script', 'addscript.png', self.addscript, 'Add A Script To The Game.')
        
        zoominAction = newAction('Zoom In', 'plus.png', self.onZoomInClicked, 'Zoom in the font of the editor.')
        zoomoutAction = newAction('Zoom Out', 'minus.png', self.onZoomOutClicked, 'Zoom out the font of the editor.')
        sfontAction = newAction('Set Font', 'font.png', self.fontdialog, 'Change the font of the text editor.')

        exitAction = newAction('Exit', 'exit.png', self.close, 'Exit application.', 'Ctrl+Q')
        aboutAction = newAction('About', 'info.png', self.aboutStellar, 'About Stellar.')
        preferencesAction = newAction('Preferences...', 'preferences.png', self.preferencesopen, 'Change Stellar preferences.', '', False)

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

        addBar('menubar', ['&Resources', spriteAction, animatedspriteAction, soundAction, objectAction,\
                                fontAction, roomAction])
        
        addBar('menubar', ['&Scripts', scriptAction])
        addBar('menubar', ['&Run', playAction, playDebugAction])
        addBar('menubar', ['&Text Editor', zoominAction, zoomoutAction, sfontAction])
        addBar('menubar', ['&Help', aboutAction])

        #TOOL BAR --------------------------------------
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable (True)
        
        addBar('toolbar', [ None, projectAction, fsaveAction, loadAction, '|', buildAction, shareAction, '|',\
                                playAction, '|', spriteAction, animatedspriteAction, soundAction, fontAction,\
                                scriptAction, objectAction, roomAction, '|', aboutAction, zoominAction, zoomoutAction ] )

        #Qtree----------------------------------------
        self.tree = TreeWidget(self)

        #QMdiArea--------------------------------------
        self.qmdiarea= QMdiAreaW(self)
        #self.addScriptsubWindow("hola")

        #WINDOW----------------------------------------
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.subfolders = ['Sprites', 'Sound', 'Fonts', 'Scripts', 'Objects', 'Rooms', 'Build']
        self.expanded = {'Sprites' : False, 'Sound' : False, 'Fonts' : False, 'Scripts' : False,
                         'Objects' : False, 'Rooms' : False}
        self.fname = "<New game>"
        self.dirname = ''
        self.setWindowTitle('{0} - Stellar {1}'.format(self.fname, cfg.__version__))
        self.center()
        self.start = Start(self)
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.splitter1.addWidget(self.tree)
        self.splitter1.addWidget(self.qmdiarea)
        self.splitter1.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter1)

    def updatetree(self):
        self.tree.clear()
        self.tree.InitParent()
        self.tree.InitChild()

        for key in self.expanded:
            if self.expanded[key]:
                self.tree.expandItem(self.tree.Parent[key])

    def preferencesopen(self):
        print(self.pref)
        execfile(self.pref, {})
        
    def newproject(self):
        newprojectdialog = NewProjectDialog(self)
        

    def Build(self):
        print("To do")

    def aboutStellar(self):
        about = QtGui.QMessageBox.information(self, 'About Stellar',
            "<center><b>Stellar</b> is an open-source program inspired in 'Game Maker' for <b>Pygame/Python</b> development.<br/><br/>    The goal is to have a program to design your own games using easy-to-learn drag-and-drop actions and different easy tools for begginers.<br/>    When you become more experienced, you will have the possibilitie of writing and editing your game with the full flexibility given by <b>Python/Pygame</b>.<br/><br/>    This is an uncomplete version, it has almost nothing, but I would love to be helped by anyone interested in the project.<br/><br/>    You are free to distribute the games you create with <b>Stellar</b> in any way you like. You can even sell them.<br/>     This of course assumes that the sprites, images, and sounds you use can be distributed or sold as well.<br/><HR><br/>  You can contribute to the project on our Github:<br/><a href=\'https://github.com/Coppolaemilio/stellar'>Stellar on Git</a></center>", QtGui.QMessageBox.Ok)
            
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, "Exit Stellar", "Save Python File before Exit?",
                                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)

        if reply == QtGui.QMessageBox.Yes:
            p = str(self.fname)
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
            
    def openfile(self):
        project = str(QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Game', 
                            '', self.tr("Python files (*.py *.pyw)")))

        if project == '':
            return
        if not os.path.isfile(project):
            QtGui.QMessageBox.question(self, "Project doesn't exist",
                "This project doesn't exist or has been removed",
                QtGui.QMessageBox.Ok)
            return
            

        for subfolder in self.subfolders:

            if not os.path.exists(os.path.join(os.path.dirname(project), subfolder)):

                QtGui.QMessageBox.question(self, "Project is broken",
                    "Project is broken or doesn't contain important folders",
                    QtGui.QMessageBox.Ok)
                return

        self.dirname = os.path.dirname(project)

        self.fname = os.path.basename(project)



        cfg.config.set('stellar', 'recentproject', project)

        with open('config.ini', 'wb') as configfile:

            cfg.config.write(configfile)
            
        self.setWindowTitle('%s - Stellar %s'% (self.fname, cfg.__version__))


        self.Sprites=[]
        self.Sound=[]
        self.Fonts=[]
        self.Scripts=[]
        self.Objects=[]
        self.Rooms=[]

        self.tree.clear()
        self.tree.InitParent()
        self.tree.InitChild(fillarrays = True)
        self.show()

    def sharegame(self):
        webbrowser.open("http://www.pygame.org/news.html")
            
    def savefile(self):
        project = str(QtGui.QFileDialog.getSaveFileName(self, 'Save project as...', 

                            self.dirname, self.tr("Python files (*.py *.pyw)")))

        if project == "":
            return
        else:
            fromDir = self.dirname
            self.fname = os.path.basename(project)
            self.dirname = os.path.dirname(project)

            if not os.path.exists(self.dirname):
                os.mkdir(self.dirname)
                
            for subfolder in self.subfolders:
                if not os.path.exists(os.path.join(self.dirname, subfolder)):

                    os.mkdir(os.path.join(self.dirname, subfolder))

            f = open(os.path.join(self.dirname, self.fname), 'w+')

            f.write('# This file was created with Stellar')

            f.close()

            cfg.config.set('stellar', 'recentproject', project)

            with open('config.ini', 'wb') as configfile:

                cfg.config.write(configfile)

            self.setWindowTitle('%s - Stellar %s'% (os.path.basename(project), cfg.__version__))

            self.addsprite(self.Sprites, fromDir)
            self.addsound(self.Sound, fromDir)
            self.addfont(self.Fonts, fromDir)
            self.addscript(self.Scripts, fromDir)
            self.addobject(self.Objects, fromDir)
            self.addroom(self.Rooms, fromDir)
            
    def fsavefile(self):
        print("To do")

    def onZoomInClicked(self):
        self.textEdit.zoomIn(+1)

    def onZoomOutClicked(self):
        self.textEdit.zoomOut(+1)       
        
    def playgame(self):
        execfile(os.path.join(self.dirname, self.fname), {})

    def fontdialog(self):

        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def addsprite(self, asprite = False, fromDir = None):
        if asprite is False:
            self.asprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
            if self.asprite !='':
                for sprite in self.asprite:
                    d = os.path.basename(str(sprite))
                    if not os.path.exists(os.path.join(self.dirname, 'Sprites', d)):
                        if d[:4]=='spr_':
                            shutil.copy(sprite, os.path.join('Sprites', d))
                            self.tree.addChild("Sprites", d)
                            self.Sprites.append(d)
                        else:
                            shutil.copy(sprite, os.path.join(self.dirname, 'Sprites', 'spr_{0}'.format(d)))
                            self.tree.addChild("Sprites", 'spr_' + d)
                            self.Sprites.append('spr_' + d)
 
        else:
            for sprite in asprite:
                if not os.path.isfile(os.path.join(self.dirname, 'Sprites', sprite)):
                    shutil.copy(os.path.join(fromDir, 'Sprites', sprite), os.path.join(self.dirname, 'Sprites', sprite))

    def addAnimatedSprite(self, aGIFsprite = False, fromDir = None):
        if aGIFsprite is False:
            self.aGIFsprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Animated Sprite(s)', 
                    '', self.tr("Image file (*.png *.gif *.jpg)"))
            
            if self.aGIFsprite !='':
                for sprite in self.aGIFsprite:
                    d = os.path.basename(str(sprite))
                    if not os.path.exists(os.path.join(self.dirname, 'Sprites', d)):
                        if d[:4]=='spr_':
                            shutil.copy(sprite,os.path.join(self.dirname, 'Sprites', d))
                            self.tree.addChild('Sprites', d)
                            self.Sprites.append(d)
                        else:
                            shutil.copy(sprite,os.path.join(self.dirname, 'Sprites', 'spr_{0}'.format(d)))
                            self.tree.addChild('Sprites', 'spr_' + d)
                            self.Sprites.append('spr_' + d)

        else:
            for sprite in aGIFsprite:
                if not os.path.isfile(os.path.join(self.dirname, 'Sprites', sprite)):
                    shutil.copy(os.path.join(fromDir, 'Sprites', sprite), os.path.join(self.dirname, 'Sprites', sprite))

    def addsound(self, asound = False, fromDir = None):
        if asound is False:
            self.asound = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sound(s)', 
                    '', self.tr("Sound file (*.ogg *.wav)"))
            
            if self.asound !='':
                for sound in self.asound:
                    d = os.path.basename(str(sound))
                    if not os.path.exists(os.path.join(self.dirname, 'Sound', d)):
                        if d[:4]=='snd_':
                            shutil.copy(sound,os.path.join(self.dirname, 'Sound', d))
                            self.tree.AddSndChild('Sound', d)
                            self.Sound.append(d)
                        else:
                            shutil.copy(sound,os.path.join(self.dirname, 'Sound', 'snd_{0}'.format(d)))
                            self.tree.addChild('Sound', 'snd_'+d)
                            self.Sound.append('snd_' + d)

        else:
            for sound in asound:
                if not os.path.isfile(os.path.join(self.dirname, 'Sound', sound)):
                    shutil.copy(os.path.join(fromDir, 'Sound', sound), os.path.join(self.dirname, 'Sound', sound))

    def addfont(self, afont = False, fromDir = None):
        if afont is False:
            self.afont = QtGui.QFileDialog.getOpenFileNames(self, 'Open Font(s)', 
                    '', self.tr("Font file (*.ttf *.ttc *.fon)"))
            
            if self.afont !='':
                for font in self.afont:
                    d = os.path.basename(str(font))
                    f = os.path.splitext(d)[0]
                    if not os.path.exists(os.path.join(self.dirname, 'Fonts', d)):
                        if d[:5]=='font_':
                            shutil.copy(font,os.path.join(self.dirname, 'Fonts', d))
                            self.tree.addChild('Fonts', d)
                            self.Fonts.append(d)
                        else:
                            shutil.copy(font,os.path.join(self.dirname, 'Fonts', 'font_{0}'.format(d)))
                            self.tree.addChild('Fonts', 'font_'+d)
                            self.Fonts.append('font_' + d)

        else:
            for font in afont:
                if not os.path.isfile(os.path.join(self.dirname, 'Fonts', font)):
                    shutil.copy(os.path.join(fromDir, 'Fonts', font), os.path.join(self.dirname, 'Fonts', font))

    def addscript(self, ascript = False, fromDir = None):
        if ascript is False:
            script = "script_"
            scriptnumber = 0
            TmpScript = script + str(scriptnumber)
            while os.path.exists(os.path.join(self.dirname, 'Scripts', "{0}.py".format(TmpScript))):
                scriptnumber += 1 
                TmpScript = script + str(scriptnumber)
            f = open(os.path.join(self.dirname, 'Scripts', "{0}.py".format(TmpScript)),'w')
            f.close()
            self.tree.addChild('Scripts',TmpScript)
            self.Scripts.append(TmpScript)
        else:
            for script in ascript:
                if not os.path.isfile(os.path.join(self.dirname, 'Scripts', script)):
                    shutil.copy(os.path.join(fromDir, 'Scripts', script), os.path.join(self.dirname, 'Scripts', script))

    def addobject(self, aobject = False, fromDir = None):
        if aobject is False:
            object = "obj_"
            objectnumber = 0
            TmpObject= object + str(objectnumber)
            while os.path.exists(os.path.join(self.dirname, 'Objects', "{0}.py".format(TmpObject))):
                objectnumber += 1 
                TmpObject = object + str(objectnumber)
            f = open(os.path.join(self.dirname, 'Objects', "{0}.py".format(TmpObject)),'w')
            f.close()
            self.tree.addChild('Objects', TmpObject)
            self.Objects.append(TmpObject)
        else:
            for object in aobject:
                if not os.path.isfile(os.path.join(self.dirname, 'Objects', object)):
                    shutil.copy(os.path.join(fromDir, 'Objects', object), os.path.join(self.dirname, 'Objects', object))

    def addroom(self, aroom = None, fromDir = None):
        pass

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
