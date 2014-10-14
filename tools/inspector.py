#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import os, sys, shutil

class Inspector(QtGui.QWidget):
    def __init__(self, main, image = None):
        super(Inspector, self).__init__(main)
        self.main = main
        self.image = image
        self.title = QtGui.QLabel("<h3>Inspector</h3>")
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.setPlaceholderText("Name")
        self.nameEdit.setMinimumWidth(150)
        self.information = QtGui.QLabel("")

        #IMAGE
        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)
        self.importButton = QtGui.QPushButton('&Import', self)
        self.importButton.clicked.connect(self.importImage)
        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setStyleSheet('background-image: url(../images/transparent.png);')
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.hide()
        #
        

        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (10)
        self.ContainerGrid.setSpacing(10)
        
        
        self.ContainerGrid.addWidget(self.title)
        self.ContainerGrid.addWidget(self.nameEdit, 1, 0)
        self.ContainerGrid.addWidget(self.importButton, 2, 0)
        self.ContainerGrid.addWidget(self.information, 3, 0)
        self.ContainerGrid.addWidget(self.scrollArea, 4, 0)
        

        self.spacer = QtGui.QWidget() 
        self.spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding) 
        self.ContainerGrid.addWidget(self.spacer)

        self.setLayout(self.ContainerGrid)

    def importImage(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '', "*.png")
        if fname:
            self.open_image(fname)
            shutil.copyfile(fname, os.path.join(
                            os.path.dirname(self.main.projectdir),
                            "sprites",
                            str(self.nameEdit.text())+".png" ))
            item = self.main.resourcelist.currentItem()
            item.setIcon(0, QtGui.QIcon(os.path.join(
                            os.path.dirname(self.main.projectdir),
                            "sprites",
                            str(self.nameEdit.text())+".png" )))

    def open_image(self, filename):
        fileName = filename
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.information.setText("X: "+ str(image.width()) + "\nY: " + str(image.height()))

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()