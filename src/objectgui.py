#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
#
# This file is part of Stellar.
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



from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import shutil
from PyQt4 import QtGui, QtCore


class ExecuteScriptD(QtGui.QDialog):
    def __init__(self, parent, tree):
        super(ExecuteScriptD, self).__init__(parent.main)
        self.parent = parent       
        self.tree = tree
        
                
        self.initUI()
        
    def initUI(self):
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.image = QtGui.QLabel()
        self.image.setPixmap(QtGui.QPixmap(os.path.join('Data', 'Actions', 'executescript.png')))

        self.apptoself = QtGui.QRadioButton("self")
        self.apptoself.toggle()
        self.apptoself.clicked.connect(self.disable)
        self.apptoother = QtGui.QRadioButton("other")
        self.apptoother.clicked.connect(self.disable)
        self.apptoobject = QtGui.QRadioButton("object:")
        self.apptoobject.clicked.connect(self.enable)
        self.objectcombo = QtGui.QComboBox()
        self.objectcombo.setEnabled(False)
        self.objectcombo.addItem('self')
        self.objectcombo.addItems(self.tree.main.Sources["Objects"])
        
        self.AppliesFrame = QtGui.QGroupBox("Applies to")
        self.Applieslayout = QtGui.QGridLayout()
        self.Applieslayout.addWidget(self.apptoself,0,0)
        self.Applieslayout.addWidget(self.apptoother,1,0)
        self.Applieslayout.addWidget(self.apptoobject,2,0)
        self.Applieslayout.addWidget(self.objectcombo,2,2)
        self.AppliesFrame.setLayout(self.Applieslayout)

        self.frame = QtGui.QGroupBox()
        self.framelayout = QtGui.QGridLayout()
        self.labelscript = QtGui.QLabel("Script:")
        self.scriptcombobox = QtGui.QComboBox()
        self.scriptcombobox.addItem("No Script")
        self.scriptcombobox.addItems(self.tree.main.Sources["Scripts"])
        self.labelarg0 = QtGui.QLabel("argument0")
        self.labelarg1 = QtGui.QLabel("argument1")
        self.labelarg2 = QtGui.QLabel("argument2")
        self.labelarg3 = QtGui.QLabel("argument3")
        self.labelarg4 = QtGui.QLabel("argument4")
        self.lineedit0 = QtGui.QLineEdit()
        self.lineedit1 = QtGui.QLineEdit()
        self.lineedit2 = QtGui.QLineEdit()
        self.lineedit3 = QtGui.QLineEdit()
        self.lineedit4 = QtGui.QLineEdit()
        
        self.framelayout.addWidget(self.labelscript,0,0)
        self.framelayout.addWidget(self.scriptcombobox,0,1)
        self.framelayout.addWidget(self.labelarg0,1,0)
        self.framelayout.addWidget(self.lineedit0,1,1)
        self.framelayout.addWidget(self.labelarg1,2,0)
        self.framelayout.addWidget(self.lineedit1,2,1)
        self.framelayout.addWidget(self.labelarg2,3,0)
        self.framelayout.addWidget(self.lineedit2,3,1)
        self.framelayout.addWidget(self.labelarg3,4,0)
        self.framelayout.addWidget(self.lineedit3,4,1)
        self.framelayout.addWidget(self.labelarg4,5,0)
        self.framelayout.addWidget(self.lineedit4,5,1)
        self.frame.setLayout(self.framelayout)
        

        self.okcancel = QtGui.QFrame()
        self.okcancelly = QtGui.QHBoxLayout()
        self.Btnok = QtGui.QPushButton("OK")
        self.Btnok.setIcon(QtGui.QIcon(os.path.join('Data','accept.png')))
        self.Btnok.clicked.connect(self.ok)
        self.Btncancel = QtGui.QPushButton("Cancel")
        self.Btncancel.setIcon(QtGui.QIcon(os.path.join('Data','cancel.png')))
        self.Btncancel.clicked.connect(self.cancel)
        self.okcancelly.addWidget(self.Btnok)
        self.okcancelly.addWidget(self.Btncancel)
        self.okcancel.setLayout(self.okcancelly)
         
        
        self.ContainerGrid.addWidget(self.image, 0, 0,1,1)
        self.ContainerGrid.addWidget(self.AppliesFrame, 0, 1,2,6)
        self.ContainerGrid.addWidget(self.frame,2,0,6,7)
        self.ContainerGrid.addWidget(self.okcancel,8,0,1,7)

        #self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.setWindowTitle("Execute Script")
        self.resize(316,347)

        self.show()  

    def ok(self):
        if self.scriptcombobox.currentText()=="No Script":
            return
        else:
            scripttoexecute = self.scriptcombobox.currentText()[:-3]
            self.parent.OkActionScript(scripttoexecute)
            self.close()

    def cancel(self):
        self.close()

    def enable(self):
        self.objectcombo.setEnabled(True)

        
    def disable(self):
        self.objectcombo.setEnabled(False)

        
