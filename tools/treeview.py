from PyQt4 import QtCore, QtGui
import os, sys
import scripteditor
import imageviewer

class TreeView(QtGui.QTreeView):
    def __init__(self, main):
        super(TreeView, self).__init__(main)
        self.main = main
        self.fileSystemModel = QtGui.QFileSystemModel(self)
        self.fileSystemModel.setReadOnly(False)
        self.clicked.connect(self.on_treeView_clicked)
        self.abstractitem = QtGui.QAbstractItemView
        self.setDragDropMode(self.abstractitem.InternalMove)
        self.connect (self,
                QtCore.SIGNAL ("currentTextChanged(const QString&)"),
                QtGui.qApp.quit)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.root = self.fileSystemModel.setRootPath(self.main.projectdir)
        self.setModel(self.fileSystemModel)
        self.setRootIndex(self.root)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        self.header().close()  
        self.indexItem=""
        self.connect(self,QtCore.SIGNAL('customContextMenuRequested(QPoint)'), self.doMenu)

        renameAction = QtGui.QAction('Rename', self)
        renameAction.triggered.connect(self.rename_file)

        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(self.main.editFileAction)
        self.popMenu.addAction(renameAction)
        self.popMenu.addAction(self.main.deleteFileAction)
        self.popMenu.addSeparator()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        self.indexItem = self.fileSystemModel.index(index.row(), 0, index.parent())
        filePath = self.fileSystemModel.filePath(self.indexItem)
        fileName = self.fileSystemModel.fileName(self.indexItem)

    def doMenu(self, point):
        self.popMenu.exec_( self.mapToGlobal(point) )

    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            self.edit_file()
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)

    def edit_file(self):
        target=str(self.abstractitem.currentIndex(self.main.treeView).data().toString())
        filePath = self.fileSystemModel.filePath(self.indexItem)
        if ".exe" in filePath:
            reply = QtGui.QMessageBox.question(self, "Not assigned", 
                         "Stellar does not have a progam to edit this kind of file, would you like to choose one?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)            
        if (".png" or ".jpg" or ".bmp") in filePath:
            self.main.window = imageviewer.ImageEditor(self.main, target, filePath)
            self.main.window.setWindowTitle(target)
            self.main.mdi.addSubWindow(self.main.window)
            self.main.window.setVisible(True)
        else:
            self.main.window = scripteditor.ScriptEditor(self.main, target, filePath)
            self.main.window.setWindowTitle(target)
            self.main.mdi.addSubWindow(self.main.window)
            self.main.window.setVisible(True)

    def delete_file(self):
        f= filePath = self.fileSystemModel.filePath(self.indexItem)
        delete_msg = "You are about to delete "+f+" Continue?"
        reply = QtGui.QMessageBox.question(self, 'Confirm', 
                         delete_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            os.remove(str(f))

    def rename_file(self):
        index = self.abstractitem.currentIndex(self.main.treeView)
        return QtGui.QTreeView.edit(self, index)