class Events(QtGui.QDialog):
    def __init__(self, parent):
        super(Events, self).__init__(parent.main)
        self.parent = parent       
                
        self.initUI()
        

    def initUI(self):
        self.ContainerGrid = QtGui.QGridLayout(self)
        

        self.btn_Create = QtGui.QPushButton('Create')
        self.btn_Create.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'create.png')))
        self.btn_Create.clicked.connect(self.addEvent_Create)
        
        self.btn_Mouse = QtGui.QPushButton('Mouse')
        self.btn_Mouse.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'mouse.png')))
        self.btn_Mouse.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.btn_Mouse.clicked.connect(self.on_mouse_menu)
        # create context menu
        self.popMenuMouse = QtGui.QMenu(self)
        self.popMenuMouse.addAction(QtGui.QAction('Left button', self))
        self.popMenuMouse.addAction(QtGui.QAction('Right button', self))    
        self.popMenuMouse.addAction(QtGui.QAction('Middle button', self))  
        self.popMenuMouse.addSeparator()
        self.popMenuMouse.addAction(QtGui.QAction('No button', self))  
        self.popMenuMouse.addSeparator()
        self.popMenuMouse.addAction(QtGui.QAction('Left pressed', self))
        self.popMenuMouse.addAction(QtGui.QAction('Right pressed', self))
        self.popMenuMouse.addAction(QtGui.QAction('Middle pressed', self))
        self.popMenuMouse.addSeparator()    
        self.popMenuMouse.addAction(QtGui.QAction('Left released', self))
        self.popMenuMouse.addAction(QtGui.QAction('Right released', self))
        self.popMenuMouse.addAction(QtGui.QAction('Middle released', self))
        self.popMenuMouse.addSeparator()
        self.popMenuMouse.addAction(QtGui.QAction('Mouse enter', self))
        self.popMenuMouse.addAction(QtGui.QAction('Mouse leave', self))
        self.popMenuMouse.addSeparator()
        self.popMenuMouse.addAction(QtGui.QAction('Mouse wheel up', self))
        self.popMenuMouse.addAction(QtGui.QAction('Mouse wheel down', self))
        self.popMenuMouse.addSeparator()
        self.globalMenuMouse = self.popMenuMouse.addMenu("&Global mouse")
        self.globalMenuMouse.addAction(QtGui.QAction('Global left button', self))
        self.globalMenuMouse.addAction(QtGui.QAction('Global right button', self))
        self.globalMenuMouse.addAction(QtGui.QAction('Global middle button', self))
        self.globalMenuMouse.addSeparator()
        self.globalMenuMouse.addAction(QtGui.QAction('Global left pressed', self))
        self.globalMenuMouse.addAction(QtGui.QAction('Global right pressed', self))
        self.globalMenuMouse.addAction(QtGui.QAction('Global middle pressed', self))
        self.globalMenuMouse.addSeparator()
        self.globalMenuMouse.addAction(QtGui.QAction('Global left released', self))
        self.globalMenuMouse.addAction(QtGui.QAction('Global right released', self))
        self.globalMenuMouse.addAction(QtGui.QAction('Global middle released', self))      


        self.btn_Destroy = QtGui.QPushButton('Destroy')
        self.btn_Destroy.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'destroy.png')))
        self.btn_Destroy.clicked.connect(self.addEvent_Destroy)

        self.btn_Other = QtGui.QPushButton('Other')
        self.btn_Other.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'other.png')))

        self.btn_Alarm = QtGui.QPushButton('Alarm')
        self.btn_Alarm.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'alarm.png')))
        self.btn_Alarm.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.btn_Alarm.clicked.connect(self.on_context_menu)
        # create context menu
        self.popMenu = QtGui.QMenu(self)
        self.popMenu.addAction(QtGui.QAction('Alarm 0', self))
        self.popMenu.addAction(QtGui.QAction('Alarm 1', self))    
        self.popMenu.addAction(QtGui.QAction('Alarm 2', self))    
        self.popMenu.addAction(QtGui.QAction('Alarm 3', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 4', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 5', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 6', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 7', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 8', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 9', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 10', self)) 
        self.popMenu.addAction(QtGui.QAction('Alarm 11', self)) 
        
        self.btn_Draw = QtGui.QPushButton('Draw')
        self.btn_Draw.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'draw.png')))
        self.btn_Draw.clicked.connect(self.addEvent_Draw)


        self.btn_Step = QtGui.QPushButton('Step')
        self.btn_Step.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'step.png')))
        self.btn_Step.clicked.connect(self.addEvent_Step)

        self.btn_KeyPress = QtGui.QPushButton('Key Press')

        self.btn_Collision = QtGui.QPushButton('Collision')
        self.btn_Collision.clicked.connect(self.addEvent_Collision)

        self.btn_Collision.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'collision.png')))

        self.btn_KeyReleased = QtGui.QPushButton('Key Released')

        self.btn_Joystick = QtGui.QPushButton('Joystick')
        self.btn_Joystick.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'joystick.png')))

        self.btn_Keyboard = QtGui.QPushButton('Keyboard')
        self.btn_Keyboard.setIcon(QtGui.QIcon(os.path.join('Data', 'Events', 'keyboard.png')))
        
        self.btn_Cancel = QtGui.QPushButton('Cancel')
        self.btn_Cancel.setIcon(QtGui.QIcon(os.path.join('Data', 'cancel.png')))
        self.btn_Cancel.clicked.connect(self.close)

        spacerItem = QtGui.QSpacerItem(50, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        
        self.CancelFrame = QtGui.QFrame()
        self.cancellayout = QtGui.QHBoxLayout()
        self.cancellayout.addItem(spacerItem)
        self.cancellayout.addWidget(self.btn_Cancel)
        self.cancellayout.addItem(spacerItem)
        self.CancelFrame.setLayout(self.cancellayout)     

        

        self.ContainerGrid.addWidget(self.btn_Create, 0, 0)
        self.ContainerGrid.addWidget(self.btn_Mouse, 0, 1)
        self.ContainerGrid.addWidget(self.btn_Destroy, 1, 0)
        self.ContainerGrid.addWidget(self.btn_Other, 1, 1)
        self.ContainerGrid.addWidget(self.btn_Alarm, 2, 0)
        self.ContainerGrid.addWidget(self.btn_Draw, 2, 1)
        self.ContainerGrid.addWidget(self.btn_Step, 3, 0)
        self.ContainerGrid.addWidget(self.btn_KeyPress, 3, 1)
        self.ContainerGrid.addWidget(self.btn_Collision, 4, 0)
        self.ContainerGrid.addWidget(self.btn_KeyReleased, 4, 1)
        self.ContainerGrid.addWidget(self.btn_Joystick, 5, 0)
        self.ContainerGrid.addWidget(self.btn_Keyboard, 5, 1)
        self.ContainerGrid.addWidget(self.CancelFrame, 7, 0,1,2)
        

        #self.setWindowIcon(QtGui.QIcon(os.path.join('Data', 'icon.png')))
        self.setWindowTitle("Choose the Event to add")
        self.resize(240,100)

        self.show()  
           
    def addEvent_Create(self):
        self.parent.AddToEventList("Create")
        self.close()

    def addEvent_Step(self):
        self.parent.AddToEventList("Step")
        self.close()

    def addEvent_Destroy(self):
        self.parent.AddToEventList("Destroy")
        self.close()

    def addEvent_Collision(self):
        self.parent.AddToEventList("Collision")
        self.close()

    def addEvent_Draw(self):
        self.parent.AddToEventList("Draw")
        self.close()
        
    def on_context_menu(self):
        # show context menu
        self.pos = QtGui.QCursor.pos()
        self.popMenu.exec_(self.pos)
        
    def on_mouse_menu(self):
        # show context menu
        self.pos = QtGui.QCursor.pos()
        self.popMenuMouse.exec_(self.pos)        

class ObjectGUI(QtGui.QWidget):
    def __init__(self, main, FileName, dirname, tree):
        super(ObjectGUI, self).__init__()

        self.main = main
        self.dirname = dirname
        self.FileName = FileName
        self.tree = tree
        self.extension = "py"


        
        self.initUI()



    def initUI(self):
        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)

        
        self.LblName = QtGui.QLabel('Name:')
        self.nameEdit = QtGui.QLineEdit(self.FileName)
        self.BnewSprite = QtGui.QPushButton("New")
        self.BeditSprite = QtGui.QPushButton("Edit")
        self.SpriteCombo = QtGui.QComboBox()
        self.SpriteCombo.addItem('<no sprite>')
        self.SpriteCombo.activated[str].connect(self.changeSprite)
        
        
        #self.SpriteCombo.addItems(self.tree.main.Sources["Sprites"][:-3])
        self.SpriteFrame = QtGui.QGroupBox("Sprite")
        
        self.spritelayout = QtGui.QGridLayout()
        self.spritelayout.setMargin (8)
        self.spritelayout.addWidget(self.SpriteCombo,0,0,1,2)
        self.spritelayout.addWidget(self.BnewSprite,1,0)
        self.spritelayout.addWidget(self.BeditSprite,1,1)
        self.SpriteFrame.setLayout(self.spritelayout)

        
        self.NameFrame = QtGui.QFrame()
        self.namelayout = QtGui.QGridLayout()
        self.namelayout.setMargin (0)
        self.namelayout.addWidget(self.LblName,0,0)
        self.namelayout.addWidget(self.nameEdit,0,1)
        self.namelayout.addWidget(self.SpriteFrame,1,0,1,2)
        self.NameFrame.setLayout(self.namelayout)

        
        self.cbvisible = QtGui.QCheckBox('Visible', self)
        self.cbsolid = QtGui.QCheckBox('Solid', self)
        self.cbpersis = QtGui.QCheckBox('Persistent', self)
        self.LblDepth = QtGui.QLabel('Depth:')
        self.depthEdit = QtGui.QLineEdit("0")
        self.LblParent = QtGui.QPushButton("Parent:")
        self.ParentEdit = QtGui.QComboBox()
        self.LblMask = QtGui.QPushButton("Mask:")
        self.MaskEdit = QtGui.QComboBox()
        self.Btninfo = QtGui.QPushButton("Show Information")
        self.Btninfo.setIcon(QtGui.QIcon(os.path.join('Data', 'info.png')))
        self.Btnok = QtGui.QPushButton("OK")
        self.Btnok.setIcon(QtGui.QIcon(os.path.join('Data','accept.png')))
        self.Btnok.clicked.connect(self.ok)
        self.eventstree = QtGui.QTreeWidget()
        self.eventstree.setHeaderLabel("Events")
        self.connect(self.eventstree, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"),self.readObjectActions)

        self.events = ["Create", "Step", "Destroy", "Collision", "Draw"]
        
        self.actionstree = QtGui.QTreeWidget()
        self.actionstree.setHeaderLabel("Actions")
        self.Btnaddevent = QtGui.QPushButton("Add Event")
        self.Btnaddevent.clicked.connect(self.AddEvent)
        self.Btndelete = QtGui.QPushButton("Delete")
        self.Btndelete.clicked.connect(self.DeleteEvent)
        self.Btnchange = QtGui.QPushButton("Change")
        self.Btnchange.clicked.connect(self.AddEvent)

        

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)


        self.FirstWidget = QtGui.QWidget()
        self.FirstGrid = QtGui.QGridLayout()
        self.FirstGrid.addWidget(self.NameFrame, 0, 0, 1, 2)
        self.FirstGrid.addWidget(self.SpriteFrame, 1, 0, 1, 2)
        self.FirstGrid.addWidget(self.cbvisible, 2, 0)
        self.FirstGrid.addWidget(self.cbsolid, 2, 1)
        self.FirstGrid.addWidget(self.cbpersis, 3, 0)
        self.FirstGrid.addWidget(self.LblDepth, 4, 0)
        self.FirstGrid.addWidget(self.depthEdit, 4, 1)
        self.FirstGrid.addWidget(self.LblParent, 5, 0)
        self.FirstGrid.addWidget(self.ParentEdit, 5, 1)
        self.FirstGrid.addWidget(self.LblMask, 6, 0)
        self.FirstGrid.addWidget(self.MaskEdit, 6, 1)
        self.FirstGrid.addItem(spacerItem)
        self.FirstGrid.addWidget(self.Btninfo, 7, 0, 1, 2)
        self.FirstGrid.addWidget(self.Btnok, 8, 0,1,2)
        self.FirstWidget.setLayout(self.FirstGrid)
        

        #---
        self.SecondWidget = QtGui.QWidget()
        self.SecondGrid = QtGui.QGridLayout()
        self.SecondGrid.setHorizontalSpacing(0)
        self.SecondGrid.addWidget(self.eventstree, 0, 0, 7, 2)
        self.SecondGrid.addWidget(self.Btnaddevent,    7, 0, 1, 2)
        self.SecondGrid.addWidget(self.Btndelete,      8, 0)
        self.SecondGrid.addWidget(self.Btnchange,      8, 1)
        self.SecondWidget.setLayout(self.SecondGrid)

        #---
        self.ThirdWidget = QtGui.QWidget()
        self.ThirdGrid = QtGui.QGridLayout()
        self.ThirdGrid.setHorizontalSpacing(0)
        self.ThirdGrid.addWidget(self.actionstree, 0, 0, 9, 2)
        self.ThirdWidget.setLayout(self.ThirdGrid)


        self.ActionCombo = QtGui.QComboBox()
        self.ActionCombo.addItem('Code')
        
        self.actions = ['Execute code', 'Execute script', 'Comment']
        self.exCodeAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'Actions', 'executecode.png')), 'Execute Code', self)
        self.exCodeAction.triggered.connect(self.AddActionCode)
        self.exScriptAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'Actions', 'executescript.png')), 'Execute Script', self)
        self.exScriptAction.triggered.connect(self.AddActionScript)
        self.commentAction = QtGui.QAction(QtGui.QIcon(os.path.join('Data', 'Actions', 'comment.png')), 'Comment', self)
        self.commentAction.triggered.connect(self.AddActionComment)
        
        self.actionToolbar = QtGui.QToolBar('Script Toolbar', orientation=QtCore.Qt.Vertical)
        self.actionToolbar.addAction(self.exCodeAction)
        self.actionToolbar.addAction(self.exScriptAction)
        self.actionToolbar.addAction(self.commentAction)

        
        #---


        self.objectsplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.objectsplitter.addWidget(self.FirstWidget)
        self.objectsplitter.addWidget(self.SecondWidget)
        self.objectsplitter.addWidget(self.ThirdWidget)
        self.objectsplitter.addWidget(self.actionToolbar)
        self.objectsplitter.setStretchFactor(1, 1)
        

        self.ContainerGrid.addWidget(self.objectsplitter)
        self.setLayout(self.ContainerGrid)

        self.refreshSprites()
        self.readObjectEvents()
        
    def refreshSprites(self):
        self.SpriteCombo.clear()
        self.SpriteCombo.addItem('<no sprite>')
        for sprite in self.tree.main.Sources["Sprites"]:
            self.SpriteCombo.addItem(sprite[:-4])

    def changeSprite(self,newsprite):
        print (newsprite)
        objectfile = open(os.path.join(self.dirname,"Objects",self.FileName+".py"), "r")
        lines = objectfile.readlines()
        objectfile.close()
        f = open(os.path.join(self.dirname,"Objects",self.FileName+".py"), 'w')
        for line in lines:  
            if ('<Sprite>' in line):
                f.write('<Sprite>'+newsprite+"\n") 
            else:
                f.write(line)
        f.close()
    
    def readObjectEvents(self):
        objectfile = open(os.path.join(self.dirname,"Objects",self.FileName+".py"), "r")
        lines = objectfile.readlines()
        objectfile.close()
        self.ActionNumber=0
        self.actionstree.clear()
        for line in lines:
            if ('<Sprite>' in line):
                line = line.replace("\n",">")
                line = line.split(">")
                index = self.SpriteCombo.findText(line[1])
                if index==-1:
                    #QtGui.QMessageBox.warning(self, "Error.", 'The sprite named "'+line[1]+'" does not exist.',QtGui.QMessageBox.Ok)
                    self.SpriteCombo.setCurrentIndex(0)
                else:
                    self.SpriteCombo.setCurrentIndex (index)
            #Events
            elif ('def event_create' in line ):
                self.AddToEventList("Create")
                
            elif('def event_step' in line):
                self.AddToEventList("Step")

            elif('def event_destroy' in line):
                self.AddToEventList("Destroy")
        self.readObjectActions()
    def readObjectActions(self):
        #Opens and read the object information           
        objectfile = open(os.path.join(self.dirname,"Objects",self.FileName+".py"), "r")
        lines = objectfile.readlines()
        objectfile.close()
        self.ActionNumber=0
        self.actionstree.clear()
        for line in lines:
            if ('<Actions>' in line):
                self.ActionNumber+=1
            #Actions
            elif('<AddActionComment>' in line):
                line = line.replace('\n','')
                line = line.split('>')
                if self.create.isSelected()==True and self.ActionNumber==1:
                    self.readActionComment(line[1])
                elif self.stepeventree.isSelected()==True and self.ActionNumber==2:
                    self.readActionComment(line[1])
            elif('<AddActionScript>' in line):
                line = line.replace('\n','')
                line = line.split('>')
                if self.create.isSelected()==True and self.ActionNumber==1:
                    self.OkActionScript(line[1])
                elif self.stepeventree.isSelected()==True and self.ActionNumber==2:
                    self.OkActionScript(line[1])
        
    def AddActionCode(self):
        create = QtGui.QTreeWidgetItem(self.actionstree,QtCore.QStringList(self.actions[0]))
        create.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Actions', 'executecode.png')))        

    def AddActionScript(self):
        scriptdialog = ExecuteScriptD(self, self.tree)

    def OkActionScript(self, scriptname):
        scriptactree = QtGui.QTreeWidgetItem(self.actionstree,QtCore.QStringList(self.actions[1]+': '+scriptname+'.'))
        scriptactree.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Actions', 'executescript.png')))

    def AddActionComment(self):
        self.comment = QtGui.QInputDialog.getText(self, "Comment","Comment:", 0)
        self.comment = list(self.comment)
        if not self.comment[0]=="":
            commentree = QtGui.QTreeWidgetItem(self.actionstree,QtCore.QStringList(self.comment[0]))
            commentree.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Actions', 'comment.png')))
    def readActionComment(self, text):
        print (text)
        commentree = QtGui.QTreeWidgetItem(self.actionstree,QtCore.QStringList(text))
        commentree.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Actions', 'comment.png')))
        #commentree.setFont(0, QtGui.QFont.StyleItalic())
              
    def AddEvent(self):
        eventdialog = Events(self)

    def DeleteEvent(self):
        if not self.eventstree.currentItem() == None:
            deletemsg = "Are you sure you want to remove the event with all its actions?"
            reply = QtGui.QMessageBox.question(self, 'Confirm', deletemsg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.Cancel)

            if reply == QtGui.QMessageBox.Yes:
                root = self.eventstree.invisibleRootItem()
                for item in self.eventstree.selectedItems():
                    (item.parent() or root).removeChild(item)
                    self.readObjectActions()
            else:
                event.ignore()
                


    def AddToEventList(self, name):
        if name=="Create":
            self.create = QtGui.QTreeWidgetItem(self.eventstree,QtCore.QStringList(self.events[0]))
            self.create.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Events', 'create.png')))
            self.create.setSelected(True)
        elif name=="Step":
            self.stepeventree = QtGui.QTreeWidgetItem(self.eventstree,QtCore.QStringList(self.events[1]))
            self.stepeventree.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Events', 'step.png')))            
        elif name=="Destroy":
            self.destroy = QtGui.QTreeWidgetItem(self.eventstree,QtCore.QStringList(self.events[2]))
            self.destroy.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Events', 'destroy.png')))
        elif name=="Collision":
            self.collision = QtGui.QTreeWidgetItem(self.eventstree,QtCore.QStringList(self.events[3]))
            self.collision.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Events', 'collision.png')))      
        elif name=="Draw":
            self.draw = QtGui.QTreeWidgetItem(self.eventstree,QtCore.QStringList(self.events[4]))
            self.draw.setIcon(0, QtGui.QIcon(os.path.join('Data', 'Events', 'draw.png')))         
        
    #def ok(self):
    #    self.main.qmdiarea.activeSubWindow().close()
    def ok(self):
        self.close()
        icon = str(self.nameEdit.text())
        if self.FileName is not icon:

            in_fname = os.path.join(self.dirname, 'Objects', "%s.%s" %
                                    (self.FileName, self.extension))
            out_fname = os.path.join(self.dirname, 'Objects', "%s.%s" % 
                                        (icon, self.extension)) 
            #self.image_handle.close()
            os.rename(in_fname, out_fname)
            self.icon = str(self.nameEdit.text())
	self.main.updatetree()
        self.main.qmdiarea.activeSubWindow().close()
